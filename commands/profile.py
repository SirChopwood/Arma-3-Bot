import embedtemplates


async def Main(self, message, command, arguments):
    if len(message.mentions) > 0:
        for member in message.mentions:
            embed = embedtemplates.profile(self, message.guild.id, member)
            if embed is not None:
                await message.channel.send(content="", embed=embed)
            else:
                await message.channel.send(content="", embed=embedtemplates.failure("Profile Not Found", "User does not have a profile, please register!"))
            return
    else:
        embed = embedtemplates.profile(self, message.guild.id, message.author)
        if embed is not None:
            await message.channel.send(content="", embed=embed)
        else:
            await message.channel.send(content="", embed=embedtemplates.failure("Profile Not Found",
                                                                                "User does not have a profile, please register!"))
        return
