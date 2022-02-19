from Bot.BotLogicModule.BotLogic import Logic

logic = Logic()
variants = logic.get_variants_now_level()
print(variants)
variants = logic.choose_variant_now_level(variants[0])
print(variants)
variants = logic.choose_variant_now_level(variants[0])
print(variants)
print(logic.choose_variant_now_level(variants[1]))
print(logic.back_level())

