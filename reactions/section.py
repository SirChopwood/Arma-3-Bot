import embedtemplates
import discord
import importlib.util


async def Main(self, channel, message, user, emoji):
    if len(message.embeds) == 1:
        title = str(message.embeds[0].title)
        if title.startswith("Section"):
            title = message.embeds[0].title
            title = title.replace("Section - ", "")
            page = int(message.embeds[0].footer.text)
            if str(emoji) == "<:RightTick:797270413607567360>":
                page += 1
            elif str(emoji) == "<:LeftTick:797270413368492046>":
                page -= 1
            spec = importlib.util.spec_from_file_location("module.name", str("commands/section.py"))
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            await foo.Main(self, message, "", title, page, True)
