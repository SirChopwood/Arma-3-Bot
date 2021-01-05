import embedtemplates

async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Changes the name of a section from the ORBAT."))
        return
    if arguments == 0:
        await message.channel.send(content="", embed=embedtemplates.failure("Incorrect Argument Count", "Old Section Name and New Name should be separated by a |"))
        return
    arguments = arguments.split("|")
    if len(arguments) != 2:
        await message.channel.send(content="", embed=embedtemplates.failure("Incorrect Argument Count", "Please provide 2 Arguments separated by a |"))
        return
    section = self.database.get_section(message.guild.id, arguments[0])
    oldname = section["Name"]
    section["Name"] = arguments[1]
    self.database.set_section(message.guild.id, arguments[0], section)
    await message.channel.send("Section Name updated!")
    await message.channel.send(content="", embed=embedtemplates.success("Section Name Set", str(oldname + " -> " + arguments[1])))
