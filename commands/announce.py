import embedtemplates
import json
import datetime
import permissions
import discord


async def Main(self, message, command, arguments):
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return

    with open("json_files/announcement_template.json", "r") as file:
        template = json.load(file)
    template["Operation"]["Host"] = message.author.display_name

    await message.author.send(content="", embed=embedtemplates.question("What is the name of the Operation?", message.author.display_name))
    opname = await self.await_response(message.author)
    if opname is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                            "You took too long to respond!"))
        return
    template["Operation"]["Title"] = opname.content

    await message.author.send(content="", embed=embedtemplates.question("What is the date of the Operation (UTC)? (DD/MM/YYYY)", message.author.display_name))
    opdate = await self.await_response(message.author)
    if opdate is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                            "You took too long to respond!"))
        return
    template["Operation"]["Date"] = opdate.content

    await message.author.send(content="", embed=embedtemplates.question("What is the time of the Operation (UTC)? (HH:MM)", message.author.display_name))
    optime = await self.await_response(message.author)
    if optime is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                            "You took too long to respond!"))
        return
    template["Operation"]["Time"] = optime.content

    await message.author.send(content="", embed=embedtemplates.question("Post an image or link to an image of the Operation.", message.author.display_name))
    opimage = await self.await_response(message.author)
    if opimage is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                            "You took too long to respond!"))
        return
    if opimage.attachments[0]:
        template["Operation"]["Image"] = opimage.attachments[0].url
    else:
        template["Operation"]["Image"] = opimage.content

    try:
        datetime.datetime.strptime(str(template["Operation"]["Date"] + " " + template["Operation"][
            "Time"]), '%d/%m/%Y %H:%M')
    except ValueError:
        await message.channel.send(content="", embed=embedtemplates.failure("Invalid Arguments",
                                                                            "Your date or time does not match the specified format!"))
        return

    announcement = await message.channel.send(content="",
                                              embed=embedtemplates.announcement(template["Operation"]["Title"],
                                                                                template["Operation"]["Time"],
                                                                                template["Operation"]["Date"],
                                                                                template["Operation"]["Image"],
                                                                                template["Operation"]["Host"]))



    template["MessageID"] = announcement.id
    template["PostDate"] = datetime.datetime.now()
    settings = self.database.get_settings(message.guild.id)
    settings["ActiveAnnouncements"].append(announcement.id)
    self.database.set_settings(message.guild.id, settings)
    self.database.add_announcement(message.guild.id, template)
    await announcement.add_reaction("<:GreenTick:743466991771451394>")
    await announcement.add_reaction("<:YellowTick:783840786999279619>")
    await announcement.add_reaction("<:BlueTick:783838821681987594>")
    await announcement.add_reaction("<:RedTick:743466992144744468>")

    for user in self.database.get_all_users(message.guild.id):
        if user["LOA"]:
            self.announcement_queue.put({"GuildID": message.guild.id, "AnnouncementID": announcement.id,
                                         "UserID": user["DiscordID"], "Status": "LOA"})

    try:
        await message.author.send(content="", embed=embedtemplates.success("Announcement Posted", "Announcement has been posted into the channel and is now being tracked for attendance."))
    except discord.Forbidden:
        print(message.author.name, "Could not be messaged.")
    await message.delete()

