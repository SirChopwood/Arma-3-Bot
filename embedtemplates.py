import discord
import datetime


def success(message_title, message_desc):
    embed = discord.Embed(title=str("<:GreenTick:743466991771451394> "+message_title), colour=discord.Colour(0xff2a), description=message_desc,
                          timestamp=datetime.datetime.now())
    return embed


def failure(message_title, message_desc):
    embed = discord.Embed(title=str("<:RedTick:743466992144744468> "+message_title), colour=discord.Colour(0xff001e), description=message_desc,
                          timestamp=datetime.datetime.now())
    return embed


def help(commandlist):
    embed = discord.Embed(title="<:BlueTick:783838821681987594> Command Help", colour=discord.Colour(0x00ffff), description=commandlist,
                          timestamp=datetime.datetime.now())
    embed.set_footer(text="Arma3Bot by Ramiris#5376",
                     icon_url="https://cdn.discordapp.com/attachments/743445776491085855/795774307249946644/PFP2.png")
    return embed


def question(question, username):
    embed = discord.Embed(title=str("<:YellowTick:783840786999279619> Question to " + username), colour=discord.Colour(0xffbb00), description=str(question),
                          timestamp=datetime.datetime.now())
    return embed


def profile(self, guild_id, author):
    embed = discord.Embed(title=str(author.name + "'s Profile"), colour=author.colour, timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=author.avatar_url)
    user = self.database.get_user(guild_id, author.id)
    ranks = self.database.get_ranks(guild_id)

    if user == None:
        return None

    for key in user:
        if key in ["_id", "Type"]:
            continue
        if key == "Rank":
            value = str(str(user[key]) + " - " + ranks["Dictionary"][user[key]]["Long"])
            embed.add_field(name=key, value=value, inline=False)
        else:
            embed.add_field(name=key, value=str(user[key]), inline=False)
    return embed


def suggestion(text, name=""):
    embed = discord.Embed(title="Suggestion: " + name, colour=discord.Colour(0xffbb00), description=text,
                          timestamp=datetime.datetime.now())
    return embed


def loa(startdate, enddate, reason, user):
    embed = discord.Embed(title="<:PurpleCross:796199276853723146> Leave of Absence: " + user.display_name, colour=discord.Colour(0x6f00ff),
                          timestamp=datetime.datetime.now())
    if startdate:
        embed.add_field(name="Start", value=startdate, inline=True)
    if enddate:
        embed.add_field(name="End", value=enddate, inline=True)
    if reason:
        embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    return embed


def loa_header(text):
    embed = discord.Embed(title="<:PurpleCross:796199276853723146> Leave of Absence", colour=discord.Colour(0x6f00ff), description=text,
                          timestamp=datetime.datetime.now())
    return embed
