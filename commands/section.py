import embedtemplates

async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Displays a section from the ORBAT."))
        return
    section = self.database.get_section(message.guild.id, arguments)
    await message.channel.send(content="", embed=embedtemplates.success("Displaying Section", str(section)))
