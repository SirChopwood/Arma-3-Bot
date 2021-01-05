import embedtemplates
import json


async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help("Adds a member slot to a section on the ORBAT"))
        return
    arguments = arguments.split("|")
    if len(arguments) != 4:
        await message.channel.send(content="", embed=embedtemplates.failure("Incorrect Argument Count", "Please provide the 4 Arguments (Section, Slot, Rank, Access) separated by a |"))
        return
    section = self.database.get_section(message.guild.id, arguments[0])
    with open("json_files/section_slot_template.json", "r") as file:
        template = json.load(file)
    template["Role"] = str(arguments[1])
    template["Rank"] = str(arguments[2])
    template["Access"] = bool(arguments[3])

    section["Structure"].append(template)
    self.database.set_section(message.guild.id, arguments[0], section)
    await message.channel.send(content="", embed=embedtemplates.success("Section Member Slot Added", str("Slot " + arguments[1] + "/" + arguments[2] + " added to section")))
