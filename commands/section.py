import embedtemplates
import discord
import datetime


async def Main(self, message, command, arguments, page=0, edit=False):
    if arguments == 0 or arguments == "" or arguments is None or arguments == command:
        await message.channel.send(content="", embed=embedtemplates.help(
            "Displays a section from the ORBAT."))
        return
    section = self.database.get_section(message.guild.id, arguments)
    if section is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Section Not Found", "Please make sure you properly spell the section name, it is case sensetive!"))
        return
    else:
        settings = self.database.get_settings(message.guild.id)
        announcement = self.database.get_announcement(message.guild.id, settings["ActiveAnnouncements"][page])

        colour = discord.colour.Colour(int("0x" + section["Colour"], 16))
        embed = discord.Embed(title=str("Section - " + section["Name"]), colour=colour, timestamp=datetime.datetime.now(), description=str("*OPERATION: "+announcement["Operation"]["Title"]+"*"))
        embed.set_thumbnail(url=section["Logo"])
        embed.set_footer(text=str(page))

        for role in section["Structure"]:
            if role["Access"]:
                name = str("**__" + str(role["Role"]) + "__**")
            else:
                name = str("**" + str(role["Role"]) + "**")
            if role["ID"] != 0:
                user = self.get_user(role["ID"])
                if role["ID"] in announcement["Attendance"]["Yes"]:
                    embed.add_field(name=name, value=str("<:GreenTick:743466991771451394> " + user.display_name), inline=False)
                elif role["ID"] in announcement["Attendance"]["Late"]:
                    embed.add_field(name=name, value=str("<:YellowTick:783840786999279619> " + user.display_name), inline=False)
                elif role["ID"] in announcement["Attendance"]["No"]:
                    embed.add_field(name=name, value=str("<:RedTick:743466992144744468> " + user.display_name), inline=False)
                elif role["ID"] in announcement["Attendance"]["LOA"]:
                    embed.add_field(name=name, value=str("<:PurpleTick:796199276853723146> " + user.display_name), inline=False)
                elif role["ID"] in announcement["Attendance"]["Maybe"]:
                    embed.add_field(name=name, value=str("<:BlueTick:783838821681987594> " + user.display_name), inline=False)
                else:
                    embed.add_field(name=name, value=str("<:GreyTick:743466991981167138> " + user.display_name),
                                        inline=False)
            else:
                embed.add_field(name=name, value="*-Closed-*", inline=False)

        if edit:
            newmessage = message
            await message.clear_reactions()
            await message.edit(content="", embed=embed)
        else:
            newmessage = await message.channel.send(content="", embed=embed)
            await message.delete()
        if page > 0:
            await newmessage.add_reaction("<:LeftTick:797270413368492046>")
        if page < (len(settings["ActiveAnnouncements"])-1):
            await newmessage.add_reaction("<:RightTick:797270413607567360>")
