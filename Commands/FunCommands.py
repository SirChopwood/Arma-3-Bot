import asyncio
import CreateEmbed
import ConfigHandler
import discord


async def Main(self, message, Config):
    if message.content.startswith(">execute"):
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
            test = message.mentions[0]
        except IndexError:
            await message.channel.send("ERROR! No User provided...")
            return

        if message.mentions[0]:
            newmessage = await message.channel.send(str("***" + str(message.mentions[
                                                                        0].display_name) + " is about to be executed by " + message.author.display_name + "...***"))
            await newmessage.add_reaction("⚠")
            await asyncio.sleep(2)

            def check(reaction, user):
                if reaction.emoji == "765631116647464970" and user == message.mentions[
                    0] and reaction.message.id == newmessage.id:
                    raise InterruptedError
                elif reaction.emoji == "765631116647464970" and user != message.mentions[
                    0] and reaction.message.id == newmessage.id:
                    raise TypeError
                else:
                    print(reaction.emoji == "765631116647464970", user == message.mentions[0],
                          reaction.message.id == newmessage.id)

            try:
                await self.wait_for('reaction_add', timeout=1.0, check=check)
            except asyncio.TimeoutError:
                await newmessage.delete()
                await message.channel.send(str("***" + str(message.mentions[
                                                               0].display_name) + " was just executed by " + message.author.display_name + " in the name of The Emperor!***" + "\nhttps://media.tenor.com/images/b08d0c2008c7a78134f50914e0ae965e/tenor.gif"))
                await message.delete()
            except InterruptedError:
                await message.channel.send(str("***" + str(message.mentions[
                                                               0].display_name) + " was about to be executed by " + message.author.display_name + ", but gracefully dodged it just in time!***"))
                await message.delete()
            except RuntimeError:
                await message.channel.send(str("***" + str(message.mentions[
                                                               0].display_name) + " was about to be executed by " + message.author.display_name + ", but was shoved out the way just in time!***"))
                await message.delete()
