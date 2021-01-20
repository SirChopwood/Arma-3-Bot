import embedtemplates
import permissions
import discord

async def Main(self, message, command, arguments):
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    if arguments == 0 or arguments == "" or arguments is None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Sets the targeted user's rank."))
        return
    if len(message.mentions) < 1:
        await message.channel.send(content="", embed=embedtemplates.failure("No Target User",
                                                                            "Please mention one or multiple users to set their rank."))
        return

    messages = []
    messages.append(message)

    messages.append(await message.channel.send(content="", embed=embedtemplates.question("What Rank ID should they be set to?", message.author.display_name)))
    try:
        rankmsg = await self.await_response(message.author)
        if rankmsg is None:
            await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                                "You took too long to respond!"))
            return
        rank = int(rankmsg.content)
    except ValueError:
        await message.channel.send(content="", embed=embedtemplates.failure("Incorrect Argument Type", "Please state a single interger"))
        return
    messages.append(rankmsg)
    ranks = self.database.get_ranks(message.guild.id)
    if rank > (len(ranks["Dictionary"])-1) or rank < 0:
        await message.channel.send(content="", embed=embedtemplates.failure("Incorrect Argument Value",
                                                                            "Please state an existing ranks' value"))
        return
    user = self.database.get_user(message.guild.id, message.mentions[0].id)
    oldrank = user["Rank"]
    user["Rank"] = rank
    self.database.set_user(message.guild.id, user)

    if ranks["Dictionary"][oldrank]["RoleID"] != 0:
        role = message.guild.get_role(ranks["Dictionary"][oldrank]["RoleID"])
        try:
            await message.mentions[0].remove_roles(role)
        except discord.Forbidden:
            await message.channel.send(content="", embed=embedtemplates.failure("Missing Permissions",
                                                                                str(
                                                                                    "I do not have permissions to set your roles, " + message.author.display_name)))
            return

    if ranks["Dictionary"][rank]["RoleID"] != 0:
        role = message.guild.get_role(ranks["Dictionary"][rank]["RoleID"])
        try:
            await message.mentions[0].add_roles(role)
        except discord.Forbidden:
            await message.channel.send(content="", embed=embedtemplates.failure("Missing Permissions",
                                                                                str(
                                                                                    "I do not have permissions to set your roles, " + message.author.display_name)))
            return

    await message.channel.send(content="", embed=embedtemplates.success("Rank Set", str(str(message.mentions[0])+" has been set to rank "+str(rank))))
    for m in messages:
        await m.delete()
