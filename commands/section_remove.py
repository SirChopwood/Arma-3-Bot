import embedtemplates
import permissions


async def Main(self, message, command, arguments):
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Removes a section from the server."))
        return

    if self.database.remove_section(message.guild.id, arguments):
        await message.channel.send(content="", embed=embedtemplates.success("Section Removed", str("The section ``"+arguments+"`` has been removed!")))
    else:
        await message.channel.send(content="", embed=embedtemplates.failure("Unknown Section",
                                                                            "A section could not be found by this name!"))
