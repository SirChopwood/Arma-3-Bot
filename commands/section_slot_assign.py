import embedtemplates
import permissions


async def remove_old_position(self, message):
    sections = self.database.get_all_sections(message.guild.id)
    for section in sections:
        for i in range(len(section["Structure"])):
            if section["Structure"][i]["ID"] == message.mentions[0].id:
                section["Structure"][i]["ID"] = 0
                self.database.set_section(message.guild.id, section["Name"], section)
                return True

    return False


async def set_user(self, message, sectionname, slotname):
    status = False

    section = self.database.get_section(message.guild.id, sectionname)
    if section is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Section Not Found",
                                                                            "A section with that name was not found!"))
        return
    if not await permissions.is_section_admin(self, message.guild.id, message.author.id, sectionname) and not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    removedrole = await remove_old_position(self, message)
    for i in range(len(section["Structure"])):
        if section["Structure"][i]["Role"] == slotname and section["Structure"][i]["ID"] == 0 and not status:
            section["Structure"][i]["ID"] = message.mentions[0].id
            status = self.database.set_section(message.guild.id, sectionname, section)

    if status and removedrole:
        await message.channel.send(content="", embed=embedtemplates.success("Slot Assignment", str(
            "User " + str(message.mentions[0].display_name) + " has been removed from their old role and added to " + sectionname + "/" + slotname)))
    elif status and not removedrole:
        await message.channel.send(content="", embed=embedtemplates.success("Slot Assignment", str(
            "User " + str(message.mentions[0].display_name) + " has been added to " + sectionname + "/" + slotname)))
    else:
        await message.channel.send(content="", embed=embedtemplates.failure("Assignment Failed", "Section or Role could not be found"))


async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help("Adds a member to a slot in a section on the ORBAT"))
        return

    elif len(message.mentions) > 0: # Questioned Responses
        messages = []
        messages.append(message)
        messages.append(await message.channel.send(content="", embed=embedtemplates.question("What Section should they be moved into?", message.author.display_name)))
        section = await self.await_response(message.author)
        messages.append(section)
        messages.append(await message.channel.send(content="", embed=embedtemplates.question("What Slot should they be moved into?", message.author.display_name)))
        slot = await self.await_response(message.author)
        messages.append(slot)
        await set_user(self, message, section.content, slot.content)
        for m in messages:
            await m.delete()
