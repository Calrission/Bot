import json


class ParseJSONData:
    def __init__(self, filepath="BotLogicModule/data.json"):
        self.filepath = filepath

    def decode_local_json(self) -> dict:
        with open(self.filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
