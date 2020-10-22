import json
import pymongo
import dns


class MongoDataBase:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://ServoSkull:SOPnFduiJ2cqqjFq@cluster0.lg0yx.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.database = self.client['776thCadian']
        self.configs = self.database['Configs']
        self.executions = self.database['Executions']

    def get_config_nosync(self, guildid):
        return self.configs.find_one({"guild_id": guildid})

    def set_config_nosync(self, guildid, config):
        return self.configs.replace_one({"guild_id": guildid}, config)

    async def get_config(self, guildid):
        return self.configs.find_one({"guild_id": guildid})

    async def set_config(self, guildid, config):
        return self.configs.replace_one({"guild_id": guildid}, config)

    async def get_executions(self, guildid):
        return self.executions.find_one({"guild_id": guildid})

    async def set_executions(self, guildid, executions):
        return self.executions.replace_one({"guild_id": guildid}, executions)




def OpenNoSync(guildid):

    filepath = "../ConfigFiles/" + str(guildid) + ".json"
    with open(filepath, "r") as file:
        return json.load(file)


async def Open(guildid):
    filepath = "../ConfigFiles/" + str(guildid) + ".json"
    with open(filepath, "r") as file:
        return json.load(file)


async def Save(data, guildid):
    filepath = "../ConfigFiles/" + str(guildid) + ".json"
    json.dump(data, open(filepath, "w"), indent=2, separators=(',', ': '))


def Secret():
    with open("Secrets.json", "r") as Secrets:
        return json.load(Secrets)
