from enum import Enum

from BotLogicModule.BotLogic import Logic
from BotUIDrawer.main import Application


class LogicUI:
    def __init__(self, logic: Logic, drawer: Application):
        self.logic = logic
        self.drawer = drawer
        self.now_choose_variants = None

        self.drawer.set_click_button(self.click_button_search)
        self.welcome()

    def welcome(self):
        self.drawer.set_text("Здравствуйте, я бот секретарь. Я помогу вам узнать про школу №15. Давайте же начнем. "
                             "Введите /start")
        self.drawer.set_image(CharacterIMG.WELCOME.src())

    def click_button_search(self, event):
        text = self.drawer.get_text_user_input()

        if text == "/start":
            variants = self.logic.get_variants_now_level()
            self.drawer.show_choose_variants(variants)
            self.drawer.set_image(CharacterIMG.DEFAULT.src())
            return

        if text.isnumeric() and (self.now_choose_variants is not None and text in self.now_choose_variants):
            return

        self.drawer.set_text("Я не понял. Повторите.")
        self.drawer.set_image(CharacterIMG.ANSWER.src())

    def run_app(self):
        self.drawer.run_app()


class CharacterIMG(Enum):
    PATH = "media_files/"
    WELCOME = "face2"
    DEFAULT = "face1"
    ANSWER = "face3"
    THING = "face2"

    def __init__(self, src):
        self.src = src

    def src(self) -> str:
        return self.PATH.value() + self.src
