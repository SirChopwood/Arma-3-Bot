import embedtemplates
import permissions


async def Main(self, message, command, arguments):
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return

    embed = embedtemplates.settings(self, message.guild.id)

    if embed is not None:
        await message.channel.send(content="", embed=embed)
    else:
        await message.channel.send(content="", embed=embedtemplates.failure("Profile Not Found",
                                                                            "User does not have a profile, please register!"))
    return
    await message.delete()
