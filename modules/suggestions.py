import embedtemplates


async def Main(self, message):
    if message.content.startswith(">"):
        return
    suggestionchannels = self.database.get_settings(message.guild.id)["SuggestionChannels"]
    if message.channel.id in suggestionchannels:
        suggestion = await message.channel.send(content="", embed=embedtemplates.suggestion(message.content))
        await message.delete()
        await suggestion.add_reaction("<:GreenTick:743466991771451394>")
        await suggestion.add_reaction("<:RedTick:743466992144744468>")
