import discord
import os
import asyncio
import CreateEmbed
import json
import sys
import ImageManipulation
from urllib.request import urlopen
import RoleCall

global Config

# server = 192.168.0.4:6969 | computer = 192.168.0.30:7000

with open("Config.json", "r") as file:
    Config = json.load(file)


class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue_checker = self.loop.create_task(self.check_time())

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

        with open("Config.json", "r") as file:
            Config = json.load(file)
        if message.id != Config["announcements"]["active"]:
            return
        else:
            found_user = False
            if str(emoji) == "<:GreenTick:743466991771451394>":
                with open("Config.json", "r") as file:
                    Config = json.load(file)
                for section in Config["ORBAT"]:
                    for i in range(len(Config["ORBAT"][section])):
                        role = Config["ORBAT"][section][i]
                        if user.id == role["ID"]:
                            Config["ORBAT"][section][i]["AttendingNextOp"] = True
                            found_user = True
                            json.dump(Config, open("Config.json", "w"))
                            print("User '" + user.name + "' IS Attending!")

            elif str(emoji) == "<:GreyTick:743466991981167138>":
                with open("Config.json", "r") as file:
                    Config = json.load(file)
                for section in Config["ORBAT"]:
                    for i in range(len(Config["ORBAT"][section])):
                        role = Config["ORBAT"][section][i]
                        if user.id == role["ID"]:
                            Config["ORBAT"][section][i]["AttendingNextOp"] = None
                            found_user = True
                            json.dump(Config, open("Config.json", "w"))
                            print("User '" + user.name + "' is UNKNOWN if they are Attending!")

            elif str(emoji) == "<:RedTick:743466992144744468>":
                with open("Config.json", "r") as file:
                    Config = json.load(file)
                for section in Config["ORBAT"]:
                    for i in range(len(Config["ORBAT"][section])):
                        role = Config["ORBAT"][section][i]
                        if user.id == role["ID"]:
                            Config["ORBAT"][section][i]["AttendingNextOp"] = False
                            found_user = True
                            json.dump(Config, open("Config.json", "w"))
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

        with open("Config.json", "r") as file:
            Config = json.load(file)
        # Special Commands

        if message.content.startswith(">help"):
            await message.author.send(content=None, embed=CreateEmbed.command_list())

        elif message.content.startswith(">broadcast") and message.author.id == 110838934644211712:
            channel = self.get_channel(724762259364118539)
            await channel.send(content=message.content[11:])
            await message.delete()

        elif message.content.startswith(">say") and message.author.id == 110838934644211712:
            await message.channel.send(message.content[5:])
            await message.delete()

        elif message.content.startswith(">restart") and message.author.id == 110838934644211712:
            await message.channel.send("Bot will restart in 30 seconds!")
            await asyncio.sleep(1)
            sys.exit(0)

        elif message.content.startswith(">welcome") and message.author.id == 110838934644211712:
            ImageManipulation.welcome_plate(message.author.name)
            await message.channel.send(content="", file=discord.File(Config['welcome message']['final file']))

        elif message.content.startswith(">announce"):
            # Access Checks
            access = False
            if message.author.id == 110838934644211712:
                access = True
            for role in message.author.roles:
                if role.name in Config["mod roles"]:
                    access = True
            if not access:
                return

            # make announcement
            announcement = message.content[10:]
            announcement = announcement.split("|")
            embed = CreateEmbed.announcement(announcement)
            newmsg = await message.channel.send(content=None, embed=embed)
            await newmsg.add_reaction("<:GreenTick:743466991771451394>")
            await newmsg.add_reaction("<:GreyTick:743466991981167138>")
            await newmsg.add_reaction("<:RedTick:743466992144744468>")
            with open("Config.json", "r") as file:
                Config = json.load(file)
                Config["announcements"]["active"] = newmsg.id
                Config["announcements"]["channel"] = message.channel.id
                for Section in Config["ORBAT"]:
                    for x in range(len(Config["ORBAT"][Section])):
                        role = Config["ORBAT"][Section][x]
                        if role["ID"]:
                            Config["ORBAT"][Section][x]["AttendingNextOp"] = None
            json.dump(Config, open("Config.json", "w"))

        elif message.content.startswith(">ORBAT"):
            if len(message.content) == 6:
                # Access Checks
                access = False
                if message.author.id == 110838934644211712:
                    access = True
                for role in message.author.roles:
                    if role.name in Config["mod roles"]:
                        access = True
                if not access:
                    return

                for Section in Config["ORBAT"]:
                    embed = CreateEmbed.ORBAT(Section)
                    await message.channel.send(content="", embed=embed)
                    await asyncio.sleep(.5)
            else:
                embed = CreateEmbed.ORBAT(message.content[7:])
                if embed is None:
                    await message.channel.send("Section not found!")
                else:
                    await message.channel.send(content="", embed=embed)

        elif message.content.startswith(">rolecall"):
            embed = CreateEmbed.rolecall()
            await message.channel.send(content="", embed=embed)

        elif message.content.startswith(">enlist"):
            # Access Checks
            access = False
            if message.author.id == 110838934644211712:
                access = True
            for role in message.author.roles:
                if role.name in Config["mod roles"]:
                    access = True
            if not access:
                return

            async def set_ORBAT_user(message, user, section_text, role_text):
                # Load Config and Verify Answers
                with open("Config.json", "r") as file:
                    Config = json.load(file)

                for x in range(len(Config["ORBAT"][section_text])):
                    Role = Config["ORBAT"][section_text][x]
                    if role_text == Role["Role"] and Role["ID"] is None:
                        # Remove Old Section/Role
                        status = None
                        for Section_Old in Config["ORBAT"]:
                            for i in range(len(Config["ORBAT"][Section_Old])):
                                Role_Old = Config["ORBAT"][Section_Old][i]
                                if Role_Old["ID"] == user.id:
                                    Config["ORBAT"][Section_Old][i]["ID"] = None
                                    Config["ORBAT"][Section_Old][i]["Name"] = ""
                                    status = Config["ORBAT"][Section_Old][i]["AttendingNextOp"]
                                    Config["ORBAT"][Section_Old][i]["AttendingNextOp"] = None
                                    print("User was removed from ", Section_Old, Role_Old)

                        # Set New Section/Role
                        Config["ORBAT"][section_text][x]["ID"] = user.id
                        Config["ORBAT"][section_text][x]["Name"] = user.display_name
                        if status is not None:
                            Config["ORBAT"][section_text][x]["AttendingNextOp"] = status
                        else:
                            Config["ORBAT"][section_text][x]["AttendingNextOp"] = None

                        json.dump(Config, open("Config.json", "w"))

                        await message.channel.send(str(user.mention + " has been enlisted to ``" + section_text + " - " + role_text + "`` by " + message.author.mention))
                        print(str(user.mention + " has been enlisted to ``" + section_text + " - " + role_text + "`` by " + message.author.mention))
                        await message.delete()
                        return True

                await message.channel.send("ERROR! Role Not Found OR All Positions Filled!...")
                return False

            try:
                test = message.mentions[0]
            except IndexError:
                await message.channel.send("ERROR! No User provided...")
                return

            if message.mentions[0]:
                message_split = message.content.split("|")
                print(message_split)
                if len(message_split) == 3:
                    print(message.mentions[0], message_split[1], message_split[2])
                    await set_ORBAT_user(message, message.mentions[0], message_split[1], message_split[2])
                else:
                    # Questions
                    sections = []
                    for Section in Config["ORBAT"]:
                        sections.append(Section)
                    section_question = await message.channel.send(
                        str("What section would you like to enlist them to? \n``" + ', '.join(sections) + "``"))
                    section_answer = await self.make_response_check(message.author)
                    section_text = section_answer.content
                    await section_question.delete()
                    await section_answer.delete()

                    try:
                        test = Config["ORBAT"][section_text]
                    except KeyError:
                        await message.channel.send("ERROR! Section Not Found...")
                        return

                    roles = []
                    for Role in Config["ORBAT"][section_text]:
                        roles.append(Role["Role"])
                    role_question = await message.channel.send(
                        str("What role would you like to enlist them to? \n``" + ', '.join(roles) + "``"))
                    role_answer = await self.make_response_check(message.author)
                    role_text = role_answer.content
                    await role_question.delete()
                    await role_answer.delete()
                    print(message.mentions[0], section_text, role_text)
                    await set_ORBAT_user(message, message.mentions[0], section_text, role_text)

        elif message.content.startswith(">rename"):
            # Load Config
            with open("Config.json", "r") as file:
                Config = json.load(file)

            for Section in Config["ORBAT"]:
                for x in range(len(Config["ORBAT"][Section])):
                    Role = Config["ORBAT"][Section][x]
                    if Role["ID"] == message.author.id:
                        # Set New Section/Role
                        Config["ORBAT"][Section][x]["Name"] = message.author.display_name

                        json.dump(Config, open("Config.json", "w"))

                        await message.channel.send(
                            str(message.author.mention + " has had their name updated in the ORBAT"))
                        await message.delete()
                        return

            await message.channel.send("ERROR! User Not Found in ORBAT...")


with open("Secrets.json", "r") as Secrets:
    Secrets = json.load(Secrets)
client = Bot()
client.run(Secrets["token"])