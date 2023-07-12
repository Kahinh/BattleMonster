from copy import deepcopy
from dataclasses import dataclass
import datetime
import random

from collections import Counter

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import lib

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

@dataclass
class Spe:

  id: int
  name: str
  description: str
  damage: int
  stacks: int
  cost: int
  emote: str
  ability_name: str

  def __init__(self, bot, rSpe, cLoadout=None):
    self.cLoadout = cLoadout
    self.bot = bot
    self.id = rSpe["id"]
    self.name = rSpe["name"]
    self.description = rSpe["description"]
    self.damage = rSpe["damage"]
    self.stacks = rSpe["stacks"]
    self.cost = rSpe["cost"]
    self.emote = rSpe["display_emote"]
    self.ability_name = rSpe["ability_name"]
    self.bonuses = lib.get_bonuses(bot, rSpe)
    self.temporary_stat = 0

  @staticmethod
  async def get_Spe_Class(bot, id, cLoadout):
    match int(id):
      case 1:
        return await Recrue.handler_Build(bot, id, cLoadout)
      case 2:
        return await EscrimeDouble.handler_Build(bot, id, cLoadout)
      case 3:
        return await Templier.handler_Build(bot, id, cLoadout)
      case 4:
        return await ChefdeGuerre.handler_Build(bot, id, cLoadout)
      case 5:
        return await Forgeron.handler_Build(bot, id, cLoadout)
      case 6:
        return await Stratège.handler_Build(bot, id, cLoadout)
      case 7:
        return await Démon.handler_Build(bot, id, cLoadout)
      case 8:
        return await Assassin.handler_Build(bot, id, cLoadout)
      case 9:
        return await Hemomancien.handler_Build(bot, id, cLoadout)
      case 10:
        return await Dompteur.handler_Build(bot, id, cLoadout)
      case 11:
        return await Guerrisseur.handler_Build(bot, id, cLoadout)
      case 12:
        return await Chargeur.handler_Build(bot, id, cLoadout)
      case _:
        print("Cette spé n'existe pas")

  @staticmethod
  def get_Spe_Class_row(bot, row):
    match int(row["id"]):
      case 1:
        return Recrue(bot, row)
      case 2:
        return EscrimeDouble(bot, row)
      case 3:
        return Templier(bot, row)
      case 4:
        return ChefdeGuerre(bot, row)
      case 5:
        return Forgeron(bot, row)
      case 6:
        return Stratège(bot, row)
      case 7:
        return Démon(bot, row)
      case 8:
        return Assassin(bot, row)
      case 9:
        return Hemomancien(bot, row)
      case 10:
        return Dompteur(bot, row)
      case 11:
        return Guerrisseur(bot, row)
      case 12:
        return Chargeur(bot, row)
      case _:
        print("Cette spé n'existe pas")

  @classmethod
  async def handler_Build(cls, bot, id, cLoadout):
    rSpe = await bot.dB.pull_spe_data(int(id))
    self = cls(bot, rSpe, cLoadout)
    return self

  @property
  def spe_damage(self):
      return 0

  def slot_nbr_max_items(self, cSlot):
    return cSlot.count

  def nbr_hit(self):
    return 0

  def demon_proc(self):
      return False

  def getDisplayStats(self, cObject2=None):
    return lib.get_display_stats(self, cObject2)
  
  def adapt_min(self, cap_min, bonus, stat):
    return cap_min

  def adapt_max(self, cap_max, bonus, stat):
    if "special_charge" in bonus:
      try:
        return int(float(self.bot.Variables["charge_gain_max_mult"]) * self.cLoadout.stats("stacks"))
      except:
        return cap_max
    else:
      return cap_max

  def update_temporary_stat(self, nbr):
    self.temporary_stat += nbr

  def temporary_stats(self):
    return {}
  
  def additional_stats(self):
    return {"damage_s": self.damage}

class Recrue(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

class EscrimeDouble(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)
  
  def slot_nbr_max_items(self, cSlot):
    if cSlot.name == "weapon":
      return cSlot.count + 1
    else:
      return cSlot.count

  def nbr_hit(self):
    return 1

class Templier(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

  def slot_nbr_max_items(self, cSlot):
    if cSlot.name == "shield":
      return cSlot.count + 1
    else:
      return cSlot.count

  @property
  def spe_damage(self):
    try:
      return int(self.cLoadout.stats("armor") * float(self.bot.Variables["templier_mult_armor_spe_damage"]))
    except:
      return 0

class ChefdeGuerre(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

class Forgeron(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

class Stratège(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

  def adapt_max(self, cap_max, bonus, stat):
    cap_max = super().adapt_max(cap_max, bonus, stat)
    if "letality_per" in bonus:
      return float(self.bot.Variables["chasseur_leta_per_cap_max"])
    else:
      return cap_max

class Démon(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)
    self.demon_stacks = 0

  @property
  def spe_damage(self):
    try:
      return min(int(float(self.bot.Variables["demon_bonus_mult"]) * self.demon_stacks * self.cLoadout.stats("damage_s")), int(float(self.bot.Variables["demon_max_spe_damage_mult_damage_s"]) * self.cLoadout.stats("damage_s")))
    except:
      return 0

  def demon_proc(self):
    if random.choices((True, False), (float(self.bot.Variables["demon_chance_proc"]), 1-float(self.bot.Variables["demon_chance_proc"])), k=1)[0]:
      self.demon_stacks += 1
      return True
    else:
      self.demon_stacks = 0
      return False

class Assassin(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

  def update_temporary_stat(self, nbr):
    self.temporary_stat = min(self.temporary_stat + nbr, self.bot.Variables["assassin_nbr_hit_activation"])

  def temporary_stats(self):
    if self.temporary_stat == 0:
      return {}
    else:
      return {
        "crit_chance_l": float(self.bot.Variables["assassin_crit_chance_bonus"]),
        "crit_chance_h": float(self.bot.Variables["assassin_crit_chance_bonus"]),
        "crit_chance_s": float(self.bot.Variables["assassin_crit_chance_bonus"]),
        "crit_damage_l": float(self.bot.Variables["assassin_crit_damage_bonus"]),
        "crit_damage_h": float(self.bot.Variables["assassin_crit_damage_bonus"]),
        "crit_damage_s": float(self.bot.Variables["assassin_crit_damage_bonus"])
      }

  def additional_stats(self):
    try:
      return {      
        "damage_s": self.damage,
        "crit_damage_l": max(0, (self.cLoadout.stats("crit_chance_l", False)-1)),
        "crit_damage_h": max(0, (self.cLoadout.stats("crit_chance_h", False)-1)),
        "crit_damage_s": max(0, (self.cLoadout.stats("crit_chance_s", False)-1))
      }
    except: 
      return {}

class Hemomancien(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

  #TODO Faire un get_buffs_stats pour Hemomancien
  def get_buffs_stats(self):
    pass

class Dompteur(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

  def slot_nbr_max_items(self, cSlot):
    if cSlot.name == "pet":
      return cSlot.count + 2
    else:
      return cSlot.count
    
  def get_buffs_stats(self):
    pets_list = [cObject for cObject in self.cLoadout.items if cObject.slot == "pet"]
    buffs_stats = {}
    for cObject in pets_list:
      buffs_stats = Counter(buffs_stats) + Counter(cObject.bonuses)
    return buffs_stats, 1

class Guerrisseur(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

  def slot_nbr_max_items(self, cSlot):
    if cSlot.name == "shield":
      return cSlot.count + 1
    else:
      return cSlot.count

class Chargeur(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

  def adapt_max(self, cap_max, bonus, stat):
    cap_max = super().adapt_max(cap_max, bonus, stat)
    if "stacks_reduction" in bonus:
      return 0
    else:
      return cap_max
    
  def update_temporary_stat(self, nbr):
    if nbr == 0:
      self.temporary_stat = 0
    else:
      self.temporary_stat += nbr

  @property
  def spe_damage(self):
    try:
      return int(self.temporary_stat)
    except:
      return 0

@dataclass
class Base_Slayer:
  def __init__(self, bot, rBase_Bonuses):
    self.bonuses = lib.get_bonuses(bot, rBase_Bonuses)