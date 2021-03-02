import asyncio
import datetime
import embedtemplates
import queue
import discord


async def Main(self):
    self.announcement_queue = queue.Queue()
    while True:
        try:
            data = self.announcement_queue.get(block=False)
            await self.wait_until_ready()
            announcement = self.database.get_announcement(data["GuildID"], data["AnnouncementID"])
            for status in ["Yes", "No", "LOA", "Late", "Maybe"]:
                for i in range(len(announcement["Attendance"][status])):
                    try:
                        announcement["Attendance"][status].remove(data["UserID"])
                    except ValueError:
                        continue
            announcement["Attendance"][data["Status"]].append(data["UserID"])
            self.database.set_announcement(data["GuildID"], announcement)
        except queue.Empty:
            await asyncio.sleep(0.1)

        for guild in self.guilds:
            for announcement in self.database.get_all_announcements(guild.id):
                settings = self.database.get_settings(guild.id)

                now = datetime.datetime.utcnow().replace(second=0, microsecond=0)
                optime = datetime.datetime.strptime(str(
                    announcement["Operation"]["Date"] + " " + announcement["Operation"][
                        "Time"]), '%d/%m/%Y %H:%M')

                if now >= optime and announcement["MessageID"] in settings["ActiveAnnouncements"]:
                    settings["ActiveAnnouncements"].remove(announcement["MessageID"])
                    self.database.set_settings(guild.id, settings)
                    continue

                try:
                    if not settings["OpReminders"]:
                        continue
                except KeyError:
                    continue

                if now == (optime - datetime.timedelta(days=1)) and announcement["Reminders"]["24h"] is False:  # 24h
                    for section in self.database.get_all_sections(guild.id):
                        for slot in section["Structure"]:
                            if slot["ID"] == 0:
                                continue
                            reacted = False
                            user = await self.fetch_user(slot["ID"])
                            for status in ["Yes", "No", "LOA", "Late", "Maybe"]:
                                if user.id in announcement["Attendance"][status]:
                                    reacted = True

                            if reacted:
                                continue
                            else:
                                try:
                                    await user.send(content="",
                                                    embed=embedtemplates.announcement_reminder(
                                                        announcement["Operation"]["Title"],
                                                        announcement["Operation"]["Time"],
                                                        announcement["Operation"]["Date"],
                                                        announcement["Operation"]["Image"],
                                                        announcement["Operation"]["Host"]))
                                except discord.Forbidden:
                                    print(user.name, "Could not be messaged.")

                    announcement["Reminders"]["24h"] = True
                    self.database.set_announcement(guild.id, announcement)

                elif now == (optime - datetime.timedelta(hours=1)) and announcement["Reminders"]["1h"] is False:  # 1h
                    for userid in announcement["Attendance"]["Maybe"]:
                        user = await self.fetch_user(userid)
                        try:
                            await user.send(content="",
                                            embed=embedtemplates.announcement_reminder(
                                                announcement["Operation"]["Title"],
                                                announcement["Operation"]["Time"],
                                                announcement["Operation"]["Date"],
                                                announcement["Operation"]["Image"],
                                                announcement["Operation"]["Host"]))
                        except discord.Forbidden:
                            print(user.name, "Could not be messaged.")
                    announcement["Reminders"]["1h"] = True
                    self.database.set_announcement(guild.id, announcement)

        await asyncio.sleep(0.2)
