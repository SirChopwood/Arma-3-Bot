import embedtemplates
import json
import permissions


async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help("Adds a member slot to a section on the ORBAT"))
        return
    if not await permissions.is_section_admin(self, message.guild.id, message.author.id, arguments) and not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    section = self.database.get_section(message.guild.id, arguments)
    with open("json_files/section_slot_template.json", "r") as file:
        template = json.load(file)

    messages = []
    messages.append(message)
    messages.append(await message.channel.send(content="", embed=embedtemplates.question("What is the name of the new Slot?",
                                                                                         message.author.display_name)))
    role = await self.await_response(message.author)
    messages.append(role)
    template["Role"] = str(role.content)

    messages.append(
        await message.channel.send(content="", embed=embedtemplates.question("Should this slot have admin access to the section? (True = 1/False = 0))",
                                                                             message.author.display_name)))
    admin = await self.await_response(message.author)
    messages.append(admin)
    try:
        template["Access"] = bool(int(admin.content))
    except TypeError:
        await message.channel.send(content="", embed=embedtemplates.failure("Invalid Argument",
                                                                            "Section Admin Access (True = 1/False = 0)"))
        return

    section["Structure"].append(template)
    self.database.set_section(message.guild.id, arguments, section)
    await message.channel.send(content="", embed=embedtemplates.success("Section Member Slot Added", str("Slot ``" + arguments + "/" + role.content + "(" + str(bool(int(admin.content))) + ")`` added to section")))
    for m in messages:
        await m.delete()
