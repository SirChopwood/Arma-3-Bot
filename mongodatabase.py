import pymongo
import json


class Main:
    def __init__(self):
        with open("mongo.txt", "r") as file:
            token = file.readlines()
        self.client = pymongo.MongoClient(token)
        self.bot_database = self.client['arma3bot']

    def get_guild_collection(self, guild_id):
        collection = self.bot_database[str(guild_id)]
        return collection

    def get_section(self, guild_id, section_name):
        collection = self.get_guild_collection(guild_id)
        section = collection.find_one({"Type": "Section", "Name": section_name})
        return section

    def get_all_sections(self, guild_id):
        collection = self.get_guild_collection(guild_id)
        sections = collection.find({"Type": "Section"})
        return sections

    def add_section(self, guild_id, section_name):
        collection = self.get_guild_collection(guild_id)
        with open("json_files/section_template.json", "r") as file:
            template = json.load(file)
        template["Name"] = section_name
        collection.insert_one(template)

    def set_section(self, guild_id, section_name, section_data):
        collection = self.get_guild_collection(guild_id)
        status = collection.replace_one({"Type": "Section", "Name": section_name}, section_data)
        if status.modified_count > 0:
            return True
        else:
            return False

    def remove_section(self, guild_id, section_name):
        collection = self.get_guild_collection(guild_id)
        status = collection.delete_one({"Type": "Section", "Name": section_name})
        if status.deleted_count > 0:
            return True
        else:
            return False

    def get_user(self, guild_id, user_id):
        collection = self.get_guild_collection(guild_id)
        user = collection.find_one({"Type": "User", "DiscordID": user_id})
        return user

    def get_users_of_rank(self, guild_id, rank):
        collection = self.get_guild_collection(guild_id)
        user = collection.find({"Type": "User", "Rank": int(rank)})
        return user

    def get_users_over_rank(self, guild_id, rank):
        collection = self.get_guild_collection(guild_id)
        user = collection.find({"Type": "User", "Rank": {"$gt": int(rank)}})
        return user

    def add_user(self, guild_id, user):
        collection = self.get_guild_collection(guild_id)
        collection.insert_one(user)

    def set_user(self, guild_id, user):
        collection = self.get_guild_collection(guild_id)
        collection.replace_one({"Type": "User", "DiscordID": user["DiscordID"]}, user)

    def get_ranks(self, guild_id):
        collection = self.get_guild_collection(guild_id)
        ranks = collection.find_one({"Type": "Ranks"})
        return ranks

    def set_ranks(self, guild_id, ranks):
        collection = self.get_guild_collection(guild_id)
        collection.replace_one({"Type": "Ranks"}, ranks)

    def add_ranks(self, guild_id, ranks):
        collection = self.get_guild_collection(guild_id)
        collection.insert_one(ranks)

    def get_settings(self, guild_id):
        collection = self.get_guild_collection(guild_id)
        settings = collection.find_one({"Type": "Settings"})
        return settings

    def set_settings(self, guild_id, settings):
        collection = self.get_guild_collection(guild_id)
        collection.replace_one({"Type": "Settings"}, settings)

    def add_settings(self, guild_id, settings):
        collection = self.get_guild_collection(guild_id)
        collection.insert_one(settings)

    def get_all_announcements(self, guild_id):
        collection = self.get_guild_collection(guild_id)
        announcements = collection.find({"Type": "Announcement"})
        return announcements

    def get_announcement(self, guild_id, announcement_id):
        collection = self.get_guild_collection(guild_id)
        announcement = collection.find_one({"Type": "Announcement", "MessageID": announcement_id})
        return announcement

    def remove_announcement(self, guild_id, announcement_id):
        collection = self.get_guild_collection(guild_id)
        announcement = collection.delete_one({"Type": "Announcement", "MessageID": announcement_id})
        settings = self.get_settings(guild_id)
        if announcement_id in settings["ActiveAnnouncements"]:
            settings["ActiveAnnouncements"].remove(announcement_id)
            self.set_settings(guild_id, settings)
        if announcement.deleted_count > 0:
            return True
        else:
            return False

    def set_announcement(self, guild_id, announcement):
        collection = self.get_guild_collection(guild_id)
        collection.replace_one({"Type": "Announcement", "MessageID": announcement["MessageID"]}, announcement)

    def add_announcement(self, guild_id, announcement):
        collection = self.get_guild_collection(guild_id)
        collection.insert_one(announcement)
