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
    self.gearscore = 0
    self.base_bonuses = lib.get_bonuses(bot, rItem)

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
    self.gearscore = self.setGearscore()
    self.bonuses = self.base_bonuses
    

class Improvable_Object(Object):
  def __init__(self, bot, rItem):
    super().__init__(bot, rItem)
    self.level = 1 if "level" not in rItem else int(rItem["level"])
    self.maxlevel = self.set_max_level()
    self.gearscore = self.setGearscore()
    self.bonuses = lib.get_bonuses(bot, self.base_bonuses, self.level, self.maxlevel)

  def set_max_level(self):
    return 0

  async def update_item_level(self, level_upgrade, cSlayer):
      self.level += level_upgrade
      await self.bot.dB.push_update_item_level(cSlayer, self)
      self.bonuses = lib.get_bonuses(self.bot, self.base_bonuses, self.level, self.maxlevel)

  def setGearscore(self):
    return int((self.bot.Rarities[self.rarity].gearscore) / self.maxlevel * self.level)

class Pet(Improvable_Object):
  def __init__(self, bot, rItem):
    super().__init__(bot, rItem)
  
  def set_max_level(self):
    return int(self.bot.Variables["object_max_level_pets"])

  async def update_item_level(self, level_upgrade, cSlayer):
    await super().update_item_level(level_upgrade, cSlayer)
    self.gearscore = self.setGearscore()

class Mythic(Improvable_Object):
  def __init__(self, bot, rItem):
    super().__init__(bot, rItem)

  def set_max_level(self):
    return int(self.bot.Variables["object_max_level_mythics"])

  async def update_item_level(self, level_upgrade, cSlayer):
    await super().update_item_level(level_upgrade, cSlayer)
    self.gearscore = self.setGearscore()