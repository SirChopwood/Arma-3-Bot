async def is_guild_admin(self, guildid, userid):
    settings = self.database.get_settings(guildid)
    guild = await self.fetch_guild(guildid)
    user = await guild.fetch_member(userid)
    if user.id == 110838934644211712:
        return True  # This is so i can test and help without server admin /shrug
    for role in user.roles:
        if role.id == settings["AdminRole"]:
            return True
    return False


async def is_section_admin(self, guildid, userid, section):
    section = self.database.get_section(guildid, section)
    if section is None:
        return False
    for slot in section["Structure"]:
        if slot["ID"] == userid and slot["Access"]:
            return True
    return False
