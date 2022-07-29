import random
import datetime
import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from Classes.Specialization import Specializations
from Classes.Items import Item

class Slayer:
    def __init__(
        self,
        Run, 
        name,
        creation_date=datetime.datetime.timestamp(datetime.datetime.now()),
        xp=0,
        money=10,
        damage_taken=0,
        special_stacks=20,
        faction=0,
        specialization=1,
        inventory_items=[],
        inventory_specializations=[1],
        slots={}
        ):
        self.Main = Run
        self.name = name
        self.creation_date = creation_date
        self.xp = xp
        self.damage_taken = damage_taken
        self.money = money
        self.special_stacks = special_stacks
        self.faction = faction
        self.specialization = specialization
        self.inventory_items = inventory_items
        self.inventory_specializations = inventory_specializations
        self.slots = slots

    def calculateBonuses(self, rBaseBonuses, rItemsSlayer):
        bonuses = {
            "armor" : rBaseBonuses["armor"],
            "armor_per" : 0,
            "health" : rBaseBonuses["hp"],
            "health_per" : 0,
            "parry_L" : 0,
            "parry_H" : 0,
            "fail_L" : rBaseBonuses["fail_L"],
            "fail_H" : rBaseBonuses["fail_H"],
            "damage_weapon" : 0,
            "damage_L" : rBaseBonuses["damage_L"],
            "damage_H" : rBaseBonuses["damage_H"],
            "damage_S" : Specializations[self.specialization].damage,
            "final_damage_L" : 0,
            "final_damage_H" : 0,
            "final_damage_S" : 0,
            "damage_per_L" : 0,
            "damage_per_H" : 0,
            "damage_per_S" : 0,
            "letality_L" : 0,
            "letality_H" : 0,
            "letality_S" : 0,
            "letality_per_L" : 0,
            "letality_per_H" : 0,
            "letality_per_S" : 0,
            "crit_chance_L" : rBaseBonuses["crit_chance_L"],
            "crit_chance_H" : rBaseBonuses["crit_chance_H"],
            "crit_chance_S" : rBaseBonuses["crit_chance_S"],
            "crit_damage_L" : rBaseBonuses["crit_damage_L"],
            "crit_damage_H" : rBaseBonuses["crit_damage_H"],
            "crit_damage_S" : rBaseBonuses["crit_damage_S"],
            "special_charge_L" : rBaseBonuses["special_charge_L"],
            "special_charge_H" : rBaseBonuses["special_charge_H"],
            "special_charge_S" : 0,
            "stacks_reduction" : 0,
            "luck": rBaseBonuses["luck"],
            "vivacity": rBaseBonuses["vivacity"]
        }

        for row in rItemsSlayer:
            cItem = Item(row)
            for bonus in cItem.bonuses:
                bonuses[bonus] += cItem.bonuses[bonus]
        return bonuses

    def calculateStats(self, rBaseBonuses, rItemsSlayer):

        bonuses = self.calculateBonuses(rBaseBonuses, rItemsSlayer)
        stats = {
            "total_armor" : int(bonuses["armor"]*(1+bonuses["armor_per"])),
            "total_max_health" : int(bonuses["health"]*(1+bonuses["health_per"])),
            "total_current_health" : int(bonuses["health"]*(1+bonuses["health_per"])) - self.damage_taken,
            "total_fail_L" : float(min(max(bonuses["fail_L"],0),1)),
            "total_fail_H" : float(min(max(bonuses["fail_H"],0),1)),
            "total_fail_S" : 0,
            "total_parry_L" : float(bonuses["parry_L"]),
            "total_parry_H" : float(bonuses["parry_H"]),
            "total_parry_S" : 0,
            "total_damage_L" : int((bonuses["damage_L"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_L"])),
            "total_damage_H" : int((bonuses["damage_H"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_H"])),
            "total_damage_S" : int((bonuses["damage_S"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_S"])),
            "total_final_damage_L" : float(bonuses["final_damage_L"]),
            "total_final_damage_H" : float(bonuses["final_damage_H"]),
            "total_final_damage_S" : float(bonuses["final_damage_S"]),
            "total_crit_chance_L" : float(min(bonuses["crit_chance_L"],1)),
            "total_crit_chance_H" : float(min(bonuses["crit_chance_H"],1)),
            "total_crit_chance_S" : float(min(bonuses["crit_chance_S"],1)),
            "total_crit_damage_L" : float(bonuses["crit_damage_L"]),
            "total_crit_damage_H" : float(bonuses["crit_damage_H"]),
            "total_crit_damage_S" : float(bonuses["crit_damage_S"]),
            "total_letality_L" : int(bonuses["letality_L"]),
            "total_letality_H" : int(bonuses["letality_H"]),
            "total_letality_S" : int(bonuses["letality_S"]),
            "total_letality_per_L" : float(bonuses["letality_per_L"]),
            "total_letality_per_H" : float(bonuses["letality_per_H"]),
            "total_letality_per_S" : float(bonuses["letality_per_S"]),
            "total_special_charge_L" : int(bonuses["special_charge_L"]),
            "total_special_charge_H" : int(bonuses["special_charge_H"]),
            "total_special_charge_S" : int(bonuses["special_charge_S"]),
            "total_stacks_reduction" : int(bonuses["stacks_reduction"]),
            "total_stacks" : int(max(Specializations[self.specialization].stacks - bonuses["stacks_reduction"], 1)),
            "total_vivacity" : int(bonuses["vivacity"]),
            "total_cooldown" : int(rBaseBonuses["cooldown"] - bonuses["vivacity"]),
            "total_luck" : float(min(max(bonuses["luck"],0),1))
        }
        return stats

    def CalculateDamage(self, Hit, cMonster, rBaseBonuses, rItemsSlayer):

        stats = self.calculateStats(rBaseBonuses, rItemsSlayer)
        #On check si on fail
        isFail = False if Hit == "S" else random.choices(population=[True, False], weights=[stats[f"total_fail_{Hit}"], 1-stats[f"total_fail_{Hit}"]], k=1)[0]
        if isFail:
            Damage = 0
            Stacks_Earned = 0
        else: 
            #On check si on est parrty
            isParry = False if Hit == "S" else random.choices(population=[True, False], weights=[min(max(cMonster.parry[f"parry_chance_{Hit}"] + stats[f"total_parry_{Hit}"], 0),1), 1-min(max(cMonster.parry[f"parry_chance_{Hit}"] + stats[f"total_parry_{Hit}"], 0), 1)], k=1)[0]
            if isParry:
                Damage = -int(min(cMonster.damage * (rBaseBonuses["ratio_armor"]/(rBaseBonuses["ratio_armor"] + (stats["total_armor"] * (1 - cMonster.letality_per) - cMonster.letality))), stats["total_current_health"]))
                Stacks_Earned = 0
                #On subit les dégâts
                self.damage_taken = abs(Damage)
            else:
                #On check si on crit
                isCrit = random.choices(population=[True, False], weights=[float(stats[f"total_crit_chance_{Hit}"]), float(1-stats[f"total_crit_chance_{Hit}"])], k=1)

                #Calcul des dégâts
                Damage = min(int(max((((stats[f"total_damage_{Hit}"]*(1 + (stats[f"total_crit_damage_{Hit}"] if isCrit[0] else 0)) * (1 + stats[f"total_final_damage_{Hit}"]))) - (cMonster.protect_crit if isCrit[0] else 0)), 0)*(rBaseBonuses["ratio_armor"]/(rBaseBonuses["ratio_armor"]+max(((cMonster.armor*(1-stats[f"total_letality_per_{Hit}"]))-stats[f"total_letality_{Hit}"]),0)))), cMonster.base_hp)
                if Hit == "S":
                    Stacks_Earned = -self.special_stacks
                else:
                    Stacks_Earned = min(stats["total_stacks"] - self.special_stacks, stats[f"total_special_charge_{Hit}"])
                self.special_stacks += Stacks_Earned
        
        stats = self.calculateStats(rBaseBonuses, rItemsSlayer)
        return Damage, Stacks_Earned, stats

    def GetLoot(self, element, rBaseBonuses, rItemsSlayer, rRarities_Name, rRarities_Weight):

        stats = self.calculateStats(rBaseBonuses, rItemsSlayer)
        rarity_loot = None

        isLoot = random.choices(population=[True, False], weights=[stats[f"total_luck"], 1-stats[f"total_luck"]], k=1)
        if isLoot[0]:
            rarity_loot = random.choices(population=list(rRarities_Name), weights=list([float(dict(element)['loot_rate']) for element in rRarities_Weight]), k=1)
        
        return rarity_loot, element

    def GetDamage(self, damage):
        self.damage_taken += damage

    def canSpecial(self, rBaseBonuses, rItemsSlayer):
        stats = self.calculateStats(rBaseBonuses, rItemsSlayer)
        if stats["total_stacks"] == self.special_stacks:
            return True
        return False

    def GetGearScore(self):
        pass

    def Regen(self):
        pass




