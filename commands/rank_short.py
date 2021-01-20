import embedtemplates
import permissions


async def Main(self, message, command, arguments):
    if arguments == "" or arguments is None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help("Changes a Rank's Short Name.."))
        return
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    ranks = self.database.get_ranks(message.guild.id)
    try:
        rank = ranks["Dictionary"][int(arguments)]
    except TypeError or IndexError:
        await message.channel.send(content="", embed=embedtemplates.failure("Invalid Argument",
                                                                            "Please provide the ID of the rank!"))
        return

    messages = []
    messages.append(message)

    messages.append(
        await message.channel.send(content="", embed=embedtemplates.question("What is the new Short Name of the Rank?",
                                                                             message.author.display_name)))
    name = await self.await_response(message.author)
    if name is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                            "You took too long to respond!"))
        return
    messages.append(name)
    rank["Short"] = name.content

    self.database.set_ranks(message.guild.id, ranks)
    await message.channel.send(content="", embed=embedtemplates.success("Rank Edited", str("Rank Short Name changed to ``" + name.content + "``.")))
    for m in messages:
        await m.delete()
