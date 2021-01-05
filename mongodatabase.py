import pymongo
import json


class Main:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://ReqBotMason:11374265@164.132.200.68:8100/?authSource=admin")
        self.bot_database = self.client['arma3bot']

    def get_guild_collection(self, guild_id):
        collection = self.bot_database[str(guild_id)]
        return collection

    def get_section(self, guild_id, section_name):
        collection = self.get_guild_collection(guild_id)
        section = collection.find_one({"Type": "Section", "Name": section_name})
        return section

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