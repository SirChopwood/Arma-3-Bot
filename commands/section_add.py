import embedtemplates
import permissions


async def Main(self, message, command, arguments):
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Creates a new section for the ORBAT. Must specify the name"))
        return
    self.database.add_section(message.guild.id, arguments)
    await message.channel.send(content="", embed=embedtemplates.success("Section Created", str("``"+arguments+"`` created!")))
