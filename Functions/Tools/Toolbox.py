from typing import KeysView
import lib

def transformRaritiesANDElements(fetch):
    dict_record = {}
    for row in fetch:
        dict_record[list(dict(row).values())[0]] = {}
        for item in list(dict(row).keys())[1:len(list(dict(row).keys()))]:
            dict_record[list(dict(row).values())[0]][item] = row[item]
    return dict_record

def transformSlots(fetch):
    dict_record = {}
    for row in fetch:
        dict_record[list(dict(row).values())[1]] = {}
        for item in list(dict(row).keys())[2:len(list(dict(row).keys()))]:
            dict_record[list(dict(row).values())[1]][item] = row[item]
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

def disable_enable_InventoryView(children, list, index):
    len_list = len(list)
    if index == len_list - 1:
        for item in children:
            if hasattr(item, "label"):
                if item.label==">>":
                    item.disabled = True   
    if index > 0:
        for item in children:
            if hasattr(item, "label"):
                if item.label=="<<":
                    item.disabled = False 
    if index == 0:
        for item in children:
            if hasattr(item, "label"):
                if item.label=="<<":
                    item.disabled = True
    if index < len_list - 1:
        for item in children:
            if hasattr(item, "label"):
                if item.label==">>":
                    item.disabled = False
    for item in children:
        if hasattr(item, "label"):
            if item.label=="Équiper":
                if len(list) > 0 :
                    if list[index].equipped:
                        item.disabled = True
                    else:
                        item.disabled = False

def filter_items_list(items_list, slot=None, element=None, rarity=None):
    filtered_list = []
    for item_id in items_list:
        if (items_list[item_id].slot == slot or slot is None) and (items_list[item_id].element == element or element is None) and (items_list[item_id].rarity == rarity or rarity is None):
            filtered_list.append(items_list[item_id])
    return filtered_list

def get_spe_row_by_id(rSpe, spe_id):
    for row in rSpe:
        if int(row["id"]) == int(spe_id):
            return lib.Spe(row)