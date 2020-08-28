import asyncio
import sys
import discord
import ImageManipulation


async def Main(self, message, Config):
    if message.content.startswith(">broadcast") and message.author.id == 110838934644211712:
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
