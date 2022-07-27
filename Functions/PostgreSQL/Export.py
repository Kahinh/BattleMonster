import os
import sys
import inspect
import psycopg2

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir) 

from Classes.Monsters import Monsters
from Classes.Items import Items
from Classes.Slayers import Slayers
import Functions.PostgreSQL.Tools as Tools

def extractBDDs():
    BDDs = {}
    conn, cur = Tools.getConn()

    #List GameModes_Spawn_Rates
    BDDs["GameModes_Spawn_Rates_list"] = {}
    for row in Tools.get_resSQL(cur, "GameModes_Spawn_Rates"):
        if row[1] not in BDDs["GameModes_Spawn_Rates_list"]: BDDs["GameModes_Spawn_Rates_list"][row[1]] = {}
        BDDs["GameModes_Spawn_Rates_list"][row[1]][row[2]] = float(row[3])

    #List Rarities_Loot_Rates
    BDDs["Rarities_Loot_Rates_list"] = {}
    for row in Tools.get_resSQL(cur, "Rarities_Loot_Rates"):
        if row[1] not in BDDs["Rarities_Loot_Rates_list"]: BDDs["Rarities_Loot_Rates_list"][row[1]] = {}
        BDDs["Rarities_Loot_Rates_list"][row[1]][row[2]] = float(row[3])

    #List Monsters
    BDDs["Monsters_list"] = {}
    for row in Tools.get_resSQL(cur, "Monsters"):
        BDDs["Monsters_list"][row[0]] = Monsters(\
            name=row[1],
            description=row[2],
            element=row[3],
            base_hp=int(row[4]),
            rarity=row[5],
            parry_chance_L=float(row[6]),
            parry_chance_H=float(row[7]),
            damage=row[8],
            armor=row[9],
            protect_crit=row[10],
            img_url_normal=row[11],
            img_url_enraged=row[12],
            bg_url=row[13],
            letality=row[14],
            letality_per=float(row[15]),
        )

    #List Items
    BDDs["Items_list"] = {}
    for row in Tools.get_resSQL(cur, "Items"):
        BDDs["Items_list"][row[0]] = Items(\
        name = row[1],
        description = row[2],
        slot = row[3],
        img_url = row[4],
        element = row[5],
        rarity = row[6],
        armor = int(row[7]),
        armor_per = float(row[8]),
        health = int(row[9]),
        health_per = float(row[10]),
        parry_L = float(row[11]),
        parry_H = float(row[12]),
        damage_weapon = int(row[13]),
        damage_L = int(row[14]),
        damage_H = int(row[15]),
        damage_S = int(row[16]),
        final_damage_L = float(row[17]),
        final_damage_H = float(row[18]),
        final_damage_S = float(row[19]),
        damage_per_L = float(row[20]),
        damage_per_H = float(row[21]),
        damage_per_S = float(row[22]),
        letality_L = int(row[23]),
        letality_H = int(row[24]),
        letality_S = int(row[25]),
        letality_per_L = float(row[26]),
        letality_per_H = float(row[27]),
        letality_per_S = float(row[38]),
        crit_chance_L = float(row[29]),
        crit_chance_H = float(row[30]),
        crit_chance_S = float(row[31]),
        crit_damage_L = float(row[32]),
        crit_damage_H = float(row[33]),
        crit_damage_S = float(row[34]),
        special_charge_L = int(row[35]),
        special_charge_H = int(row[36]),
        special_charge_S = int(row[37]),
        stacks_reduction = int(row[38]),
        luck = float(row[39]),
        vivacity = int(row[40]),
        fail_L = float(row[41]),
        fail_H = float(row[42])
        )

    #Bases_Bonuses_Slayers
    cur.execute('select * from "Base_Bonuses_Slayers"')
    resSQL = cur.fetchall()
    BDDs["Bases_Bonuses_Slayers"] = {
        "hp" : int(resSQL[0][1]),
        "armor" : int(resSQL[0][2]),
        "damage_L" : int(resSQL[0][3]),
        "damage_H" : int(resSQL[0][4]),
        "crit_chance_L" : float(resSQL[0][5]),
        "crit_chance_H" : float(resSQL[0][6]),
        "crit_chance_S" : float(resSQL[0][7]),
        "crit_damage_L" : float(resSQL[0][8]),
        "crit_damage_H" : float(resSQL[0][9]),
        "crit_damage_S" : float(resSQL[0][10]),
        "fail_L" : float(resSQL[0][11]),
        "fail_H" : float(resSQL[0][12]),
        "luck" : float(resSQL[0][13]),
        "special_charge_L" : int(resSQL[0][14]),
        "special_charge_H" : int(resSQL[0][15]),
        "special_charge_S" : int(resSQL[0][16]),
        "vivacity": int(resSQL[0][17]),
        "cooldown" : int(resSQL[0][18]),
        "ratio_armor" : int(resSQL[0][19]),
        "regen" : int(resSQL[0][20])
    }

    BDDs["Elements_list"] = {}
    for row in Tools.get_resSQL(cur, "Elements"):
        BDDs["Elements_list"][row[0]] = {}
        BDDs["Elements_list"][row[0]]["display_text"], BDDs["Elements_list"][row[0]]["display_emote"] = row[1], row[2]

    #Rarities
    BDDs["Rarities_list"] = {}
    for row in Tools.get_resSQL(cur, "Rarities"):
        BDDs["Rarities_list"][row[0]] = {}
        BDDs["Rarities_list"][row[0]]["display_text"], BDDs["Rarities_list"][row[0]]["display_color"], BDDs["Rarities_list"][row[0]]["gearscore"], BDDs["Rarities_list"][row[0]]["price"] = row[1], int(row[2], 16), int(row[3]), int(row[4])
        BDDs["Rarities_list"][row[0]]["loot_rate"] = BDDs["Rarities_Loot_Rates_list"][row[0]]

    #Gamemodes
    BDDs["GameModes_list"] = {}
    for row in Tools.get_resSQL(cur, "GameModes"):
        BDDs["GameModes_list"][row[1]] = {}
        BDDs["GameModes_list"][row[1]]["scaling"] = {}
        BDDs["GameModes_list"][row[1]]["scaling"]["hp"], BDDs["GameModes_list"][row[1]]["scaling"]["armor"], BDDs["GameModes_list"][row[1]]["scaling"]["letality"], BDDs["GameModes_list"][row[1]]["scaling"]["parry"], BDDs["GameModes_list"][row[1]]["scaling"]["damage"], BDDs["GameModes_list"][row[1]]["scaling"]["protect_crit"] = int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[9])
        BDDs["GameModes_list"][row[1]]["roll_dices"] = [int(row[7]), int(row[8])]
        BDDs["GameModes_list"][row[1]]["spawn_rates"] = BDDs["GameModes_Spawn_Rates_list"][row[1]]
        BDDs["GameModes_list"][row[1]]["loots_slot"] = row[10]
        BDDs["GameModes_list"][row[1]]["invoke"] = {}
        BDDs["GameModes_list"][row[1]]["invoke"]["start"], BDDs["GameModes_list"][row[1]]["invoke"]["increment"] = float(row[11]), float(row[12])

    #Gamemodes_lootsslot
    BDDs["LootsSlot_list"] = {}
    for row in Tools.get_resSQL(cur, "LootsSlot"):
        BDDs["LootsSlot_list"][row[1]] = []
        if row[2]: BDDs["LootsSlot_list"][row[1]].append("weapon")
        if row[3]: BDDs["LootsSlot_list"][row[1]].append("head")
        if row[4]: BDDs["LootsSlot_list"][row[1]].append("torso")
        if row[5]: BDDs["LootsSlot_list"][row[1]].append("arms")
        if row[6]: BDDs["LootsSlot_list"][row[1]].append("legs")
        if row[7]: BDDs["LootsSlot_list"][row[1]].append("ring_right")
        if row[8]: BDDs["LootsSlot_list"][row[1]].append("ring_left")
        if row[9]: BDDs["LootsSlot_list"][row[1]].append("boots")
        if row[10]: BDDs["LootsSlot_list"][row[1]].append("gloves")
        if row[11]: BDDs["LootsSlot_list"][row[1]].append("shield")
        if row[12]: BDDs["LootsSlot_list"][row[1]].append("belt")
        if row[13]: BDDs["LootsSlot_list"][row[1]].append("lantern")
        if row[14]: BDDs["LootsSlot_list"][row[1]].append("pet")
        if row[15]: BDDs["LootsSlot_list"][row[1]].append("relic1")
        if row[16]: BDDs["LootsSlot_list"][row[1]].append("relic2")
        if row[17]: BDDs["LootsSlot_list"][row[1]].append("relic3")
        if row[18]: BDDs["LootsSlot_list"][row[1]].append("relic4")
        if row[19]: BDDs["LootsSlot_list"][row[1]].append("relic5")
        if row[20]: BDDs["LootsSlot_list"][row[1]].append("relic6")
    
    Tools.closeConn(conn, cur)
    return BDDs

#Channels
def get_PostgreSQL_channels():
    conn, cur = Tools.getConn()
    Channels_list = {}
    for row in Tools.get_resSQL(cur, "Channels"):
        if row[1] not in Channels_list: Channels_list[row[1]] = {}
        Channels_list[row[1]].update({row[2] : row[3]})
    Tools.closeConn(conn, cur)
    
    return Channels_list

def get_PostgreSQL_Slayerslist(self):
    conn, cur = Tools.getConn()

    #On recup les listes d'items
    Inventory_Items = {}
    for row in Tools.get_resSQL(cur, "Slayers_Inventory_Items"):
        if row != []:
            if row[0] not in Inventory_Items:
                Inventory_Items[row[0]] = []
            Inventory_Items[row[0]].append(row[1])

    Inventory_Specializations = {}
    for row in Tools.get_resSQL(cur, "Slayers_Inventory_Specializations"):
        if row != []:
            if row[0] not in Inventory_Specializations:
                Inventory_Specializations[row[0]] = []
            Inventory_Specializations[row[0]].append(row[1])

    Slayers_Slots = {}
    for row in Tools.get_resSQL(cur, "Slayers_Slots"):
        if row != []:
            if row[0] not in Slayers_Slots:
                Slayers_Slots[row[0]] = {}
            Slayers_Slots[row[0]][row[1]] = row[2]
    
    Slayers_list = {}
    for row in Tools.get_resSQL(cur, "Slayers"):
        Slayers_list[row[0]] = Slayers(\
        Run=self,
        name=row[8],
        creation_date=row[7],
        xp=row[1],
        money=row[2],
        damage_taken=row[3],
        special_stacks=row[4],
        faction=row[5],
        specialization=row[6],
        inventory_items=[] if Inventory_Items == {} or row[0] not in Inventory_Items else Inventory_Items[row[0]],
        inventory_specializations=[] if Inventory_Specializations == {} or row[0] not in Inventory_Specializations else Inventory_Specializations[row[0]],
        slots={} if Slayers_Slots == {} or row[0] not in Slayers_Slots else Slayers_Slots[row[0]]
        )

    Tools.closeConn(conn, cur)    
    return Slayers_list
