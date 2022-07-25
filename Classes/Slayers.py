import random
import datetime
import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from Functions.PostgreSQL.Functions import Items_list
from Classes.Specialization import Specializations_list
from Functions.PostgreSQL.Functions import Bases_Bonuses_Slayers

class Slayers:
    def __init__(
        self, 
        name,
        creation_date=datetime.datetime.timestamp(datetime.datetime.now()),
        xp=0,
        money=10,
        damage_taken=0,
        special_stacks=0,
        faction="",
        specialization=1,
        inventory_items=[],
        inventory_specializations=[1],
        slot_weapon=None,
        slot_head=None,
        slot_torso=None,
        slot_arms=None,
        slot_legs=None,
        slot_ring_right=None,
        slot_ring_left=None,
        slot_boots=None,
        slot_gloves=None,
        slot_second_weapon=None,
        slot_belt=None,
        slot_lantern=None,
        slot_pet=None,
        slot_relic1=None,
        slot_relic2=None,
        slot_relic3=None,
        slot_relic4=None,
        slot_relic5=None,
        slot_relic6=None,
        ):
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
        self.slots = {
            "weapon" : slot_weapon,
            "head" : slot_head,
            "torso" : slot_torso,
            "arms" : slot_arms,
            "legs" : slot_legs,
            "ring_right" : slot_ring_right,
            "ring_left" : slot_ring_left,
            "boots" : slot_boots,
            "gloves" : slot_gloves,
            "second_weapon" : slot_second_weapon,
            "belt" : slot_belt,
            "lantern" : slot_lantern,
            "pet" : slot_pet,
            "relic1": slot_relic1,
            "relic2": slot_relic2,
            "relic3": slot_relic3,
            "relic4": slot_relic4,
            "relic5": slot_relic5,
            "relic6": slot_relic6
        }

    def calculateBonuses(self):
        bonuses = {
            "armor" : Bases_Bonuses_Slayers["armor"],
            "armor_per" : 0,
            "health" : Bases_Bonuses_Slayers["hp"],
            "health_per" : 0,
            "parry_L" : 0,
            "parry_H" : 0,
            "fail_L" : Bases_Bonuses_Slayers["fail_L"],
            "fail_H" : Bases_Bonuses_Slayers["fail_H"],
            "damage_weapon" : 0,
            "damage_L" : Bases_Bonuses_Slayers["damage_L"],
            "damage_H" : Bases_Bonuses_Slayers["damage_H"],
            "damage_S" : Specializations_list[self.specialization].damage,
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
            "crit_chance_L" : Bases_Bonuses_Slayers["crit_chance_L"],
            "crit_chance_H" : Bases_Bonuses_Slayers["crit_chance_H"],
            "crit_chance_S" : Bases_Bonuses_Slayers["crit_chance_S"],
            "crit_damage_L" : Bases_Bonuses_Slayers["crit_damage_L"],
            "crit_damage_H" : Bases_Bonuses_Slayers["crit_damage_H"],
            "crit_damage_S" : Bases_Bonuses_Slayers["crit_damage_S"],
            "special_charge_L" : Bases_Bonuses_Slayers["special_charge_L"],
            "special_charge_H" : Bases_Bonuses_Slayers["special_charge_H"],
            "special_charge_S" : 0,
            "stacks_reduction" : 0,
            "luck": Bases_Bonuses_Slayers["luck"],
            "vivacity": Bases_Bonuses_Slayers["vivacity"]
        }

        for slot in self.slots:
            if self.slots[slot] is not None:
                for item_bonus in Items_list[self.slots[slot]].bonuses:
                    bonuses[item_bonus] += Items_list[self.slots[slot]].bonuses[item_bonus]

        return bonuses

    def calculateStats(self):
        bonuses = self.calculateBonuses()
        stats = {
            "total_armor" : int(bonuses["armor"]*(1+bonuses["armor_per"])),
            "total_max_health" : int(bonuses["health"]*(1+bonuses["health_per"])),
            "total_current_health" : int(bonuses["health"]*(1+bonuses["health_per"])) - self.damage_taken,
            "total_fail_L" : min(max(bonuses["fail_L"],0),1),
            "total_fail_H" : min(max(bonuses["fail_H"],0),1),
            "total_fail_S" : 0,
            "total_parry_L" : bonuses["parry_L"],
            "total_parry_H" : bonuses["parry_H"],
            "total_parry_S" : 0,
            "total_damage_L" : int((bonuses["damage_L"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_L"])),
            "total_damage_H" : int((bonuses["damage_H"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_H"])),
            "total_damage_S" : int((bonuses["damage_S"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_S"])),
            "total_final_damage_L" : bonuses["final_damage_L"],
            "total_final_damage_H" : bonuses["final_damage_H"],
            "total_final_damage_S" : bonuses["final_damage_S"],
            "total_crit_chance_L" : min(bonuses["crit_chance_L"],1),
            "total_crit_chance_H" : min(bonuses["crit_chance_H"],1),
            "total_crit_chance_S" : min(bonuses["crit_chance_S"],1),
            "total_crit_damage_L" : bonuses["crit_damage_L"],
            "total_crit_damage_H" : bonuses["crit_damage_H"],
            "total_crit_damage_S" : bonuses["crit_damage_S"],
            "total_letality_L" : bonuses["letality_L"],
            "total_letality_H" : bonuses["letality_H"],
            "total_letality_S" : bonuses["letality_S"],
            "total_letality_per_L" : bonuses["letality_per_L"],
            "total_letality_per_H" : bonuses["letality_per_H"],
            "total_letality_per_S" : bonuses["letality_per_S"],
            "total_special_charge_L" : bonuses["special_charge_L"],
            "total_special_charge_H" : bonuses["special_charge_H"],
            "total_special_charge_S" : bonuses["special_charge_S"],
            "total_stacks_reduction" : bonuses["stacks_reduction"],
            "total_stacks" : max(Specializations_list[self.specialization].stacks - bonuses["stacks_reduction"], 1),
            "total_vivacity" : bonuses["vivacity"],
            "total_cooldown" : Bases_Bonuses_Slayers["cooldown"] - bonuses["vivacity"]
        }
        return stats

    def CalculateDamage(self, Hit, Battle):
        stats = self.calculateStats()
        #On check si on fail
        isFail = random.choices(population=[True, False], weights=[stats[f"total_fail_{Hit}"], 1-stats[f"total_fail_{Hit}"]], k=1)
        if isFail[0]:
            Damage = 0
            Stacks_Earned = 0
        else: 
            #On check si on est parrty
            isParry = random.choices(population=[True, False], weights=[min(max(Battle.monster_class.parry[f"parry_chance_{Hit}"] + stats[f"total_parry_{Hit}"], 0),1), 1-min(max((Battle.monster_class.parry[f"parry_chance_{Hit}"] + stats[f"total_parry_{Hit}"]), 0), 1)], k=1)
            if isParry[0]:
                Damage = -int(min(Battle.monster_class.damage * (Bases_Bonuses_Slayers["ratio_armor"]/(Bases_Bonuses_Slayers["ratio_armor"] + (stats["total_armor"] * (1 - Battle.monster_class.letality_per) - Battle.monster_class.letality))), stats["total_current_health"]))
                Stacks_Earned = 0
                #On subit les dégâts
                self.damage_taken = abs(Damage)
            else:
                #On check si on crit
                isCrit = random.choices(population=[True, False], weights=[stats[f"total_crit_chance_{Hit}"], 1-stats[f"total_crit_chance_{Hit}"]], k=1)
                #Calcul des dégâts
                Damage = min(int(max(((stats[f"total_damage_{Hit}"]*(1 + (stats[f"total_crit_damage_{Hit}"] if isCrit[0] else 0)) * (1 + stats[f"total_final_damage_{Hit}"])) - (Battle.monster_class.protect_crit if isCrit[0] else 0)), 0)*(Bases_Bonuses_Slayers["ratio_armor"]/(Bases_Bonuses_Slayers["ratio_armor"]+max(((Battle.monster_class.armor*(1-stats[f"total_letality_per_{Hit}"]))-stats[f"total_letality_{Hit}"]),0)))), Battle.monster_class.base_hp)
                Stacks_Earned = min(self.calculateStats()["total_stacks"] - self.special_stacks, self.calculateStats()[f"total_special_charge_{Hit}"])
                self.special_stacks += Stacks_Earned
        return Damage, Stacks_Earned

    def GetLoot(self):
        pass

    def GetDamage(self, damage):
        self.damage_taken += damage

    def GetGearScore(self):
        pass

    def Regen(self):
        pass



