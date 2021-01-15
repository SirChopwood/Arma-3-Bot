import importlib.util
import permissions
import embedtemplates


async def Main(self, message, command, arguments):
    if not await permissions.is_guild_admin(self, message.guild.id, message.author.id):
        await message.channel.send(content="", embed=embedtemplates.failure("Permission Denied",
                                                                            "User does not have permission to use this!"))
        return
    settings = self.database.get_settings(message.guild.id)
    settings["SuggestionChannels"].append(message.channel.id)
    self.database.set_settings(message.guild.id, settings)

    spec = importlib.util.spec_from_file_location("module.name", str("commands/suggestion_header.py"))
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    await foo.Main(self, message, command, arguments)
