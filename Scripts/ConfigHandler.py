import json
import pymongo

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
