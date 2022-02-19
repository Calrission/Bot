from BotLogicModule.BotLogic import Logic
from BotUIDrawer.main import Application


class LogicUI:
    def __init__(self, logic: Logic, drawer: Application):
        self.logic = logic
        self.drawer = drawer

        self.drawer.set_click_button(self.click_button_search)
        self.welcome_text()

    def welcome_text(self):
        self.drawer.set_text("Hello World")

    def click_button_search(self, event):
        self.drawer.set_text("Hi from logicUI")

    def validateUserInput(self):
        pass

    def run_app(self):
        self.drawer.run_app()
