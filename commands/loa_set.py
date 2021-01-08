import importlib.util


async def Main(self, message, command, arguments):
    settings = self.database.get_settings(message.guild.id)
    settings["LOAChannels"].append(message.channel.id)
    self.database.set_settings(message.guild.id, settings)

    spec = importlib.util.spec_from_file_location("module.name", str("commands/loa_header.py"))
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    await foo.Main(self, message, command, arguments)
