from BotLogicModule.ParseJSONData import ParseJSONData


class Logic:
    def __init__(self):
        self.data = ParseJSONData().decode_local_json()
        self.path_indexes_data = []

    def get_object_from_path(self, path: list) -> dict | str:
        now_object = self.data
        for index in path:
            now_object = now_object[list(now_object.keys())[index]]
        return now_object

    def get_variants_now_level(self) -> list | str:
        now_object = self.get_object_from_path(self.path_indexes_data)
        if isinstance(now_object, dict):
            return list(now_object.keys())
        else:
            now_object: str
            return now_object

    def choose_variant_now_level(self, name_variant: str) -> list | str:
        index_variant = list(self.get_object_from_path(self.path_indexes_data).keys()).index(name_variant)
        self.path_indexes_data.append(index_variant)
        return self.get_variants_now_level()

    def back_level(self):
        del self.path_indexes_data[-1]
        return self.get_variants_now_level()
