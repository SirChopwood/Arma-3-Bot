import embedtemplates
import json
import datetime
import permissions
import discord


async def Main(self, message, command, arguments):
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return

    with open("json_files/application_template.json", "r") as file:
        template = json.load(file)

    response = await self.question(message.author, "What is the application for?")
    if response is None:
        return
    else:
        template["Title"] = response.content

    questions = []
    questionloop = True
    while questionloop:
        if len(questions) == 24:
            await message.author.send(content="", embed=embedtemplates.failure("Max Question Limit",
                                                                               "Discord limits the number of questions to 24, sorry for this inconvenience!"))
            break
        response = await self.question(message.author, "What is question " + str(len(questions)+1) + "?")
        if response is None or response.content.lower() == "done":
            questionloop = False
        else:
            questions.append(response.content)

    if len(questions) == 0:
        await message.author.send(content="", embed=embedtemplates.failure("No Questions Given",
                                                                           "You did not supply any questions before ending!"))

    template["Questions"] = questions

    application = await message.channel.send(content="", embed=embedtemplates.application_header(str("Application: " + template["Title"]), questions))

    template["MessageID"] = application.id
    template["PostDate"] = datetime.datetime.now()

    self.database.add_application(message.guild.id, template)
    await application.add_reaction("<:YellowTick:783840786999279619>")

    try:
        await message.author.send(content="", embed=embedtemplates.success("Application Posted", "The Application has been posted and is now accepting responses."))
    except discord.Forbidden:
        print(message.author.name, "Could not be messaged.")
    await message.delete()

