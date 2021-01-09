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
        else:
            return
        self.announcement_queue.put({"GuildID": message.guild.id, "AnnouncementID": message.id, "UserID": user.id, "Status":status})