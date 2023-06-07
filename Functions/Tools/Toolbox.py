from typing import KeysView
import lib

def transformChannels(fetch):
    dict_record = {}
    for row in fetch:
        dict_record[row["name"]] = {}
        dict_record[row["name"]] = row["channel_id"]
    return dict_record

def disable_enable_LootReviewView(children, cSlayer, id):
    for item in children:
        if hasattr(item, "label"):
            if item.label=="Équiper":
                if cSlayer.isEquipped(id):
                    item.disabled = True
                else:
                    item.disabled = False
            if item.label=="Vendre":
                if cSlayer.isinInventory(id) == False:
                    item.disabled = True
                else:
                    item.disabled = False