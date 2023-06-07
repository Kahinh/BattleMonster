def get_bonuses(bot, dict_data, level=1, max_level=1):
    bonuses = {}
    for statistic in bot.Statistics:
        for sub_division in bot.Statistics[statistic].sub_division():
            bonuses.update({sub_division: float(dict_data.get(sub_division, 0))})
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

def cap_min_max_stats(bot, dict_data, cSpe):
    for _, cStatistic in bot.Statistics.items():
        for sub_division in cStatistic.sub_division():
            if cStatistic.cap_min is not None:
                dict_data[sub_division] = max(cSpe.adapt_min(cStatistic.cap_min, cStatistic.name, dict_data), dict_data[sub_division])
            if cStatistic.cap_max is not None:
                dict_data[sub_division] = min(cSpe.adapt_max(cStatistic.cap_max, cStatistic.name, dict_data), dict_data[sub_division])
    return dict_data