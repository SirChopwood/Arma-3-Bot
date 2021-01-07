import embedtemplates
import discord


async def set_name(self, ranks, message, user_id):
    user = self.database.get_user(message.guild.id, user_id)
    name = str(ranks[user["Rank"]]["Format"])

    name = name.replace("$RL", str(ranks[user["Rank"]]["Long"]))  # Long Rank Name
    name = name.replace("$RS", str(ranks[user["Rank"]]["Short"]))  # Long Rank Name
    name = name.replace("$FN", str(user["FirstName"]))  # Short User Name
    name = name.replace("$LN", str(user["LastName"]))  # Long User Name
    if "Nickname" in user:
        name = name.replace("$NN", str(user["Nickname"]))  # Nickname

    try:
        discorduser = await message.guild.fetch_member(user_id)
        await discorduser.edit(nick=name)
        await message.channel.send(content="", embed=embedtemplates.success("Name Set", name))
    except discord.Forbidden:
        await message.channel.send(content="", embed=embedtemplates.failure("Missing Permissions",
                                                                            str("I do not have permissions to set your name, " + name)))
        return


async def Main(self, message, command, arguments):
    ranks = self.database.get_ranks(message.guild.id)
    ranks = ranks["Dictionary"]
    if len(message.mentions) > 0:
        for member in message.mentions:
            await set_name(self, ranks, message, member.id)
        return

    else:
        await set_name(self, ranks, message, message.author.id)
        return
