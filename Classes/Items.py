class Item:
  def __init__(
    self, 
    rItem
    ):
    self.item_id = rItem["item_id"]
    self.name = rItem["name"]
    self.description = rItem["description"]
    self.slot = rItem["slot"]
    self.img_url = rItem["img_url"]
    self.element = rItem["element"]
    self.rarity = rItem["rarity"]
    self.bonuses = {
      "armor" : rItem["armor"],
      "armor_per" : rItem["armor_per"],
      "health" : rItem["health"],
      "health_per" : rItem["health_per"],
      "parry_L" : rItem["parry_L"],
      "parry_H" : rItem["parry_H"],
      "parry_S" : rItem["parry_S"],
      "fail_L" : rItem["fail_L"],
      "fail_H" : rItem["fail_H"],
      "damage_weapon" : rItem["damage_weapon"],
      "damage_L" : rItem["damage_L"],
      "damage_H" : rItem["damage_H"],
      "damage_S" : rItem["damage_S"],
      "final_damage_L" : rItem["final_damage_L"],
      "final_damage_H" : rItem["final_damage_H"],
      "final_damage_S" : rItem["final_damage_S"],
      "damage_per_L" : rItem["damage_per_L"],
      "damage_per_H" : rItem["damage_per_H"],
      "damage_per_S" : rItem["damage_per_S"],
      "letality_L" : rItem["letality_L"],
      "letality_H" : rItem["letality_H"],
      "letality_S" : rItem["letality_S"],
      "letality_per_L" : rItem["letality_per_L"],
      "letality_per_H" : rItem["letality_per_H"],
      "letality_per_S" : rItem["letality_per_S"],
      "crit_chance_L" : rItem["crit_chance_L"],
      "crit_chance_H" : rItem["crit_chance_H"],
      "crit_chance_S" : rItem["crit_chance_S"],
      "crit_damage_L" : rItem["crit_damage_L"],
      "crit_damage_H" : rItem["crit_damage_H"],
      "crit_damage_S" : rItem["crit_damage_S"],
      "special_charge_L" : rItem["special_charge_L"],
      "special_charge_H" : rItem["special_charge_H"],
      "special_charge_S" : rItem["special_charge_S"],
      "stacks_reduction" : rItem["stacks_reduction"],
      "luck": rItem["luck"],
      "vivacity": rItem["vivacity"]
    }
  
  def getDisplayStats(self, cItem2=None):
    desc_stat = ""
    for bonus in self.bonuses:
      if cItem2 is None:
        if self.bonuses[bonus] != 0:
          if bonus.find("_") != -1 and self.bonuses[bonus[:-1]+"L"] == self.bonuses[bonus[:-1]+"H"] == self.bonuses[bonus[:-1]+"S"]:
            if bonus.find("L") != -1:
              desc_stat += f"\n- {bonus[:-2]} : **{self.bonuses[bonus]}**"   
          else:
            desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}**"      
      else:
        if self.bonuses[bonus] != 0 or cItem2.bonuses[bonus] != 0:
          if bonus.find("_") != -1 and self.bonuses[bonus[:-1]+"L"] == self.bonuses[bonus[:-1]+"H"] == self.bonuses[bonus[:-1]+"S"] and cItem2.bonuses[bonus[:-1]+"L"] == cItem2.bonuses[bonus[:-1]+"H"] == cItem2.bonuses[bonus[:-1]+"S"]:
            if bonus.find("L") != -1:
              desc_stat += f"\n- {bonus[:-2]} : **{self.bonuses[bonus]}** <- (**{cItem2.bonuses[bonus]}**)"
          else:
            desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}** <- (**{cItem2.bonuses[bonus]}**)"

    return desc_stat
