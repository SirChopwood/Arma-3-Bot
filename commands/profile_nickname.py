import embedtemplates


async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="",
                                   embed=embedtemplates.help("Sets the user's nickname, should only be used if needed. Will not be shown unless specified in their rank format."))
        return

    user = self.database.get_user(message.guild.id, message.author.id)
    user["Nickname"] = arguments

    self.database.set_user(message.guild.id, user)
    await message.channel.send(content="", embed=embedtemplates.success("Nickname Updated", str("Hello " + arguments)))
