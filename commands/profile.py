import embedtemplates


async def Main(self, message, command, arguments):
    if len(message.mentions) > 0:
        for member in message.mentions:
            embed = embedtemplates.profile(self, message.guild.id, member)
            await message.channel.send(content="", embed=embed)
            return
    else:
        embed = embedtemplates.profile(self, message.guild.id, message.author)
        await message.channel.send(content="", embed=embed)
        return
