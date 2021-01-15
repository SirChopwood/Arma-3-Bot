import embedtemplates
import permissions


async def Main(self, message, command, arguments):
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    settings = self.database.get_settings(message.guild.id)
    loa = await message.channel.send(content="", embed=embedtemplates.loa_header("React to this post to mark your LOA!"))
    await loa.add_reaction("<:PurpleCross:796199276853723146>")
    await message.delete()
    settings["LOAHeaders"].append(loa.id)
    self.database.set_settings(message.guild.id, settings)

