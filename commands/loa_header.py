import embedtemplates


async def Main(self, message, command, arguments):
    settings = self.database.get_settings(message.guild.id)
    loa = await message.channel.send(content="", embed=embedtemplates.loa_header("React to this post to mark your LOA!"))
    await loa.add_reaction("<:PurpleCross:796199276853723146>")
    await message.delete()
    settings["LOAHeaders"].append(loa.id)
    self.database.set_settings(message.guild.id, settings)

