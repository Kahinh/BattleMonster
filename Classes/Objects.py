import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import lib

class Object:
  def __init__(self, bot, rItem):
    self.bot = bot
    self.id = rItem["id"]
    self.level = 0
    self.name = rItem["name"]
    self.description = rItem["description"]
    self.slot = rItem["slot"]
    self.equipped = False if "equipped" not in rItem else rItem["equipped"]
    self.img_url = rItem["img_url"]
    self.element = rItem["element"]
    self.rarity = rItem["rarity"]
    self.gearscore = self.setGearscore()
    self.bonuses = {
      "armor" : rItem["armor"],
      "armor_per" : float(rItem["armor_per"]),
      "health" : rItem["health"],
      "health_per" : float(rItem["health_per"]),
      "parry_l" : float(rItem["parry_l"]),
      "parry_h" : float(rItem["parry_h"]),
      "parry_s" : float(rItem["parry_s"]),
      "damage_weapon" : rItem["damage_weapon"],
      "damage_l" : rItem["damage_l"],
      "damage_h" : rItem["damage_h"],
      "damage_s" : rItem["damage_s"],
      "final_damage_l" : float(rItem["final_damage_l"]),
      "final_damage_h" : float(rItem["final_damage_h"]),
      "final_damage_s" : float(rItem["final_damage_s"]),
      "damage_per_l" : float(rItem["damage_per_l"]),
      "damage_per_h" : float(rItem["damage_per_h"]),
      "damage_per_s" : float(rItem["damage_per_s"]),
      "letality_l" : rItem["letality_l"],
      "letality_h" : rItem["letality_h"],
      "letality_s" : rItem["letality_s"],
      "letality_per_l" : float(rItem["letality_per_l"]),
      "letality_per_h" : float(rItem["letality_per_h"]),
      "letality_per_s" : float(rItem["letality_per_s"]),
      "crit_chance_l" : float(rItem["crit_chance_l"]),
      "crit_chance_h" : float(rItem["crit_chance_h"]),
      "crit_chance_s" : float(rItem["crit_chance_s"]),
      "crit_damage_l" : float(rItem["crit_damage_l"]),
      "crit_damage_h" : float(rItem["crit_damage_h"]),
      "crit_damage_s" : float(rItem["crit_damage_s"]),
      "special_charge_l" : rItem["special_charge_l"],
      "special_charge_h" : rItem["special_charge_h"],
      "special_charge_s" : rItem["special_charge_s"],
      "stacks_reduction" : rItem["stacks_reduction"],
      "luck": float(rItem["luck"]),
      "vivacity": rItem["vivacity"]
    }

  @staticmethod
  def get_Object_Class(bot, rItem):
    if rItem["slot"] == "pet":
      return Pet(bot, rItem)
    else:
      if rItem["rarity"] == "mythic":
        return Mythic(bot, rItem)
      else:
        return Item(bot, rItem)

  def equip(self):
      #TODO Mettre un self.bot.db 
      self.equipped = True

  def unequip(self):
      #TODO Mettre un self.bot.db 
      self.equipped = False
  
  def getDisplayStats(self, cObject2=None):
    return lib.get_display_stats(self, cObject2)

  def setGearscore(self):
    return self.bot.Rarities[self.rarity].gearscore

class Item(Object):
  def __init__(self, bot, rItem):
    super().__init__(bot, rItem)

class Improvable_Object(Object):
  def __init__(self, bot, rItem):
    super().__init__(bot, rItem)
    self.level = 1 if "level" not in rItem else rItem["level"]
    self.gearscore = self.setGearscore()
    self.base_bonuses = {
      "armor" : rItem["armor"],
      "armor_per" : float(rItem["armor_per"]),
      "health" : rItem["health"],
      "health_per" : float(rItem["health_per"]),
      "parry_l" : float(rItem["parry_l"]),
      "parry_h" : float(rItem["parry_h"]),
      "parry_s" : float(rItem["parry_s"]),
      "damage_weapon" : rItem["damage_weapon"],
      "damage_l" : rItem["damage_l"],
      "damage_h" : rItem["damage_h"],
      "damage_s" : rItem["damage_s"],
      "final_damage_l" : float(rItem["final_damage_l"]),
      "final_damage_h" : float(rItem["final_damage_h"]),
      "final_damage_s" : float(rItem["final_damage_s"]),
      "damage_per_l" : float(rItem["damage_per_l"]),
      "damage_per_h" : float(rItem["damage_per_h"]),
      "damage_per_s" : float(rItem["damage_per_s"]),
      "letality_l" : rItem["letality_l"],
      "letality_h" : rItem["letality_h"],
      "letality_s" : rItem["letality_s"],
      "letality_per_l" : float(rItem["letality_per_l"]),
      "letality_per_h" : float(rItem["letality_per_h"]),
      "letality_per_s" : float(rItem["letality_per_s"]),
      "crit_chance_l" : float(rItem["crit_chance_l"]),
      "crit_chance_h" : float(rItem["crit_chance_h"]),
      "crit_chance_s" : float(rItem["crit_chance_s"]),
      "crit_damage_l" : float(rItem["crit_damage_l"]),
      "crit_damage_h" : float(rItem["crit_damage_h"]),
      "crit_damage_s" : float(rItem["crit_damage_s"]),
      "special_charge_l" : rItem["special_charge_l"],
      "special_charge_h" : rItem["special_charge_h"],
      "special_charge_s" : rItem["special_charge_s"],
      "stacks_reduction" : rItem["stacks_reduction"],
      "luck": float(rItem["luck"]),
      "vivacity": rItem["vivacity"]
    }
    self.bonuses = self.calculate_bonuses()

  def calculate_bonuses(self):
    bonuses = {
      "armor" : int(self.base_bonuses["armor"] * self.level),
      "armor_per" : round(self.base_bonuses["armor_per"] * self.level,4),
      "health" : int(self.base_bonuses["health"] * self.level),
      "health_per" : round(self.base_bonuses["health_per"] * self.level,4),
      "parry_l" : round(self.base_bonuses["parry_l"] * self.level,4),
      "parry_h" : round(self.base_bonuses["parry_h"] * self.level,4),
      "parry_s" : round(self.base_bonuses["parry_s"] * self.level,4),
      "damage_weapon" : int(self.base_bonuses["damage_weapon"] * self.level),
      "damage_l" : int(self.base_bonuses["damage_l"] * self.level),
      "damage_h" : int(self.base_bonuses["damage_h"] * self.level),
      "damage_s" : int(self.base_bonuses["damage_s"] * self.level),
      "final_damage_l" : round(self.base_bonuses["final_damage_l"] * self.level,4),
      "final_damage_h" : round(self.base_bonuses["final_damage_h"] * self.level,4),
      "final_damage_s" : round(self.base_bonuses["final_damage_s"] * self.level,4),
      "damage_per_l" : round(self.base_bonuses["damage_per_l"] * self.level,4),
      "damage_per_h" : round(self.base_bonuses["damage_per_h"] * self.level,4),
      "damage_per_s" : round(self.base_bonuses["damage_per_s"] * self.level,4),
      "letality_l" : int(self.base_bonuses["letality_l"] * self.level),
      "letality_h" : int(self.base_bonuses["letality_h"] * self.level),
      "letality_s" : int(self.base_bonuses["letality_s"] * self.level),
      "letality_per_l" : round(self.base_bonuses["letality_per_l"] * self.level,4),
      "letality_per_h" : round(self.base_bonuses["letality_per_h"] * self.level,4),
      "letality_per_s" : round(self.base_bonuses["letality_per_s"] * self.level,4),
      "crit_chance_l" : round(self.base_bonuses["crit_chance_l"] * self.level,4),
      "crit_chance_h" : round(self.base_bonuses["crit_chance_h"] * self.level,4),
      "crit_chance_s" : round(self.base_bonuses["crit_chance_s"] * self.level,4),
      "crit_damage_l" : round(self.base_bonuses["crit_damage_l"] * self.level,4),
      "crit_damage_h" : round(self.base_bonuses["crit_damage_h"] * self.level,4),
      "crit_damage_s" : round(self.base_bonuses["crit_damage_s"] * self.level,4),
      "special_charge_l" : int(self.base_bonuses["special_charge_l"] * self.level),
      "special_charge_h" : int(self.base_bonuses["special_charge_h"] * self.level),
      "special_charge_s" : int(self.base_bonuses["special_charge_s"] * self.level),
      "stacks_reduction" : int(self.base_bonuses["stacks_reduction"] * self.level),
      "luck": round(self.base_bonuses["luck"] * self.level,4),
      "vivacity": int(self.base_bonuses["vivacity"] * self.level)
    }
    return bonuses

  async def update_item_level(self, level_upgrade, cSlayer):
      self.level += level_upgrade
      await self.bot.dB.push_update_item_level(cSlayer, self)
      self.bonuses = self.calculate_bonuses()

class Pet(Improvable_Object):
  def __init__(self, bot, rItem):
    super().__init__(bot, rItem)

  async def update_item_level(self, level_upgrade, cSlayer):
    await super().update_item_level(level_upgrade, cSlayer)
    self.gearscore = self.setGearscore()

  def setGearscore(self):
    if self.rarity == "mythic":
      return int(((self.bot.Rarities[self.rarity].gearscore+40)/100) * self.level)
    else:
      return int((self.bot.Rarities[self.rarity].gearscore/100) * self.level)

class Mythic(Improvable_Object):
  def __init__(self, bot, rItem):
    super().__init__(bot, rItem)

  async def update_item_level(self, level_upgrade, cSlayer):
    await super().update_item_level(level_upgrade, cSlayer)
    self.gearscore = self.setGearscore()

  def setGearscore(self):
    return self.bot.Rarities[self.rarity].gearscore + self.level