import embedtemplates
import discord


async def Main(self, channel, message, user, emoji):
    member = await channel.guild.fetch_member(user.id)
    settings = self.database.get_settings(message.guild.id)
    admin_access = False
    for role in member.roles:
        if role.id == settings["AdminRole"]:
            admin_access = True

    if channel.id in settings["SuggestionChannels"] and message.id in settings["SuggestionHeaders"]:
        await message.clear_reactions()
        await message.add_reaction("<:YellowTick:783840786999279619>")  # <:PurpleCross:796199276853723146>

        await member.send(content="", embed=embedtemplates.question("What is your suggestion?", member.name))
        response = await self.await_response(member)

        suggestion = await channel.send(content="", embed=embedtemplates.suggestion(response.content))
        await suggestion.add_reaction("<:GreenTick:743466991771451394>")
        await suggestion.add_reaction("<:RedTick:743466992144744468>")
    if channel.id in settings["SuggestionChannels"] and admin_access:
        if str(emoji) == "<:YellowTick:783840786999279619>":
            embed = message.embeds[0]
            embed.colour = discord.Colour(0x00ff00)
            embed.title = "Suggestion - Accepted"
            await message.edit(content="", embed=embed)
        elif str(emoji) == "<:PurpleTick:796199276853723146>":
            embed = message.embeds[0]
            embed.colour = discord.Colour(0xff0000)
            embed.title = "Suggestion - Declined"
            await message.edit(content="", embed=embed)
