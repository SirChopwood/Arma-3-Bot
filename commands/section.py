import embedtemplates
import discord
import datetime


async def Main(self, message, command, arguments):
    if arguments == 0 or arguments == "" or arguments is None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Displays a section from the ORBAT."))
        return
    section = self.database.get_section(message.guild.id, arguments)
    if section is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Section Not Found", "Please make sure you properly spell the section name, it is case sensetive!"))
        return
    else:
        colour = discord.colour.Colour(int("0x" + section["Colour"], 16))
        embed = discord.Embed(title=section["Name"], colour=colour, timestamp=datetime.datetime.now())
        embed.set_footer(text="Arma3Bot by Ramiris#5376",
                         icon_url="https://cdn.discordapp.com/attachments/743445776491085855/795774307249946644/PFP2.png")
        embed.set_thumbnail(url=section["Logo"])

        ranks = self.database.get_ranks(message.guild.id)

        for role in section["Structure"]:
            if role["Access"]:
                name = str("**__" + str(role["Role"]) + "__**")
            else:
                name = str("**" + str(role["Role"]) + "**")
            if role["ID"] != 0:
                user = self.get_user(role["ID"])
                embed.add_field(name=name, value=str("<:GreyTick:743466991981167138> " + user.display_name), inline=False)
            else:
                embed.add_field(name=name, value="*-Closed-*", inline=False)

        await message.channel.send(content="", embed=embed)
