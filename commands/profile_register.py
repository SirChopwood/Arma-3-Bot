import embedtemplates
import json

async def Main(self, message, command, arguments):
    messages = []
    with open("json_files/user_profile.json", "r") as file:
        template = json.load(file)
    template["DiscordID"] = message.author.id

    messages.append(await message.channel.send(content="", embed=embedtemplates.question("What is your first name?",
                                                                         message.author.display_name)))
    response = await self.await_response(message.author)
    template["FirstName"] = response.content
    messages.append(response)

    messages.append(await message.channel.send(content="", embed=embedtemplates.question("What is your last name?",
                                                                                         message.author.display_name)))
    response = await self.await_response(message.author)
    template["LastName"] = response.content
    messages.append(response)

    self.database.add_user(message.guild.id, template)
    await message.channel.send(content="", embed=embedtemplates.success("User Registered", str("Welcome " + message.author.mention)))
    embed = embedtemplates.profile(self, message.guild.id, message.author)
    await message.channel.send(content="", embed=embed)
    for m in messages:
        await m.delete()
