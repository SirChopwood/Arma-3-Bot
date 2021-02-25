import embedtemplates
import permissions


async def Main(self, message, command, arguments):
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    settings = self.database.get_settings(message.guild.id)
    await message.channel.send(content="", embed=embedtemplates.application_header("Any applications posted will have results posted below!"))
    await message.delete()
    settings["ApplicationResults"] = message.channel.id
    self.database.set_settings(message.guild.id, settings)

