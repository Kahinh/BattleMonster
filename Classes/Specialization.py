from copy import deepcopy
import datetime

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
      "parry_L" : rSpe["parry_L"],
      "parry_H" : rSpe["parry_H"],
      "parry_S" : rSpe["parry_S"],
      "fail_L" : rSpe["fail_L"],
      "fail_H" : rSpe["fail_H"],
      "damage_weapon" : rSpe["damage_weapon"],
      "damage_L" : rSpe["damage_L"],
      "damage_H" : rSpe["damage_H"],
      "damage_S" : rSpe["damage_S"],
      "final_damage_L" : rSpe["final_damage_L"],
      "final_damage_H" : rSpe["final_damage_H"],
      "final_damage_S" : rSpe["final_damage_S"],
      "damage_per_L" : rSpe["damage_per_L"],
      "damage_per_H" : rSpe["damage_per_H"],
      "damage_per_S" : rSpe["damage_per_S"],
      "letality_L" : rSpe["letality_L"],
      "letality_H" : rSpe["letality_H"],
      "letality_S" : rSpe["letality_S"],
      "letality_per_L" : rSpe["letality_per_L"],
      "letality_per_H" : rSpe["letality_per_H"],
      "letality_per_S" : rSpe["letality_per_S"],
      "crit_chance_L" : rSpe["crit_chance_L"],
      "crit_chance_H" : rSpe["crit_chance_H"],
      "crit_chance_S" : rSpe["crit_chance_S"],
      "crit_damage_L" : rSpe["crit_damage_L"],
      "crit_damage_H" : rSpe["crit_damage_H"],
      "crit_damage_S" : rSpe["crit_damage_S"],
      "special_charge_L" : rSpe["special_charge_L"],
      "special_charge_H" : rSpe["special_charge_H"],
      "special_charge_S" : rSpe["special_charge_S"],
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
  
  def get_damage(self, cMonster, cSlayer):
    if self.id == 3: #Templier
      return int(cSlayer.stats["total_armor"]), ""
    elif self.id == 4: #Chef de Guerre
      return sum(cMonster.last_hits), ""
    elif self.id == 5: #Forgeron
      for slayer_id in cMonster.slayers_hits:
        cMonster.slayers_hits[slayer_id].timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now())
      return 0, "(*Cooldown reset*)"
    elif self.id == 6: #Analyst Chasseur   
      if cMonster.armor == cMonster.armor_cap:
        return int(cSlayer.stats["total_letality_S"] * (1+cSlayer.stats["total_letality_per_S"])), ""
      else:
        armor_reduction = int((cMonster.armor * cSlayer.stats["total_letality_per_S"] + cSlayer.stats["total_letality_S"]) / 5)
        armor_reduction = int(min(armor_reduction, cMonster.armor - cMonster.armor_cap))
        cMonster.armor -= armor_reduction
        return 0, f"(-{armor_reduction} 🛡️)"
    else:
      return 0, ""

  def getDisplayStats(self):
    desc_stat = ""
    for bonus in self.bonuses:
      if self.bonuses[bonus] != 0:
        if bonus.find("_") != -1 and bonus[-1:] in ["L", "H", "S"]:
          if self.bonuses[bonus[:-1]+"L"] == self.bonuses[bonus[:-1]+"H"] == self.bonuses[bonus[:-1]+"S"]:
            if bonus.find("L") != -1:
              desc_stat += f"\n- {bonus[:-2]} : **{self.bonuses[bonus]}**" 
          else:
              desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}**"
        else:
          desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}**"      
    return desc_stat
