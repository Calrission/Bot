import json

"""
Класс логики бота. Служить для перемещения по дереву (json файлу). В self два параметра: data - словарь с объектами; 
path_indexes_data - текущий путь выбранного объекта.
by Струков Артемий
created 19/02/2022
"""


class Logic:
    def __init__(self):
        self.data: dict = ParseJSONData().decode_local_json()
        self.path_indexes_data: list = []

    def get_object_from_path(self, path: list) -> dict | str:
        """
        :return: объект находящийся по этому пути (dict или str)

        :param: path - лист index в json файле (путь до объекта)
        """
        now_object = self.data
        for index in path:
            now_object = now_object[list(now_object.keys())[index]]
        return now_object

    def get_variants_now_level(self) -> list | str:
        """
        :return: список всех подобъектов текущего объекта (если dict) или его значение (если str)
        """
        now_object = self.get_object_from_path(self.path_indexes_data)
        if isinstance(now_object, dict):
            return list(now_object.keys())
        else:
            now_object: str
            return now_object

    def choose_object_now_level(self, name_object: str) -> list | str:
        """
        Перейди к этому объекту (изменив путь выбранного объекта)

        :param: name_object - название объекта

        :return: список всех подобъектов выбранного объекта (если dict) или его значение (если str)
        """
        index_variant = list(self.get_object_from_path(self.path_indexes_data).keys()).index(name_object)
        self.path_indexes_data.append(index_variant)
        return self.get_variants_now_level()

    def back_level(self) -> list | str:
        """
        Перейди к предпоследнему объекту в пути (изменив сам путь выбранного объекта)

        :return: список всех подобъектов выбранного объекта (если dict) или его значение (если str)
        """
        del self.path_indexes_data[-1]
        return self.get_variants_now_level()


class ParseJSONData:
    def __init__(self, filepath="BotLogicModule/data.json"):
        self.filepath = filepath

    def decode_local_json(self) -> dict:
        with open(self.filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
