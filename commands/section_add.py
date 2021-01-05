import embedtemplates

async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Creates a new section for the ORBAT. Must specify the name"))
        return
    self.database.add_section(message.guild.id, arguments)
    await message.channel.send(content="", embed=embedtemplates.success("Section Created", str("``"+arguments+"`` created!")))
