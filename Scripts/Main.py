# Import Libraries
import discord
import asyncio
import CreateEmbed
import ImageManipulation
import ConfigHandler
import datetime

# Import Commmands
import sys

sys.path.insert(0, '../Commands')
import Administration
import ORBAT
import FunCommands


class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo = ConfigHandler.MongoDataBase()

    async def on_ready(self):
        print('===| Logged In as {0.user} |==='.format(self))
        activity = discord.Activity(name='for heretics!!', type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)

    # async def on_resumed(self):
        # print('===| Connection Resumed as {0.user} at {1} |==='.format(self, str(datetime.datetime.now())))

    # async def on_disconnect(self):
        # print('>>> Connection Lost at {0} <<<'.format(str(datetime.datetime.now())))

    async def make_response_check(self, user):
        def check(message):
            return message.author == user

        try:
            content = await client.wait_for('message', check=check, timeout=100)
        except asyncio.TimeoutError:
            print("User didnt respond")

        return content

    async def on_raw_reaction_add(self, payload):
        channel = await self.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.fetch_user(payload.user_id)
        emoji = payload.emoji

        async def set_status(self, status):
            found_user = False
            Config = await self.mongo.get_config(guildid=message.guild.id)
            for section in Config["ORBAT"]:
                for i in range(len(Config["ORBAT"][section])):
                    role = Config["ORBAT"][section][i]
                    if user.id == role["ID"]:
                        Config["ORBAT"][section][i]["AttendingNextOp"] = status
                        found_user = True
                        await self.mongo.set_config(guildid=message.guild.id, config=Config)
                        displaychannel = await self.fetch_channel(Config["announcements"]["displaychannel"])
                        displaymessage = await displaychannel.fetch_message(
                            Config["announcements"]["displaymessages"][str(section)])
                        embed = CreateEmbed.ORBAT(section, Config)
                        await displaymessage.edit(content=None, embed=embed)
            return found_user

        Config = await self.mongo.get_config(guildid=message.guild.id)

        if message.id != Config["announcements"]["active"]:
            return
        else:
            found_user = False
            if str(emoji) == "<:GreenTick:743466991771451394>":
                found_user = await set_status(self, True)
                print("User '" + user.name + "' IS Attending!")

            elif str(emoji) == "<:GreyTick:743466991981167138>":
                found_user = await set_status(self, None)
                print("User '" + user.name + "' is UNKNOWN if they are Attending!")

            elif str(emoji) == "<:RedTick:743466992144744468>":
                found_user = await set_status(self, False)
                print("User '" + user.name + "' is NOT Attending!")

            if not found_user:
                print("User '" + user.name + "' Is not assigned a Section and Role!")

    async def on_member_join(self, user):
        Config = await self.mongo.get_config(guildid=user.guild.id)
        ImageManipulation.welcome_plate(user.name, Config)
        channel = self.get_channel(Config["welcome message"]["channel"])
        await channel.send(content="", file=discord.File(Config['welcome message']['final file']))

    async def on_member_remove(self, user):
        Config = await self.mongo.get_config(guildid=user.guild.id)
        for Section in Config["ORBAT"]:
            for x in range(len(Config["ORBAT"][Section])):
                Role = Config["ORBAT"][Section][x]
                if Role["ID"] == user.id:
                    # Set New Section/Role
                    Config["ORBAT"][Section][x]["Name"] = ""
                    Config["ORBAT"][Section][x]["ID"] = None
                    Config["ORBAT"][Section][x]["AttendingNextOp"] = None
                    print(str(user.display_name) + " has left " + str(user.guild.name) + " while on the ORBAT.")
                    await self.mongo.set_config(guildid=user.guild.id, config=Config)

    async def on_message(self, message):
        if message.author.bot:
            return

        Config = await self.mongo.get_config(guildid=message.guild.id)

        if message.content.startswith(">help"):
            await message.author.send(content=None, embed=CreateEmbed.command_list(Config))

        await Administration.Main(self, message, Config)
        await ORBAT.Main(self, message, Config)
        await FunCommands.Main(self, message, Config)


Secrets = ConfigHandler.Secret()
client = Bot()
client.run(Secrets["token"])
