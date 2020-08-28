import json


def OpenNoSync():
    with open("Config.json", "r") as file:
        return json.load(file)


async def Open():
    with open("Config.json", "r") as file:
        return json.load(file)


async def Save(data):
    json.dump(data, open("Config.json", "w"), indent=2, separators=(',', ': '))


def Secret():
    with open("Secrets.json", "r") as Secrets:
        return json.load(Secrets)
