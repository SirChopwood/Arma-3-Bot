import embedtemplates


async def Main(self, message, command, arguments):
    settings = self.database.get_settings(message.guild.id)
    suggestion = await message.channel.send(content="", embed=embedtemplates.suggestion("React to this post to make an anonymous suggestion!"))
    await suggestion.add_reaction("<:YellowTick:783840786999279619>")
    await message.delete()
    settings["SuggestionHeaders"].append(suggestion.id)
    self.database.set_settings(message.guild.id, settings)

