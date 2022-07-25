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
from gitignore import postgresql


#Si on est en local (Donc en prod)
#conn = psycopg2.connect('dbname')
conn = psycopg2.connect(f'host={postgresql.host} user={postgresql.user} password={postgresql.password} dbname={postgresql.dbname}')
cur = conn.cursor()

#List Behemoths
cur.execute('select * from "Monsters"')
resSQL = cur.fetchall()

Monsters_list = {}
for row in resSQL:
    Monsters_list[row[0]] = Monsters(\
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
cur.execute('select * from "Items"')
resSQL = cur.fetchall()

Items_list = {}
for row in resSQL:
    Items_list[row[0]] = Items(\
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
Bases_Bonuses_Slayers = {
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
    "ratio_armor" : int(resSQL[0][19])
}

#Elements
cur.execute('select * from "Elements"')
resSQL = cur.fetchall()

Elements_list = {}
for row in resSQL:
    Elements_list[row[0]] = {}
    Elements_list[row[0]]["display_text"], Elements_list[row[0]]["display_emote"] = row[1], row[2]

#Rarities
cur.execute('select * from "Rarities"')
resSQL = cur.fetchall()

Rarities_list = {}
for row in resSQL:
    Rarities_list[row[0]] = {}
    Rarities_list[row[0]]["display_text"], Rarities_list[row[0]]["display_color"] = row[1], int(row[2], 16)
    Rarities_list[row[0]]["loot_rate"] = {}
    Rarities_list[row[0]]["loot_rate"]["common"], Rarities_list[row[0]]["loot_rate"]["rare"], Rarities_list[row[0]]["loot_rate"]["epic"], Rarities_list[row[0]]["loot_rate"]["legendary"] = float(row[3]), float(row[4]), float(row[5]), float(row[6])