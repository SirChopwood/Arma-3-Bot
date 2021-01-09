import queue
import asyncio


async def Main(self):
    self.announcement_queue = queue.Queue()
    while True:
        try:
            data = self.announcement_queue.get(block=False)
        except queue.Empty:
            await asyncio.sleep(1)
            continue
        await self.wait_until_ready()
        announcement = self.database.get_announcement(data["GuildID"], data["AnnouncementID"])
        for status in ["Yes", "No", "LOA", "Late", "Maybe"]:
            for i in range(len(announcement["Attendance"][status])):
                if announcement["Attendance"][status][i] == data["UserID"]:
                    announcement["Attendance"][status].pop(i)

        announcement["Attendance"][data["Status"]].append(data["UserID"])
        self.database.set_announcement(data["GuildID"], announcement)
        await asyncio.sleep(0.2)
