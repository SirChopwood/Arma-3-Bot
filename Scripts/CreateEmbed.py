import discord
import datetime
import json
import ConfigHandler


# Generic Bot Embed Formats
def command_list(Config):
    embed = discord.Embed(title=str("What I do..."), colour=852223,
                          timestamp=datetime.datetime.now())

    embed.set_author(name="Servo Skull 0776-1058-5391-1A",
                     icon_url="https://cdn.discordapp.com/attachments/743445776491085855/743449150065999912/PFP.jpg")
    embed.set_footer(text="Servo Skull 0776-1058-5391-1A",
                     icon_url="https://cdn.discordapp.com/attachments/743445776491085855/743449150065999912/PFP.jpg")

    embed.add_field(name="**__Commands__**",
                    value="*These are special commands that can be called by stating their name.*",
                    inline=False)

    for command in Config["special commands"]:
        embed.add_field(name=str("**" + command["command"] + "**"), value=str("```" + command["response"] + "```"),
                        inline=False)

    return embed


# RoleCall
def ORBAT(section, Config):
    if section not in Config["ORBAT"]:
        return None
    embed = discord.Embed(title=str("776th ORBAT - " + section), colour=852223)

    checked_in = 0
    filled_slots = 0
    for role in Config["ORBAT"][section]:
        if role["ID"]:
            filled_slots += 1
            if role["AttendingNextOp"] is None:
                embed.add_field(name=str("**" + role["Role"] + "**"),
                                value=str("<:GreyTick:743466991981167138> " + role["Name"]),
                                inline=False)
            elif role["AttendingNextOp"] is True:
                embed.add_field(name=str("**" + role["Role"] + "**"),
                                value=str("<:GreenTick:743466991771451394> " + role["Name"]),
                                inline=False)
                checked_in += 1
            elif role["AttendingNextOp"] is False:
                embed.add_field(name=str("**" + role["Role"] + "**"),
                                value=str("<:RedTick:743466992144744468> " + role["Name"]),
                                inline=False)
                checked_in += 1

        else:
            embed.add_field(name=str("**" + role["Role"] + "**"), value=str("*-CLOSED-*"), inline=False)
        embed.set_footer(text=str(str(checked_in) + " / " + str(filled_slots) + " Checked In"))
    return embed


def rolecall(Config):
    embed = discord.Embed(title=str("776th Role Call"), colour=852223)

    total_filled_slots = 0
    total_checked_in = 0
    for Section in Config["ORBAT"]:
        checked_in = 0
        filled_slots = 0
        attending = 0
        not_attending = 0
        for role in Config["ORBAT"][Section]:
            if role["ID"]:
                filled_slots += 1
                if role["AttendingNextOp"] is True:
                    attending += 1
                    checked_in += 1
                elif role["AttendingNextOp"] is False:
                    not_attending += 1
                    checked_in += 1
        total_checked_in += checked_in
        total_filled_slots += filled_slots
        embed.add_field(name=Section, value=str(
            "<:GreenTick:743466991771451394> " + str(attending) + "  <:GreyTick:743466991981167138> " + str(
                filled_slots - checked_in) + "  <:RedTick:743466992144744468> " + str(not_attending)), inline=False)
    embed.set_footer(text=str(str(total_checked_in) + " / " + str(total_filled_slots) + " Checked In (Total)"))
    return embed


def announcement(data):
    embed = discord.Embed(title=str("776th Operation Announcement"), colour=852223)
    embed.add_field(name="Operation Name:", value=data[0], inline=False)
    embed.add_field(name="Time/Date:", value=data[1], inline=False)
    embed.set_footer(text="Please react below for roll call.")
    return embed
