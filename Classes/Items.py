class Item:
  def __init__(
    self, 
    rItem
    ):
    self.item_id = rItem["id"]
    self.level = 1 if "level" not in rItem else rItem["level"]
    self.name = rItem["name"]
    self.description = rItem["description"]
    self.slot = rItem["slot"]
    self.equipped = False if "equipped" not in rItem else rItem["equipped"]
    self.img_url = rItem["img_url"]
    self.element = rItem["element"]
    self.rarity = rItem["rarity"]
    self.bonuses = {
      "armor" : rItem["armor"] * self.level,
      "armor_per" : rItem["armor_per"] * self.level,
      "health" : rItem["health"] * self.level,
      "health_per" : rItem["health_per"] * self.level,
      "parry_L" : rItem["parry_L"] * self.level,
      "parry_H" : rItem["parry_H"] * self.level,
      "parry_S" : rItem["parry_S"] * self.level,
      "fail_L" : rItem["fail_L"] * self.level,
      "fail_H" : rItem["fail_H"] * self.level,
      "damage_weapon" : rItem["damage_weapon"] * self.level,
      "damage_L" : rItem["damage_L"] * self.level,
      "damage_H" : rItem["damage_H"] * self.level,
      "damage_S" : rItem["damage_S"] * self.level,
      "final_damage_L" : rItem["final_damage_L"] * self.level,
      "final_damage_H" : rItem["final_damage_H"] * self.level,
      "final_damage_S" : rItem["final_damage_S"] * self.level,
      "damage_per_L" : rItem["damage_per_L"] * self.level,
      "damage_per_H" : rItem["damage_per_H"] * self.level,
      "damage_per_S" : rItem["damage_per_S"] * self.level,
      "letality_L" : rItem["letality_L"] * self.level,
      "letality_H" : rItem["letality_H"] * self.level,
      "letality_S" : rItem["letality_S"] * self.level,
      "letality_per_L" : rItem["letality_per_L"] * self.level,
      "letality_per_H" : rItem["letality_per_H"] * self.level,
      "letality_per_S" : rItem["letality_per_S"] * self.level,
      "crit_chance_L" : rItem["crit_chance_L"] * self.level,
      "crit_chance_H" : rItem["crit_chance_H"] * self.level,
      "crit_chance_S" : rItem["crit_chance_S"] * self.level,
      "crit_damage_L" : rItem["crit_damage_L"] * self.level,
      "crit_damage_H" : rItem["crit_damage_H"] * self.level,
      "crit_damage_S" : rItem["crit_damage_S"] * self.level,
      "special_charge_L" : rItem["special_charge_L"] * self.level,
      "special_charge_H" : rItem["special_charge_H"] * self.level,
      "special_charge_S" : rItem["special_charge_S"] * self.level,
      "stacks_reduction" : rItem["stacks_reduction"] * self.level,
      "luck": rItem["luck"] * self.level,
      "vivacity": rItem["vivacity"] * self.level
    }
  
  def equip(self):
      self.equipped = True

  def unequip(self):
      self.equipped = False
  
  def getDisplayStats(self, cItem2=None):
    desc_stat = ""
    if cItem2 is not None:
      desc_stat += f"\n*Comparaison {cItem2.name}*"
    for bonus in self.bonuses:
      if cItem2 is None or self.item_id == cItem2.item_id:
        if self.bonuses[bonus] != 0:
          if bonus.find("_") != -1 and bonus[-1:] in ["L", "H", "S"]:
            if self.bonuses[bonus[:-1]+"L"] == self.bonuses[bonus[:-1]+"H"] == self.bonuses[bonus[:-1]+"S"]:
              if bonus.find("L") != -1:
                desc_stat += f"\n- {bonus[:-2]} : **{self.bonuses[bonus]}**" 
            else:
                desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}**"
          else:
            desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}**"      
      else:
        if self.bonuses[bonus] != 0 or cItem2.bonuses[bonus] != 0:
          if bonus.find("_") != -1 and bonus[-1:] in ["L", "H", "S"]:
            if self.bonuses[bonus[:-1]+"L"] == self.bonuses[bonus[:-1]+"H"] == self.bonuses[bonus[:-1]+"S"] and cItem2.bonuses[bonus[:-1]+"L"] == cItem2.bonuses[bonus[:-1]+"H"] == cItem2.bonuses[bonus[:-1]+"S"]:
              if bonus.find("L") != -1:
                desc_stat += f"\n- {bonus[:-2]} : **{self.bonuses[bonus]}** <- (**{cItem2.bonuses[bonus]}**)"
            else:
              desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}** <- (**{cItem2.bonuses[bonus]}**)"
          else:
            desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}** <- (**{cItem2.bonuses[bonus]}**)"

    return desc_stat
