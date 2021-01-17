import embedtemplates
import permissions


async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Changes a section's Discord Role."))
        return
    if not await permissions.is_section_admin(self, message.guild.id, message.author.id, arguments[0]) and not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    section = self.database.get_section(message.guild.id, arguments)
    messages = []
    messages.append(message)

    messages.append(
        await message.channel.send(content="", embed=embedtemplates.question(
            "Please mention (ping) the role you want attached to this Section or type '0' for none.",
            message.author.display_name)))
    name = await self.await_response(message.author)
    messages.append(name)
    try:
        section["RoleID"] = int(name.role_mentions[0].id)
    except AttributeError:
        await message.channel.send(content="", embed=embedtemplates.failure("Invalid Argument",
                                                                            "Please mention (ping) the role you want attached to this Section or type '0' for none!"))
        return

    self.database.set_section(message.guild.id, arguments, section)
    await message.channel.send(content="", embed=embedtemplates.success("Rank Edited", str("Rank RoleID changed to ``" + str(name.role_mentions[0].id) + "``.")))
