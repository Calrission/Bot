from LogicUI import LogicUI
from BotLogicModule.BotLogic import Logic
from BotUIDrawer.main import Application


if __name__ == "__main__":
    logicUI = LogicUI(Logic(), Application())
    logicUI.run_app()
