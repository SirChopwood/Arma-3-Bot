import discord
import importlib
import os
import importlib.util
import mongodatabase
import sys
import traceback
import asyncio
import embedtemplates
import datetime
import json
import background_tasks


class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = mongodatabase.Main()

    async def run_file(self, filename, message="", arguments=""):
        command_found = False
        for command_file in os.listdir("commands"):
            if command_file in ["__init__.py", "__pycache__"]:
                continue
            elif command_file[:-3] == filename:
                spec = importlib.util.spec_from_file_location("module.name", str("commands/" + command_file))
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)
                await foo.Main(self, message, filename, arguments)
                command_found = True
        if not command_found:
            await message.channel.send("Command not found!")

    async def await_response(self, user):
        def check(message):
            return message.author == user
        try:
            content = await client.wait_for('message', check=check, timeout=100)
        except asyncio.TimeoutError:
            user.send(content="", embed=embedtemplates.failure("Message Timeout", "Bot has timed out while awaiting a response."))
            return None
        return content

    async def on_ready(self):
        print('===| Logged In as {0.user} |==='.format(self))
        activity = discord.Activity(name='for hostiles!', type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)

        self.loop.create_task(await background_tasks.Main(self))

    async def on_guild_join(self, guild):
        with open("json_files/server_settings.json", "r") as file:
            settingstemplate = json.load(file)
        with open("json_files/server_ranks.json", "r") as file:
            rankstemplate = json.load(file)
        self.database.add_ranks(guild.id, rankstemplate)
        self.database.add_settings(guild.id, settingstemplate)

    async def on_raw_reaction_add(self, payload):
        channel = await self.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.fetch_user(payload.user_id)
        emoji = payload.emoji

        if user.bot or message.channel.type == discord.ChannelType.private or message.channel.type == discord.ChannelType.group:
            return

        for reaction_file in os.listdir("reactions"):
            if reaction_file in ["__init__.py", "__pycache__"]:
                continue
            else:
                spec = importlib.util.spec_from_file_location("module.name", str("reactions/" + reaction_file))
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)
                await foo.Main(self, channel, message, user, emoji)

    async def on_member_join(self, user):
        if user.bot:
            return
        embed = discord.Embed(title="Welcome!", colour=discord.Colour(0xff3333),
                              description=str("Welcome to the server " + user.name + ". Please make sure you do >profile_register to gain access to the full server."),
                              timestamp=datetime.datetime.now())
        embed.set_footer(text="Arma3Bot by Ramiris#5376",
                         icon_url="https://cdn.discordapp.com/attachments/743445776491085855/795774307249946644/PFP2.png")
        await user.send(content="", embed=embed)

    async def on_member_remove(self, user):
        print(user.display_name, " Has left.")

    async def on_error(self, event, *args, **kwargs):
        type, value, tb = sys.exc_info()
        if event == "on_message":
            try:
                channel = " in #" + args[0].channel.name
            except AttributeError:
                channel = " in private DMs"
            await args[0].channel.send(
                "*An error occured, sorry for the inconvenience. Ramiris has been notified of the error.*")
        else:
            channel = ""
        tbs = "*" + type.__name__ + " exception handled in " + event + channel + " : " + str(
            value) + "*\n\n```\n"
        for string in traceback.format_tb(tb):
            tbs = tbs + string
        tbs = tbs + "```"
        print(tbs)
        await self.get_user(110838934644211712).send(tbs)

    async def on_message(self, message):
        if message.author.bot or message.channel.type == discord.ChannelType.private or message.channel.type == discord.ChannelType.group:
            return

        for module_file in os.listdir("modules"):
            if module_file in ["__init__.py", "__pycache__"]:
                continue
            else:
                spec = importlib.util.spec_from_file_location("module.name", str("modules/" + module_file))
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)
                await foo.Main(self, message)

        if message.content.startswith(">"):
            command = message.content[1:].split(" ")[0]
            arguments = message.content[1:].replace(str(command+" "), "")
            await self.run_file(command, message, arguments)


if __name__ == '__main__':  # https://discord.com/oauth2/authorize?client_id=792538125196197940&scope=bot&permissions=8
    print("Bot Starting...")
    intents = discord.Intents.default()
    intents.members = True
    client = DiscordBot(intents=intents)
    with open("token.txt", "r") as file:
        token = file.readlines()
    client.run(token[0])
