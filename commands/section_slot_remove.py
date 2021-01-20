import embedtemplates
import json
import permissions


async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help("Removes a member slot from a section on the ORBAT"))
        return
    if not await permissions.is_section_admin(self, message.guild.id, message.author.id, arguments) and not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    section = self.database.get_section(message.guild.id, arguments)

    messages = []
    messages.append(message)
    messages.append(await message.channel.send(content="", embed=embedtemplates.question("What is the Role Name of the Slot you want to remove?",
                                                                                         message.author.display_name)))
    role = await self.await_response(message.author)
    if role is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                            "You took too long to respond!"))
        return
    messages.append(role)

    removed = False
    for i in range(len(section["Structure"])):
        if section["Structure"][i]["Role"] == role.content:
            section["Structure"].pop(i)
            removed = True
            break

    if removed:
        self.database.set_section(message.guild.id, arguments, section)
        await message.channel.send(content="", embed=embedtemplates.success("Section Member Slot Removed",
                                                                            str("The slot ``" + role.content + "`` was removed.")))
    else:
        await message.channel.send(content="", embed=embedtemplates.failure("Unknown Slot",
                                                                            "A slot by the name provided could not be found!"))
    for m in messages:
        await m.delete()
