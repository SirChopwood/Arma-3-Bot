import os
import embedtemplates


async def Main(self, message, command, arguments):
    ranks = self.database.get_ranks(message.guild.id)
    ranklist = "```\n"
    for i in range(len(ranks["Dictionary"])):
        ranklist = str(ranklist + str(i) + ": " + ranks["Dictionary"][i]["Long"] + "\n")
    ranklist = ranklist + "```"
    await message.channel.send(content="", embed=embedtemplates.help(ranklist))
