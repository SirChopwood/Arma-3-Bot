import discord
import datetime


def success(message_title, message_desc):
    embed = discord.Embed(title=message_title, colour=discord.Colour(0xff2a), description=message_desc,
                          timestamp=datetime.datetime.now())
    embed.set_footer(text="Arma3Bot by Ramiris#5376",
                     icon_url="https://cdn.discordapp.com/attachments/743445776491085855/795774307249946644/PFP2.png")
    return embed


def failure(message_title, message_desc):
    embed = discord.Embed(title=message_title, colour=discord.Colour(0xff001e), description=message_desc,
                          timestamp=datetime.datetime.now())
    embed.set_footer(text="Arma3Bot by Ramiris#5376",
                     icon_url="https://cdn.discordapp.com/attachments/743445776491085855/795774307249946644/PFP2.png")
    return embed


def help(commandlist):
    embed = discord.Embed(title="Command Help", colour=discord.Colour(0x00ffff), description=commandlist,
                          timestamp=datetime.datetime.now())
    embed.set_footer(text="Arma3Bot by Ramiris#5376",
                     icon_url="https://cdn.discordapp.com/attachments/743445776491085855/795774307249946644/PFP2.png")
    return embed


def question(question, username):
    embed = discord.Embed(title=str("Question to " + username), colour=discord.Colour(0xffbb00), description=str(question),
                          timestamp=datetime.datetime.now())
    embed.set_footer(text="Arma3Bot by Ramiris#5376",
                     icon_url="https://cdn.discordapp.com/attachments/743445776491085855/795774307249946644/PFP2.png")
    return embed
