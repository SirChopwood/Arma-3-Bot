import embedtemplates


async def Main(self, channel, message, user, emoji):
    if user.bot:
        return
    settings = self.database.get_settings(message.guild.id)
    if channel.id in settings["SuggestionChannels"] and message.id in settings["SuggestionHeaders"]:
        await message.clear_reactions()
        await message.add_reaction("<:YellowTick:783840786999279619>")  # <:PurpleCross:796199276853723146>

        await user.send(content="", embed=embedtemplates.question("What is your suggestion?", user.name))
        response = await self.await_response(user)

        suggestion = await channel.send(content="", embed=embedtemplates.suggestion(response.content))
        await suggestion.add_reaction("<:GreenTick:743466991771451394>")
        await suggestion.add_reaction("<:RedTick:743466992144744468>")
