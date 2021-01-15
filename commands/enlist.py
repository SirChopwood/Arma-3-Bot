async def Main(self, message, command, arguments):
    await self.run_file("section_slot_assign", message, arguments)
