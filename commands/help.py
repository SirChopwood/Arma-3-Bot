import os
import embedtemplates


async def Main(self, message, command, arguments):
    commandlist = "***Command List:***\n*type > followed by the command name for help*\n```\n"
    for command_file in os.listdir("commands"):
        if command_file == "__init__.py" or command_file == "__pycache__":
            continue
        else:
            commandlist = commandlist + command_file.replace(".py", "") + "\n"
    commandlist = commandlist + "```"

    await message.channel.send(content="", embed=embedtemplates.help(commandlist))
