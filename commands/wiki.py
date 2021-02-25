async def Main(self, message, command, arguments):
    pages = {
        "repo": "https://github.com/SirChopwood/Arma-3-Bot",
        "application": "https://github.com/SirChopwood/Arma-3-Bot/wiki/Applications",
        "loa": "https://github.com/SirChopwood/Arma-3-Bot/wiki/LOAs-(Leave-of-Absence)",
        "rank": "https://github.com/SirChopwood/Arma-3-Bot/wiki/Rank-Commands-&-Formatting#commands",
        "format": "https://github.com/SirChopwood/Arma-3-Bot/wiki/Rank-Commands-&-Formatting#formatting",
        "section": "https://github.com/SirChopwood/Arma-3-Bot/wiki/Section-Commands",
        "setup": "https://github.com/SirChopwood/Arma-3-Bot/wiki/Setup",
        "suggestion": "https://github.com/SirChopwood/Arma-3-Bot/wiki/Suggestions"
    }

    page_found = False
    for page_key in pages.keys():
        if page_key in message.content:
            await message.channel.send(pages[page_key])
            page_found = True
            break

    if page_found:
        return
    else:
        await message.channel.send("https://github.com/SirChopwood/Arma-3-Bot/wiki")
