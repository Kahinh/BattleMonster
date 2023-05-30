from typing import KeysView
import lib

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

def filter_items_list(items_list, slot=None, element=None, rarity=None):
    filtered_list = []
    for id in items_list:
        if (items_list[id].slot == slot or slot is None) and (items_list[id].element == element or element is None) and (items_list[id].rarity == rarity or rarity is None):
            filtered_list.append(items_list[id])
    return filtered_list

def disable_enable_LootReviewView(children, Slayer, id):
    for item in children:
        if hasattr(item, "label"):
            if item.label=="Équiper":
                if Slayer.isEquipped(id):
                    item.disabled = True
                else:
                    item.disabled = False
            if item.label=="Vendre":
                if Slayer.isinInventory(id) == False:
                    item.disabled = True
                else:
                    item.disabled = False