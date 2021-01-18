import embedtemplates
import json
import permissions


async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments == None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help("Adds a Rank to the server."))
        return
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    ranks = self.database.get_ranks(message.guild.id)
    with open("json_files/server_ranks_item.json", "r") as file:
        template = json.load(file)

    messages = []
    messages.append(message)

    template["Long"] = str(arguments)

    messages.append(
        await message.channel.send(content="", embed=embedtemplates.question("What is the Short Name of the new Rank?",
                                                                             message.author.display_name)))
    shortname = await self.await_response(message.author)
    messages.append(shortname)
    template["Short"] = str(shortname.content)

    messages.append(
        await message.channel.send(content="", embed=embedtemplates.question("What is the Format of the new Rank?",
                                                                             message.author.display_name)))
    formatting = await self.await_response(message.author)
    messages.append(formatting)
    template["Format"] = str(formatting.content)

    ranks["Dictionary"].append(template)
    self.database.set_ranks(message.guild.id, ranks)
    await message.channel.send(content="", embed=embedtemplates.success("Rank Added", str("Rank ``" + arguments + "`` added to server")))
    for m in messages:
        await m.delete()
