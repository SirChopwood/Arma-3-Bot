import os
import embedtemplates


async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments is None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Shows details regarding a specific rank."))
        return
    try:
        rank = int(arguments)
        ranks = self.database.get_ranks(message.guild.id)
        ranklist = "```\n"
        for key in ranks["Dictionary"][rank]:
            ranklist = str(ranklist + key + ": " + ranks["Dictionary"][rank][key] + "\n")
        ranklist = ranklist + "```"
        await message.channel.send(content="", embed=embedtemplates.help(ranklist))
        return
    except ValueError:
        await message.channel.send(content="", embed=embedtemplates.failure("Incorrect Argument Type", "Please state a single integer"))
        return
    except IndexError:
        await message.channel.send(content="", embed=embedtemplates.failure("Incorrect Argument Value", "Please state an existing ranks' value"))
        return
