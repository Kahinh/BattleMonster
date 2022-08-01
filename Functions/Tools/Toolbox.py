def transformRaritiesANDElements(fetch):
    dict_record = {}
    for row in fetch:
        dict_record[list(dict(row).values())[0]] = {}
        for item in list(dict(row).keys())[1:len(list(dict(row).keys()))]:
            dict_record[list(dict(row).values())[0]][item] = row[item]
    return dict_record

def transformChannels(fetch):
    dict_record = {}
    for row in fetch:
        dict_record[row["name"]] = {}
        dict_record[row["name"]] = row["channel_id"]
    return dict_record

def transformGamemodesLootSlot(fetch):
    dict_record = {}
    for row in fetch:
        if row["gamemode"] not in dict_record:
            dict_record[row["gamemode"]] = []
        dict_record[row["gamemode"]].append(row["slot"])
    return dict_record

def transformGamemodesSpawnRate(fetch):
    dict_record = {}
    for row in fetch:
        if row["gamemode_name"] not in dict_record:
            dict_record[row["gamemode_name"]] = {}
        dict_record[row["gamemode_name"]][row["rarities"]] = float(row["spawn_rate"])
    return dict_record

def transformRaritiesLootRate(fetch):
    dict_record = {}
    for row in fetch:
        if row["rarities_name"] not in dict_record:
            dict_record[row["rarities_name"]] = {}
        dict_record[row["rarities_name"]][row["rarities"]] = float(row["loot_rate"])
    return dict_record