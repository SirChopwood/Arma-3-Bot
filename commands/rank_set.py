import os
import embedtemplates


async def Main(self, message, command, arguments):
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
    user["Rank"] = rank
    self.database.set_user(message.guild.id, user)
    await message.channel.send(content="", embed=embedtemplates.success("Rank Set",str(str(message.mentions[0])+" has been set to rank "+str(rank))))
    for m in messages:
        await m.delete()
