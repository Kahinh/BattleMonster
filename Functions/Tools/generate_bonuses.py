def get_bonuses(bot, dict_data, level=1, max_level=1):
    bonuses = {}
    for statistic in bot.Statistics:
        for sub_division in bot.Statistics[statistic].sub_division():
            bonuses.update({sub_division: float(dict_data.get(sub_division, 0)) / max_level * level})
    return bonuses

def add_bonuses(bot, dict_data_1, dict_data_2):
    bonuses = {}
    for statistic in bot.Statistics:
        for sub_division in bot.Statistics[statistic].sub_division():
            bonuses.update({sub_division: float(dict_data_1.get(sub_division, 0)) + float(dict_data_2.get(sub_division, 0))})
    return bonuses

def remove_bonuses(bot, dict_data_1, dict_data_2):
    bonuses = {}
    for statistic in bot.Statistics:
        for sub_division in bot.Statistics[statistic].sub_division():
            bonuses.update({sub_division: float(dict_data_1.get(sub_division, 0)) - float(dict_data_2.get(sub_division, 0))})
    return bonuses

def cap_min_max_bonus(bonus, stat, bot, cSpe):
    if "_" in bonus[-2:]: bonus = bonus[:-2]
    if bot.Statistics[bonus].cap_min is not None:
        stat = float(max(cSpe.adapt_min(bot.Statistics[bonus].cap_min, bonus, stat), stat))
    if bot.Statistics[bonus].cap_max is not None:
        stat = float(min(cSpe.adapt_max(bot.Statistics[bonus].cap_max, bonus, stat), stat))
    return stat