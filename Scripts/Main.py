# Import Libraries
import discord
import asyncio
import CreateEmbed
import ImageManipulation
import ConfigHandler

# Import Commmands
import Administration
import ORBAT

global Config

Config = ConfigHandler.OpenNoSync()


class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('\n\n\nWe have logged in as {0.user}'.format(self))
        illya = self.get_user(110838934644211712)
        await illya.send("Bot Restarted")
        activity = discord.Activity(name='for heretics!!', type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)
        # await self.get_channel(Config["announcements"]["channel"]).fetch_message(Config["announcements"]["active"])

    async def check_time(self):
        await self.wait_until_ready()

        # do action here

        await asyncio.sleep(1)

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
            Config = await ConfigHandler.Open()
            for section in Config["ORBAT"]:
                for i in range(len(Config["ORBAT"][section])):
                    role = Config["ORBAT"][section][i]
                    if user.id == role["ID"]:
                        Config["ORBAT"][section][i]["AttendingNextOp"] = status
                        found_user = True
                        await ConfigHandler.Save(Config)
                        displaychannel = await self.fetch_channel(Config["announcements"]["displaychannel"])
                        displaymessage = await displaychannel.fetch_message(Config["announcements"]["displaymessages"][str(section)])
                        embed = CreateEmbed.ORBAT(section)
                        await displaymessage.edit(content=None, embed=embed)
            return found_user

        Config = await ConfigHandler.Open()

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
        ImageManipulation.welcome_plate(user.name)
        channel = self.get_channel(Config["welcome message"]["channel"])
        await channel.send(content="", file=discord.File(Config['welcome message']['final file']))

    async def on_message(self, message):
        if message.author.bot:
            return

        Config = await ConfigHandler.Open()

        if message.content.startswith(">help"):
            await message.author.send(content=None, embed=CreateEmbed.command_list())

        await Administration.Main(self, message, Config)
        await ORBAT.Main(self, message, Config)


Secrets = ConfigHandler.Secret()
client = Bot()
client.run(Secrets["token"])
