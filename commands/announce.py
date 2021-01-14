import embedtemplates
import json
import datetime


async def Main(self, message, command, arguments):

    with open("json_files/announcement_template.json", "r") as file:
        template = json.load(file)
    template["Operation"]["Host"] = message.author.display_name

    await message.author.send(content="", embed=embedtemplates.question("What is the name of the Operation?", message.author.display_name))
    opname = await self.await_response(message.author)
    template["Operation"]["Title"] = opname.content

    await message.author.send(content="", embed=embedtemplates.question("What is the date of the Operation? (DD/MM/YY)", message.author.display_name))
    opdate = await self.await_response(message.author)
    template["Operation"]["Date"] = opdate.content

    await message.author.send(content="", embed=embedtemplates.question("What is the time of the Operation? (MM:HH)", message.author.display_name))
    optime = await self.await_response(message.author)
    template["Operation"]["Time"] = optime.content

    await message.author.send(content="", embed=embedtemplates.question("Post an image or link to an image of the Operation.", message.author.display_name))
    opimage = await self.await_response(message.author)
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
