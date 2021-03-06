import embedtemplates
import discord
import permissions


async def set_name(self, ranks, message, user_id):
    user = self.database.get_user(message.guild.id, user_id)
    name = str(ranks[user["Rank"]]["Format"])

    name = name.replace("$RL", str(ranks[user["Rank"]]["Long"]))  # Long Rank Name
    name = name.replace("$RS", str(ranks[user["Rank"]]["Short"]))  # Long Rank Name
    name = name.replace("$FN", str(user["FirstName"]))  # Short User Name
    name = name.replace("$LN", str(user["LastName"]))  # Long User Name
    name = name.replace("$FI", str(user["FirstName"][0]))  # Short User Name Initial
    name = name.replace("$LI", str(user["LastName"][0]))  # Long User Name Initial
    if "Nickname" in user:
        name = name.replace("$NN", str(user["Nickname"]))  # Nickname
    elif "$NN" in name:
        await message.channel.send(content="", embed=embedtemplates.failure("Missing Nickname",
                                                                            str("User needs to set a nickname first, then retry with ``>setname``.")))
        return 0

    try:
        discorduser = await message.guild.fetch_member(user_id)
        await discorduser.edit(nick=name)
        return 1
    except discord.Forbidden:
        await message.channel.send(content="", embed=embedtemplates.failure("Missing Permissions",
                                                                            str("I do not have permissions to set your name, " + name)))
        return 0


async def Main(self, message, command, arguments):
    ranks = self.database.get_ranks(message.guild.id)
    ranks = ranks["Dictionary"]
    status = 0
    if len(message.mentions) > 0:
        if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
            await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                                "User does not have permission to use this!"))
            return
        for member in message.mentions:
            status += await set_name(self, ranks, message, member.id)

    if len(message.role_mentions) > 0:
        if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
            await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                                "User does not have permission to use this!"))
            return
        for role_mention in message.role_mentions:
            for member in role_mention.members:
                status += await set_name(self, ranks, message, member.id)

    else:
        status = await set_name(self, ranks, message, message.author.id)

    await message.channel.send(content="", embed=embedtemplates.success("Name(s) Set", str(str(status) + " Name(s) were set.")))
