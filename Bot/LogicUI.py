from enum import Enum
from BotLogicModule.BotLogic import Logic
from BotUIDrawer.main import Application
import pathlib
from pathlib import Path


class LogicUI:
    def __init__(self, logic: Logic, drawer: Application):
        self.commands = {"/start": self.start, "/welcome": self.welcome, "/back": self.back, "/help": self.help,
                         "/variants": self.variants_, "/clear": self.clear}
        self.logic = logic
        self.drawer = drawer
        self.variants = []
        self.welcome()
        self.drawer.set_click_button(self.click_button_search)

    def welcome(self, **kwargs):
        self.drawer.set_image(CharacterIMG.WELCOME.src)
        self.drawer.set_new_text_output(
            "Здравствуйте, я бот секретарь. Я помогу вам узнать про школу №15 с УИОП г. Электросталь. Давайте же "
            "начнем.\nВведите /start для того чтобы начать.\nВведите /help для получения помощи.")
        self.drawer.new_buttons(self.commands)

    def back(self, **kwargs):
        if len(self.logic.path_indexes_data) == 0:
            self.drawer.set_text_output("Назад пути нет !")
            self.drawer.set_image(CharacterIMG.QUITE.src)
            return
        self.variants = self.logic.back_level()
        self.drawer.show_choose_variants(self.variants)
        self.add_variants_and_command_to_button()
        self.drawer.set_image(CharacterIMG.DEFAULT.src)

    def help(self, **kwargs):
        help_text = "Список команд:\n" \
                    "/start - возвращает в начало пирамиды\n" \
                    "/variants - показывает варианты перехода по пирамиде\n" \
                    "/back - возвращает назад по пирамиде\n" \
                    "/clear - очищает поле вывода\n" \
                    "/welcome - показывает приветственный текст"
        self.drawer.set_new_text_output(help_text)
        self.drawer.set_image_gif(CharacterIMG.ANIMATION_FACE.src)

    def start(self, **kwargs):
        self.logic.path_indexes_data = []
        self.variants = self.logic.get_variants_now_level()
        self.add_variants_and_command_to_button()
        self.drawer.show_choose_variants(self.variants)
        self.drawer.set_image(CharacterIMG.DEFAULT.src)

    def clear(self, **kwargs):
        self.drawer.clear_text_output()

    def variants_(self, **kwargs):
        self.variants = self.logic.get_variants_now_level()
        if type(self.variants) == list:
            self.drawer.show_choose_variants(self.variants)
            self.drawer.set_image(CharacterIMG.DEFAULT.src)
            self.add_variants_and_command_to_button()
        elif type(self.variants) == str:
            self.drawer.set_text_output("Извините, но для текущей позиции нету вариантов переходов по пирамиде.")
            self.drawer.set_image(CharacterIMG.QUITE.src)

    def parse_now_variants_to_buttons_dict(self) -> dict:
        return {i: self.select_variant for i in self.variants}

    def add_variants_and_command_to_button(self):
        self.drawer.new_buttons(self.parse_now_variants_to_buttons_dict())
        self.drawer.add_buttons(self.commands)

    def select_variant(self, name_variant: str):
        self.variants = self.logic.choose_object_now_level(name_variant)
        if type(self.variants) == list:
            self.drawer.show_choose_variants(self.variants)
            self.add_variants_and_command_to_button()
        elif type(self.variants) == str:
            self.drawer.show_object_variant(self.variants)
            self.drawer.new_buttons(self.commands)
            self.drawer.set_image(CharacterIMG.ANSWER.src)

    def click_button_search(self, _):
        text = self.drawer.get_text_user_input().strip()
        self.drawer.clear_text_user_input()

        if text == "/start":
            self.start()
            return

        if (text.isnumeric() or text in self.variants) and type(self.variants) == list and len(self.variants) > 0:
            if text.isnumeric() and (0 >= int(text) or int(text) > len(self.variants)):
                self.drawer.set_text_output("Такого пункта в списке вариантов нет !")
                self.drawer.set_image(CharacterIMG.QUITE.src)
                return
            name_variant = self.variants[int(text) - 1] if text.isnumeric() else text
            self.select_variant(name_variant)
            self.drawer.set_image(CharacterIMG.DEFAULT.src)
            return

        if text == "/back":
            self.back()
            return

        if text == "/help":
            self.help()
            return

        if text == "/welcome":
            self.welcome()
            return

        if text == "/clear":
            self.clear()
            return

        if text == "/variants":
            self.variants_()
            return

        self.drawer.set_text_output("Я не понял. Повторите.")
        self.drawer.set_image(CharacterIMG.QUITE.src)

    def run_app(self):
        self.drawer.run_app()


class CharacterIMG(Enum):
    WELCOME = "face2.png"
    DEFAULT = "face1.png"
    ANSWER = "face3.png"
    THING = "face2.png"
    QUITE = "face4.png"
    ICON = "icon.png"
    ICON_ISO = "icon.ico"
    ANIMATION_FACE = "animation_face.gif"

    def __init__(self, filename):
        self.filename = filename
        self.main_path = "media_files"

    @property
    def src(self) -> str:
        return str(Path(pathlib.Path.cwd(), self.main_path, self.filename))
