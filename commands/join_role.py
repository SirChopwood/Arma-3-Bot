import embedtemplates
import permissions


async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Changes the Discord Role that you get when Joining."))
        return
    if not await permissions.is_section_admin(self, message.guild.id, message.author.id, arguments[0]) and not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    settings = self.database.get_settings(message.guild.id)

    try:
        settings["JoinRole"] = int(message.role_mentions[0].id)
    except AttributeError:
        await message.channel.send(content="", embed=embedtemplates.failure("Invalid Argument",
                                                                            "Please mention (ping) the role you want on Join or type '0' for none!"))
        return

    self.database.set_settings(message.guild.id, settings)
    await message.channel.send(content="", embed=embedtemplates.success("Settings Edited", str("Join RoleID changed to ``" + str(message.role_mentions[0].id) + "``.")))
    await message.delete()
