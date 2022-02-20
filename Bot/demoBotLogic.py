from Bot.BotLogicModule.BotLogic import Logic

logic = Logic()
# variants = logic.get_variants_now_level()
# print(variants)
# variants = logic.choose_object_now_level(variants[0])
# print(variants)
# print(logic.choose_object_now_level(variants[0]))
# print(logic.back_level())

while True:
    variants = logic.get_variants_now_level()
    print(variants)
    if type(variants) == list:
        logic.choose_object_now_level(variants[0])
    else:
        logic.back_level()
        print(logic.get_variants_now_level())
        break
