import embedtemplates
import discord


async def Main(self, channel, message, user, emoji):
    member = await channel.guild.fetch_member(user.id)
    settings = self.database.get_settings(message.guild.id)
    admin_access = False

    if member.bot:
        return

    for role in member.roles:
        if role.id == settings["AdminRole"]:
            admin_access = True

    if channel.id in settings["SuggestionChannels"] and message.id in settings["SuggestionHeaders"]:
        await member.send(content="", embed=embedtemplates.question("What is your suggestion?", member.name))
        response = await self.await_response(member)
        if response is None:
            try:
                await user.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                                "You took too long to respond!"))
            except discord.Forbidden:
                print(user.name, "Could not be messaged.")
            return

        suggestion = await channel.send(content="", embed=embedtemplates.suggestion(response.content))
        await suggestion.add_reaction("<:GreenTick:743466991771451394>")
        await suggestion.add_reaction("<:RedTick:743466992144744468>")

        newmessage = await message.channel.send(content="", embed=embedtemplates.suggestion("React to this post to make an anonymous suggestion!"))
        await message.delete()
        await newmessage.add_reaction("<:YellowTick:783840786999279619>")

    if channel.id in settings["SuggestionChannels"] and admin_access and message.id not in settings["SuggestionHeaders"]:
        if str(emoji.name) == "YellowTick":
            embed = message.embeds[0]
            embed.colour = discord.Colour(0x00ff00)
            embed.title = "Suggestion - Accepted"
            await message.edit(content="", embed=embed)
        elif str(emoji.name) == "PurpleTick":
            embed = message.embeds[0]
            embed.colour = discord.Colour(0xff0000)
            embed.title = "Suggestion - Declined"
            await message.edit(content="", embed=embed)
