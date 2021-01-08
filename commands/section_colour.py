import embedtemplates

async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Displays a section from the ORBAT."))
        return
    arguments = arguments.split("|")
    if len(arguments) != 2:
        await message.channel.send(content="", embed=embedtemplates.failure("Incorrect Argument Count", "Please provide 2 Arguments separated by a |"))
        return
    if len(arguments[1]) != 6:
        await message.channel.send(content="", embed=embedtemplates.failure("Incorrect Argument Format",
                                                                            "Section Name and Colour (Hex code without the #) should be separated by a |"))
        return
    section = self.database.get_section(message.guild.id, arguments[0])
    section["Colour"] = arguments[1]
    self.database.set_section(message.guild.id, arguments[0], section)
    await message.channel.send(content="", embed=embedtemplates.success("Section Colour updated!", str("Colour set to: " + section["Colour"])), )