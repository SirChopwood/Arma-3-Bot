import embedtemplates
import permissions


async def Main(self, message, command, arguments):
    if arguments == "" or arguments is None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help("Removes a Rank from the server."))
        return
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    ranks = self.database.get_ranks(message.guild.id)
    try:
        ranks["Dictionary"].pop(int(arguments))
    except TypeError or IndexError:
        await message.channel.send(content="", embed=embedtemplates.failure("Invalid Argument",
                                                                            "Please provide the ID of the rank!"))
        return

    for user in self.database.get_users_of_rank(message.guild.id, arguments):
        user["Rank"] = 0
        self.database.set_user(message.guild.id, user)

    for user in self.database.get_users_over_rank(message.guild.id, arguments):
        user["Rank"] = int(user["Rank"]) - 1
        self.database.set_user(message.guild.id, user)

    self.database.set_ranks(message.guild.id, ranks)
    await message.channel.send(content="", embed=embedtemplates.success("Rank Removed", str("Rank " + arguments + " has been removed and all user's ranks have been adjusted accordingly.")))
