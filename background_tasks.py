import asyncio
import datetime
import embedtemplates
import queue


async def Main(self):
    self.announcement_queue = queue.Queue()
    while True:
        try:
            data = self.announcement_queue.get(block=False)
            await self.wait_until_ready()
            announcement = self.database.get_announcement(data["GuildID"], data["AnnouncementID"])
            for status in ["Yes", "No", "LOA", "Late", "Maybe"]:
                for i in range(len(announcement["Attendance"][status])):
                    if announcement["Attendance"][status][i] == data["UserID"]:
                        announcement["Attendance"][status].pop(i)

            announcement["Attendance"][data["Status"]].append(data["UserID"])
            self.database.set_announcement(data["GuildID"], announcement)
        except queue.Empty:
            await asyncio.sleep(0.1)

        for guild in self.guilds:
            for announcement in self.database.get_all_announcements(guild.id):
                now = datetime.datetime.utcnow().replace(second=0, microsecond=0)
                optime = datetime.datetime.strptime(str(
                    announcement["Operation"]["Date"] + " " + announcement["Operation"][
                        "Time"]), '%d/%m/%Y %H:%M')

                if now == (optime - datetime.timedelta(days=1)) and announcement["Reminders"]["24h"] is False:
                    print("One Day before")
                elif now == (optime - datetime.timedelta(hours=1)) and announcement["Reminders"]["1h"] is False:
                    print("One Hour before")
                elif now == (optime - datetime.timedelta(minutes=1)) and announcement["Reminders"]["24h"] is False:
                    print("TEST PRINT")
                    for userid in announcement["Attendance"]["Maybe"]:
                        user = await self.fetch_user(userid)
                        await user.send(content="", embed=embedtemplates.announcement(announcement["Operation"]["Title"],
                                                                                     announcement["Operation"]["Time"],
                                                                                     announcement["Operation"]["Date"],
                                                                                     announcement["Operation"]["Image"],
                                                                                     announcement["Operation"]["Host"]))
                    announcement["Reminders"]["24h"] = True
                    self.database.set_announcement(guild.id, announcement)

        await asyncio.sleep(0.2)