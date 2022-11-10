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
      "parry_l" : rItem["parry_l"] * self.level,
      "parry_h" : rItem["parry_h"] * self.level,
      "parry_s" : rItem["parry_s"] * self.level,
      "fail_l" : rItem["fail_l"] * self.level,
      "fail_h" : rItem["fail_h"] * self.level,
      "damage_weapon" : rItem["damage_weapon"] * self.level,
      "damage_l" : rItem["damage_l"] * self.level,
      "damage_h" : rItem["damage_h"] * self.level,
      "damage_s" : rItem["damage_s"] * self.level,
      "final_damage_l" : rItem["final_damage_l"] * self.level,
      "final_damage_h" : rItem["final_damage_h"] * self.level,
      "final_damage_s" : rItem["final_damage_s"] * self.level,
      "damage_per_l" : rItem["damage_per_l"] * self.level,
      "damage_per_h" : rItem["damage_per_h"] * self.level,
      "damage_per_s" : rItem["damage_per_s"] * self.level,
      "letality_l" : rItem["letality_l"] * self.level,
      "letality_h" : rItem["letality_h"] * self.level,
      "letality_s" : rItem["letality_s"] * self.level,
      "letality_per_l" : rItem["letality_per_l"] * self.level,
      "letality_per_h" : rItem["letality_per_h"] * self.level,
      "letality_per_s" : rItem["letality_per_s"] * self.level,
      "crit_chance_l" : rItem["crit_chance_l"] * self.level,
      "crit_chance_h" : rItem["crit_chance_h"] * self.level,
      "crit_chance_s" : rItem["crit_chance_s"] * self.level,
      "crit_damage_l" : rItem["crit_damage_l"] * self.level,
      "crit_damage_h" : rItem["crit_damage_h"] * self.level,
      "crit_damage_s" : rItem["crit_damage_s"] * self.level,
      "special_charge_l" : rItem["special_charge_l"] * self.level,
      "special_charge_h" : rItem["special_charge_h"] * self.level,
      "special_charge_s" : rItem["special_charge_s"] * self.level,
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
          if bonus.find("_") != -1 and bonus[-1:] in ["l", "h", "s"]:
            if self.bonuses[bonus[:-1]+"l"] == self.bonuses[bonus[:-1]+"h"] == self.bonuses[bonus[:-1]+"s"]:
              if bonus.find("l") != -1:
                desc_stat += f"\n- {bonus[:-2]} : **{self.bonuses[bonus]}**" 
            else:
                desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}**"
          else:
            desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}**"      
      else:
        if self.bonuses[bonus] != 0 or cItem2.bonuses[bonus] != 0:
          if bonus.find("_") != -1 and bonus[-1:] in ["l", "h", "s"]:
            if self.bonuses[bonus[:-1]+"l"] == self.bonuses[bonus[:-1]+"h"] == self.bonuses[bonus[:-1]+"s"] and cItem2.bonuses[bonus[:-1]+"l"] == cItem2.bonuses[bonus[:-1]+"h"] == cItem2.bonuses[bonus[:-1]+"s"]:
              if bonus.find("l") != -1:

                #emote
                if self.bonuses[bonus] == cItem2.bonuses[bonus]:
                  emote = "🔸"
                elif self.bonuses[bonus] > cItem2.bonuses[bonus]:
                  emote = "🔹"
                elif self.bonuses[bonus] < cItem2.bonuses[bonus]:
                  emote = "🔻"
                else:
                  emote = ""

                desc_stat += f"\n- {bonus[:-2]} : **{self.bonuses[bonus]}** [← {cItem2.bonuses[bonus]}] {emote}"
            else:

              #emote
              if self.bonuses[bonus] == cItem2.bonuses[bonus]:
                emote = "🔸"
              elif self.bonuses[bonus] > cItem2.bonuses[bonus]:
                emote = "🔹"
              elif self.bonuses[bonus] < cItem2.bonuses[bonus]:
                emote = "🔻"
              else:
                emote = ""

              desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}** [← {cItem2.bonuses[bonus]}] {emote}"
          else:

            #emote
            if self.bonuses[bonus] == cItem2.bonuses[bonus]:
              emote = "🔸"
            elif self.bonuses[bonus] > cItem2.bonuses[bonus]:
              emote = "🔹"
            elif self.bonuses[bonus] < cItem2.bonuses[bonus]:
              emote = "🔻"
            else:
              emote = ""

            desc_stat += f"\n- {bonus} : **{self.bonuses[bonus]}** [← {cItem2.bonuses[bonus]}] {emote}"

    return desc_stat
