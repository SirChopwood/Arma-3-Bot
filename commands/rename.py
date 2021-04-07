async def Main(self, message, command, arguments):
    await self.run_file("profile_rename", message, arguments)
