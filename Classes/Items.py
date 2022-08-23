class Item:
  def __init__(
    self, 
    rItem
    ):
    self.item_id = rItem["id"]
    self.level = rItem["level"]
    self.name = rItem["name"]
    self.description = rItem["description"]
    self.slot = rItem["slot"]
    self.equipped = rItem["equipped"]
    self.img_url = rItem["img_url"]
    self.element = rItem["element"]
    self.rarity = rItem["rarity"]
    self.bonuses = {
      "armor" : rItem["armor"] * rItem["level"],
      "armor_per" : rItem["armor_per"] * rItem["level"],
      "health" : rItem["health"] * rItem["level"],
      "health_per" : rItem["health_per"] * rItem["level"],
      "parry_L" : rItem["parry_L"] * rItem["level"],
      "parry_H" : rItem["parry_H"] * rItem["level"],
      "parry_S" : rItem["parry_S"] * rItem["level"],
      "fail_L" : rItem["fail_L"] * rItem["level"],
      "fail_H" : rItem["fail_H"] * rItem["level"],
      "damage_weapon" : rItem["damage_weapon"] * rItem["level"],
      "damage_L" : rItem["damage_L"] * rItem["level"],
      "damage_H" : rItem["damage_H"] * rItem["level"],
      "damage_S" : rItem["damage_S"] * rItem["level"],
      "final_damage_L" : rItem["final_damage_L"] * rItem["level"],
      "final_damage_H" : rItem["final_damage_H"] * rItem["level"],
      "final_damage_S" : rItem["final_damage_S"] * rItem["level"],
      "damage_per_L" : rItem["damage_per_L"] * rItem["level"],
      "damage_per_H" : rItem["damage_per_H"] * rItem["level"],
      "damage_per_S" : rItem["damage_per_S"] * rItem["level"],
      "letality_L" : rItem["letality_L"] * rItem["level"],
      "letality_H" : rItem["letality_H"] * rItem["level"],
      "letality_S" : rItem["letality_S"] * rItem["level"],
      "letality_per_L" : rItem["letality_per_L"] * rItem["level"],
      "letality_per_H" : rItem["letality_per_H"] * rItem["level"],
      "letality_per_S" : rItem["letality_per_S"] * rItem["level"],
      "crit_chance_L" : rItem["crit_chance_L"] * rItem["level"],
      "crit_chance_H" : rItem["crit_chance_H"] * rItem["level"],
      "crit_chance_S" : rItem["crit_chance_S"] * rItem["level"],
      "crit_damage_L" : rItem["crit_damage_L"] * rItem["level"],
      "crit_damage_H" : rItem["crit_damage_H"] * rItem["level"],
      "crit_damage_S" : rItem["crit_damage_S"] * rItem["level"],
      "special_charge_L" : rItem["special_charge_L"] * rItem["level"],
      "special_charge_H" : rItem["special_charge_H"] * rItem["level"],
      "special_charge_S" : rItem["special_charge_S"] * rItem["level"],
      "stacks_reduction" : rItem["stacks_reduction"] * rItem["level"],
      "luck": rItem["luck"] * rItem["level"],
      "vivacity": rItem["vivacity"] * rItem["level"]
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
