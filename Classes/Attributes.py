from copy import deepcopy
from dataclasses import dataclass
import datetime

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import lib


class Spe:
  def __init__(
    self, 
    rSpe
    ):
    self.id = rSpe["id"]
    self.name = rSpe["name"]
    self.description = rSpe["description"]
    self.damage = rSpe["damage"]
    self.stacks = rSpe["stacks"]
    self.cost = rSpe["cost"]
    self.emote = rSpe["display_emote"]
    self.ability_name = rSpe["ability_name"]
    self.bonuses = {
      "armor" : rSpe["armor"],
      "armor_per" : rSpe["armor_per"],
      "health" : rSpe["health"],
      "health_per" : rSpe["health_per"],
      "parry_l" : rSpe["parry_l"],
      "parry_h" : rSpe["parry_h"],
      "parry_s" : rSpe["parry_s"],
      "damage_weapon" : rSpe["damage_weapon"],
      "damage_l" : rSpe["damage_l"],
      "damage_h" : rSpe["damage_h"],
      "damage_s" : rSpe["damage_s"],
      "final_damage_l" : rSpe["final_damage_l"],
      "final_damage_h" : rSpe["final_damage_h"],
      "final_damage_s" : rSpe["final_damage_s"],
      "damage_per_l" : rSpe["damage_per_l"],
      "damage_per_h" : rSpe["damage_per_h"],
      "damage_per_s" : rSpe["damage_per_s"],
      "letality_l" : rSpe["letality_l"],
      "letality_h" : rSpe["letality_h"],
      "letality_s" : rSpe["letality_s"],
      "letality_per_l" : rSpe["letality_per_l"],
      "letality_per_h" : rSpe["letality_per_h"],
      "letality_per_s" : rSpe["letality_per_s"],
      "crit_chance_l" : rSpe["crit_chance_l"],
      "crit_chance_h" : rSpe["crit_chance_h"],
      "crit_chance_s" : rSpe["crit_chance_s"],
      "crit_damage_l" : rSpe["crit_damage_l"],
      "crit_damage_h" : rSpe["crit_damage_h"],
      "crit_damage_s" : rSpe["crit_damage_s"],
      "special_charge_l" : rSpe["special_charge_l"],
      "special_charge_h" : rSpe["special_charge_h"],
      "special_charge_s" : rSpe["special_charge_s"],
      "stacks_reduction" : rSpe["stacks_reduction"],
      "luck": rSpe["luck"],
      "vivacity": rSpe["vivacity"]
    }

  def adjust_slot_count(self, rSlots):
    Slots = deepcopy(rSlots)
    #SURAREMENT
    if self.id == 2:
      Slots["weapon"]["count"] = 2
    #TEMPLIER
    if self.id == 3:
      Slots["shield"]["count"] = 1
    return Slots

  def nbr_hit(self, standard):
    base = deepcopy(standard)
    if self.id == 2:
      base += 1
    return base
  
  def get_damage(self, cOpponent, cSlayer):
    if self.id == 3: #Templier
      return int(cSlayer.stats["total_armor"]), ""
    elif self.id == 4: #Chef de Guerre
      return sum(cOpponent.last_hits), ""
    elif self.id == 5: #Forgeron
      for id in cOpponent.slayers_hits:
        cOpponent.slayers_hits[id].timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now())
      return 0, "(*Cooldown reset*)"
    elif self.id == 6: #Analyst Chasseur   
      if cOpponent.armor == cOpponent.armor_cap:
        return int(cSlayer.stats["total_letality_s"] * (1+cSlayer.stats["total_letality_per_s"])), ""
      else:
        #TODO A REFAIRE POUR LE REWORK LETA
        armor_reduction = int((cOpponent.armor * cSlayer.stats["total_letality_per_s"] + cSlayer.stats["total_letality_s"]) / 5)
        armor_reduction = int(min(armor_reduction, cOpponent.armor - cOpponent.armor_cap))
        cOpponent.armor -= armor_reduction
        return 0, f"(-{armor_reduction} 🛡️)"
    else:
      return 0, ""

  def getDisplayStats(self, cItem2=None):
    return lib.get_display_stats(self, cItem2)

@dataclass
class Faction:
  id: int
  name: str
  description: str
  emote: str
  gatherable_affinity: str
  money: int

  def __init__(self, rFaction):
    self.id = rFaction["id"]
    self.name = rFaction["name"]
    self.description = rFaction["description"]
    self.emote = rFaction["emote"]
    self.gatherable_affinity = rFaction["gatherable_affinity"]
    self.money = rFaction["money"]