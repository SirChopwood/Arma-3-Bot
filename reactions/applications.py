import embedtemplates
import discord
import datetime


async def Main(self, channel, message, user, emoji):
    member = await channel.guild.fetch_member(user.id)
    settings = self.database.get_settings(message.guild.id)
    admin_access = False

    if member.bot:
        return

    for role in member.roles:
        if role.id == settings["AdminRole"]:
            admin_access = True

    application = self.database.get_application(message.guild.id, message.id)

    if channel.id == settings["ApplicationResults"] and admin_access:
        if str(emoji.name) == "YellowTick":
            embed = message.embeds[0]
            embed.colour = discord.Colour(0x00ff00)
            embed.title = embed.title + " - Accepted"
            await message.edit(content="", embed=embed)
        elif str(emoji.name) == "PurpleTick":
            embed = message.embeds[0]
            embed.colour = discord.Colour(0xff0000)
            embed.title = embed.title + " - Declined"
            await message.edit(content="", embed=embed)

    elif application is not None:
        if str(emoji.name) == "YellowTick":
            responses = []
            for question in application["Questions"]:
                response = await self.question(user, question)
                if response is not None:
                    responses.append(response.content)
                else:
                    return
            resultschannel = await self.fetch_channel(settings["ApplicationResults"])
            resultmessage = await resultschannel.send(content="", embed=embedtemplates.application(user, application["MessageID"], application["Questions"], responses))
            await resultmessage.add_reaction("<:GreenTick:743466991771451394>")
            await resultmessage.add_reaction("<:RedTick:743466992144744468>")
            result = {"DiscordID": user.id, "DateTime": datetime.datetime.now(), "Answers": responses}
            application["Results"].append(result)
            self.database.set_application(message.guild.id, application)
            await user.send(content="", embed=embedtemplates.success("Response Posted",
                                                                               "The Response has been posted."))