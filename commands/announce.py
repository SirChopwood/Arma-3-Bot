import embedtemplates
import json
import datetime
import permissions


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

    await message.author.send(content="", embed=embedtemplates.question("What is the date of the Operation? (DD/MM/YY)", message.author.display_name))
    opdate = await self.await_response(message.author)
    if opdate is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                            "You took too long to respond!"))
        return
    template["Operation"]["Date"] = opdate.content

    await message.author.send(content="", embed=embedtemplates.question("What is the time of the Operation? (MM:HH)", message.author.display_name))
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
    await message.delete()
