import embedtemplates
import permissions


async def Main(self, message, command, arguments):
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    settings = self.database.get_settings(message.guild.id)
    suggestion = await message.channel.send(content="", embed=embedtemplates.suggestion("React to this post to make an anonymous suggestion!"))
    await suggestion.add_reaction("<:YellowTick:783840786999279619>")
    await message.delete()
    if suggestion.id not in settings["SuggestionHeaders"]:
        settings["SuggestionHeaders"].append(suggestion.id)
        self.database.set_settings(message.guild.id, settings)

