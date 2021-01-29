import permissions

async def Main(self, channel, message, user, emoji):
    if user.bot:
        return
    settings = self.database.get_settings(message.guild.id)
    if message.id in settings["ActiveAnnouncements"]:
        if str(emoji) == "<:GreenTick:743466991771451394>":
            status = "Yes"
        elif str(emoji) == "<:YellowTick:783840786999279619>":
            status = "Late"
        elif str(emoji) == "<:BlueTick:783838821681987594>":
            status = "Maybe"
        elif str(emoji) == "<:RedTick:743466992144744468>":
            status = "No"
        elif "PurpleTick" in str(emoji):
            if await permissions.is_guild_admin(self, message.guild.id, user.id):
                if self.database.remove_announcement(message.guild.id, message.id):
                    await message.delete()
            return
        elif "RightTick" in str(emoji):
            if await permissions.is_guild_admin(self, message.guild.id, user.id):
                for reaction in message.reactions:
                    users = await reaction.users().flatten()
                    if str(reaction.emoji) == "<:GreenTick:743466991771451394>":
                        async for user2 in users:
                            self.announcement_queue.put(
                                {"GuildID": message.guild.id, "AnnouncementID": message.id, "UserID": user2.id,
                                 "Status": "Yes"})
                    elif str(reaction.emoji) == "<:YellowTick:783840786999279619>":
                        async for user2 in users:
                            self.announcement_queue.put(
                            {"GuildID": message.guild.id, "AnnouncementID": message.id, "UserID": user.id,
                             "Status": "Late"})
                    elif str(reaction.emoji) == "<:BlueTick:783838821681987594>":
                        async for user2 in users:
                            self.announcement_queue.put(
                            {"GuildID": message.guild.id, "AnnouncementID": message.id, "UserID": user.id,
                             "Status": "Maybe"})
                    elif str(reaction.emoji) == "<:RedTick:743466992144744468>":
                        async for user2 in users:
                            self.announcement_queue.put(
                            {"GuildID": message.guild.id, "AnnouncementID": message.id, "UserID": user.id,
                             "Status": "No"})

        else:
            return
        self.announcement_queue.put({"GuildID": message.guild.id, "AnnouncementID": message.id, "UserID": user.id, "Status":status})
