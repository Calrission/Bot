from LogicUI import LogicUI
from BotLogicModule.BotLogic import Logic
from BotUIDrawer.main import Application

logicUI = LogicUI(Logic(), Application())
logicUI.run_app()
