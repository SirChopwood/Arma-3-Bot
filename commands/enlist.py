import importlib.util


async def Main(self, message, command, arguments):
    spec = importlib.util.spec_from_file_location("module.name", str("commands/section_slot_assign.py"))
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    await foo.Main(self, message, command, arguments)