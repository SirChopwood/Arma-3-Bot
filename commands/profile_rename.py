import embedtemplates
import discord


async def Main(self, message, command, arguments):
    messages = []
    user = self.database.get_user(message.guild.id, message.author.id)
    if user is not None:
        messages.append(await message.channel.send(content="", embed=embedtemplates.question(
            "What is your FIRST name? (Max 10 Characters)",
            message.author.display_name)))
        response = await self.await_response(message.author)
        if response is None:
            await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                                "You took too long to respond!"))
            return
        user["FirstName"] = response.content
        messages.append(response)

        messages.append(await message.channel.send(content="", embed=embedtemplates.question(
            "What is your LAST name? (Max 10 Characters)",
            message.author.display_name)))
        response = await self.await_response(message.author)
        if response is None:
            await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                                "You took too long to respond!"))
            return
        user["LastName"] = response.content
        messages.append(response)
        self.database.set_user(message.guild.id, user)
        for m in messages:
            try:
                await m.delete()
            except discord.Forbidden:
                continue
        await self.run_file("setname", message, arguments)
        await message.channel.send(content="", embed=embedtemplates.success("User's Names Updated", str(
                "Welcome " + message.author.mention)))


    else:
        await message.channel.send(content="", embed=embedtemplates.failure("Not Registered",
                                                                            "You have not registered in this guild!"))
        return
