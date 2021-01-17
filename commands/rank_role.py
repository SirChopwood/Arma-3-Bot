import embedtemplates
import permissions


async def Main(self, message, command, arguments):
    if arguments == "" or arguments is None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help("Changes a Rank's Discord Role."))
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
        await message.channel.send(content="", embed=embedtemplates.question("Please mention (ping) the role you want attached to this Rank or type '0' for none.",
                                                                             message.author.display_name)))
    name = await self.await_response(message.author)
    messages.append(name)
    try:
        rank["RoleID"] = name.role_mentions[0].id
    except AttributeError:
        await message.channel.send(content="", embed=embedtemplates.failure("Invalid Argument",
                                                                            "Please mention (ping) the role you want attached to this Rank or type '0' for none!"))
        return

    self.database.set_ranks(message.guild.id, ranks)
    await message.channel.send(content="", embed=embedtemplates.success("Rank Edited", str("Rank RoleID changed to ``" + str(name.role_mentions[0].id) + "``.")))
    for m in messages:
        await m.delete()
