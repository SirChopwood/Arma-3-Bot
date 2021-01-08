import embedtemplates


async def Main(self, channel, message, user, emoji):
    settings = self.database.get_settings(message.guild.id)
    if channel.id in settings["LOAChannels"] and message.id in settings["LOAHeaders"]:
        await message.clear_reactions()
        await message.add_reaction("<:PurpleCross:796199276853723146>")
        user2 = await channel.guild.fetch_member(user.id)

        await user.send(content="", embed=embedtemplates.question("When will your LOA start?", user.name))
        start = await self.await_response(user)

        await user.send(content="", embed=embedtemplates.question("When will your LOA end?", user.name))
        end = await self.await_response(user)

        await user.send(content="", embed=embedtemplates.question("What is the reason for your LOA?", user.name))
        reason = await self.await_response(user)

        if start is not None and end is not None and reason is not None:
            await user.send(content="", embed=embedtemplates.success("LOA Posted", "Check the LOA Channel for Details"))
            await channel.send(content="", embed=embedtemplates.loa(startdate=start.content, enddate=end.content, reason=reason.content, user=user2))
