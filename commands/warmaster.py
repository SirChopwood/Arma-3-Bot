import discord


async def Main(self, message, command, arguments):
    embed = discord.Embed(title="For the Warmaster!", colour=discord.Colour(0x9400D3), description="Nice Cock!")
    embed.set_image(url="https://cdn.discordapp.com/attachments/792427557294178325/801961285528453120/Nice_Saint.png")
    await message.channel.send(content="", embed=embed)
