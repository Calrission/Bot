from enum import Enum
from BotLogicModule.BotLogic import Logic
from BotUIDrawer.main import Application
from BotVoiceModule.BotVoiceReader import VoiceReader
import pathlib
import Levenshtein
from pathlib import Path


class LogicUI:
    def __init__(self, logic: Logic, drawer: Application):
        self.commands = ["/start", "/welcome", "/back", "/help",
                         "/variants", "/clear", "/voice"]
        self.logic = logic
        self.drawer = drawer
        self.voice = VoiceReader()
        self.variants = []
        self.welcome()
        self.drawer.set_click_button_search(self.click_button_search)
        self.drawer.set_click_button_voice(self.click_button_voice)

    def welcome(self):
        self.drawer.set_image(CharacterIMG.WELCOME.src)
        self.drawer.set_new_text_output(
            "Здравствуйте, я бот-секретарь. Я помогу вам узнать о школе №15 с УИОП г. Электросталь. Давайте же "
            "начнем.\nВведите /start для того чтобы начать.\nВведите /help для получения помощи.")
        self.drawer.new_buttons(self.commands, self.click_button_variants)

    def back(self):
        if len(self.logic.path_indexes_data) == 0:
            self.drawer.set_text_output("Назад пути нет !")
            self.drawer.set_image(CharacterIMG.QUITE.src)
            return
        self.variants = self.logic.back_level()
        self.drawer.show_choose_variants(self.variants)
        self.add_variants_and_command_to_button()
        self.drawer.set_image(CharacterIMG.DEFAULT.src)

    def help(self):
        help_text = "Список команд:\n" \
                    "/start (/старт) - возвращает в начало пирамиды\n" \
                    "/variants (/варианты) - показывает варианты перехода по пирамиде\n" \
                    "/back (/назад) - возвращает назад по пирамиде\n" \
                    "/clear (/очистка) - очищает поле вывода\n" \
                    "/welcome - показывает приветственный текст\n" \
                    "/voice - переключение режима голосового ввода\n\n" \
                    "В скобках указана команды для голосового ввода (они также начинаются со слова 'слэш')"
        self.drawer.set_new_text_output(help_text)
        self.drawer.set_image_gif(CharacterIMG.ANIMATION_FACE.src)

    def start(self):
        self.logic.path_indexes_data = []
        self.variants = self.logic.get_variants_now_level()
        self.add_variants_and_command_to_button()
        self.drawer.show_choose_variants(self.variants)
        self.drawer.set_image(CharacterIMG.DEFAULT.src)

    def clear(self):
        self.drawer.clear_text_output()

    def variants_(self):
        self.variants = self.logic.get_variants_now_level()
        if type(self.variants) == list:
            self.drawer.show_choose_variants(self.variants)
            self.drawer.set_image(CharacterIMG.DEFAULT.src)
            self.add_variants_and_command_to_button()
        elif type(self.variants) == str:
            self.drawer.set_text_output("Извините, но для текущей позиции нету вариантов переходов по пирамиде.")
            self.drawer.set_image(CharacterIMG.QUITE.src)

    def parse_now_variants_to_buttons_dict(self) -> list:
        return self.variants

    def add_variants_and_command_to_button(self):
        self.drawer.new_buttons(self.parse_now_variants_to_buttons_dict(), self.click_button_variants)
        self.drawer.add_buttons(self.commands, self.click_button_variants)

    def select_variant(self, name_variant: str):
        self.variants = self.logic.choose_object_now_level(name_variant)
        if type(self.variants) == list:
            self.drawer.show_choose_variants(self.variants)
            self.add_variants_and_command_to_button()
            self.drawer.set_image(CharacterIMG.DEFAULT.src)
        elif type(self.variants) == str:
            self.drawer.show_object_variant(self.variants)
            self.drawer.new_buttons(self.commands, self.click_button_variants)
            self.drawer.set_image(CharacterIMG.ANSWER.src)

    def click_button_variants(self, name_variant: str):
        self.parse_text_input_user(name_variant)

    def parse_text_input_user(self, text: str):
        if text == "/start":
            self.start()
            return

        if (text.isnumeric() or text.capitalize() in self.variants) and \
                type(self.variants) == list and len(self.variants) > 0:
            if text.isnumeric() and (0 >= int(text) or int(text) > len(self.variants)):
                self.drawer.set_text_output("Такого пункта в списке вариантов нет !")
                self.drawer.set_image(CharacterIMG.QUITE.src)
                return
            name_variant = self.variants[int(text) - 1] if text.isnumeric() else text.capitalize()
            self.select_variant(name_variant)
            return

        if text == "/back":
            self.back()
            return

        if text == "/help" or text == "/":
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

        if text == "/voice":
            self.click_button_voice(None)
            return

        near_words = self.near_words(text, (self.variants if type(self.variants) == list else []) + self.commands)
        if len(near_words) == 0:
            self.drawer.set_text_output("Я не понял. Повторите.")
        else:
            str_near_words = "\n".join(near_words)
            self.drawer.set_text_output(
                f"Я вас не понял. Вы ввели '{text}'. Возможно вы хотели ввести:\n{str_near_words}")
        self.drawer.set_image(CharacterIMG.QUITE.src)

    def click_button_search(self, _):
        text = self.drawer.get_text_user_input().strip()
        self.drawer.clear_text_user_input()
        self.parse_text_input_user(text)

    @staticmethod
    def near_words(word: str, variants_words: list[str]) -> list[str]:
        return [i[0] for i in list(filter(lambda x: 0 <= x[1] <= 3,
                                          [(v_word, Levenshtein.distance(word, v_word)) for v_word in
                                           variants_words]))]

    def parse_voice_text(self, text: str):
        commands_rus_end = {"/старт": "/start", "/очистка": "/clear", "/варианты": "/variants", "/назад": "/back"}
        if "слэш" in text:
            text = text.replace("слэш ", "/") if "слэш " in text else text.replace("слэш", "/")
            if text in commands_rus_end:
                text = text.replace(text, commands_rus_end[text])
        if text == "хватит":
            self.click_button_voice(None)
        elif text != "":
            self.drawer.set_new_text_user_input(text)

    def click_button_voice(self, _):
        self.voice_()

    def voice_(self):
        if not self.voice.is_activ():
            self.drawer.set_text_output("Голосовой ввод включен, скажите 'хватит' для отключения")
            self.voice.start(self.parse_voice_text)
        else:
            self.drawer.set_text_output("Голосовой ввод выключен")
            self.voice.stop()

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
