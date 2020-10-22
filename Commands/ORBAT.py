import asyncio
import CreateEmbed
import ConfigHandler


async def Main(self, message, Config):
    if message.content.startswith(">announce"):
        # Access Checks
        access = False
        if message.author.id == 110838934644211712:
            access = True
        for role in message.author.roles:
            if role.name in Config["mod roles"]:
                access = True
        if not access:
            return
        if message.channel.id != Config["announcements"]["channel"]:
            message.channel.send("Warning - Announcement created in a new channel.")

        # make announcement
        announcement = message.content[10:]
        announcement = announcement.split("|")
        embed = CreateEmbed.announcement(announcement)
        newmsg = await message.channel.send(content=None, embed=embed)
        await newmsg.add_reaction("<:GreenTick:743466991771451394>")
        await newmsg.add_reaction("<:GreyTick:743466991981167138>")
        await newmsg.add_reaction("<:RedTick:743466992144744468>")
        Config["announcements"]["active"] = newmsg.id
        Config["announcements"]["channel"] = message.channel.id
        for Section in Config["ORBAT"]:
            for x in range(len(Config["ORBAT"][Section])):
                role = Config["ORBAT"][Section][x]
                if role["ID"]:
                    Config["ORBAT"][Section][x]["AttendingNextOp"] = None
        await self.mongo.set_config(guildid=message.guild.id, config=Config)

    elif message.content.startswith(">edit"):
        channel = await self.fetch_channel(Config["announcements"]["channel"])
        message = await channel.fetch_message(Config["announcements"]["active"])
        announcement = message.content[10:]
        announcement = announcement.split("|")
        embed = CreateEmbed.announcement(announcement)
        await message.edit(content=None, embed=embed)

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
                embed = CreateEmbed.ORBAT(Section, Config)
                await message.channel.send(content="", embed=embed)
                await asyncio.sleep(.5)
        else:
            embed = CreateEmbed.ORBAT(message.content[7:], Config)
            if embed is None:
                await message.channel.send("Section not found!")
            else:
                await message.channel.send(content="", embed=embed)

    elif message.content.startswith(">rolecall"):
        embed = CreateEmbed.rolecall(Config)
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

        async def set_ORBAT_user(message, user, section_text, role_text, Config):
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

                    await self.mongo.set_config(guildid=message.guild.id, config=Config)

                    await message.channel.send(str(
                        user.mention + " has been enlisted to ``" + section_text + " - " + role_text + "`` by " + message.author.mention))
                    print(str(
                        user.mention + " has been enlisted to ``" + section_text + " - " + role_text + "`` by " + message.author.mention))
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
                await set_ORBAT_user(message, message.mentions[0], message_split[1], message_split[2], Config)
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
                await set_ORBAT_user(message, message.mentions[0], section_text, role_text, Config)

    elif message.content.startswith(">discharge"):
        # Access Checks
        access = False
        if message.author.id == 110838934644211712:
            access = True
        for role in message.author.roles:
            if role.name in Config["mod roles"]:
                access = True
        if not access:
            return

        try:
            user = message.mentions[0]
        except IndexError:
            await message.channel.send("No user found, please Ping an active ORBAT user after the command.")
            return

        for Section_Old in Config["ORBAT"]:
            for i in range(len(Config["ORBAT"][Section_Old])):
                Role_Old = Config["ORBAT"][Section_Old][i]
                if Role_Old["ID"] == user.id:
                    Config["ORBAT"][Section_Old][i]["ID"] = None
                    Config["ORBAT"][Section_Old][i]["Name"] = ""
                    Config["ORBAT"][Section_Old][i]["AttendingNextOp"] = None
                    print("User was removed from ", Section_Old, Role_Old)

        await self.mongo.set_config(guildid=message.guild.id, config=Config)

        await message.channel.send(str(
            user.mention + " has been discharged from the unit by " + message.author.mention))
        print(str(
            user.mention + " has been discharged from the unit by " + message.author.mention))
        await message.delete()

    elif message.content.startswith(">rename"):
        # Load Config
        for Section in Config["ORBAT"]:
            for x in range(len(Config["ORBAT"][Section])):
                Role = Config["ORBAT"][Section][x]
                if Role["ID"] == message.author.id:
                    # Set New Section/Role
                    Config["ORBAT"][Section][x]["Name"] = message.author.display_name

                    await self.mongo.set_config(guildid=message.guild.id, config=Config)

                    await message.channel.send(
                        str(message.author.mention + " has had their name updated in the ORBAT"))
                    await message.delete()
                    return

        await message.channel.send("ERROR! User Not Found in ORBAT...")

    elif message.content.startswith(">display"):
        # Access Checks
        access = False
        if message.author.id == 110838934644211712:
            access = True
        for role in message.author.roles:
            if role.name in Config["mod roles"]:
                access = True
        if not access:
            return

        messagelist = {}
        for Section in Config["ORBAT"]:
            embed = CreateEmbed.ORBAT(Section, Config)
            newmessage = await message.channel.send(content="", embed=embed)
            messagelist[str(Section)] = newmessage.id
            await asyncio.sleep(.5)

        Config["announcements"]["displaymessages"] = messagelist
        Config["announcements"]["displaychannel"] = message.channel.id
        await self.mongo.set_config(guildid=message.guild.id, config=Config)