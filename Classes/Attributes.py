from copy import deepcopy
from dataclasses import dataclass
import datetime
import random

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
    self.add_spe_damage()
    self.remaining_hit_temporary_stat = 0
    self.spe_damage = 0

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
      case _:
        print("Cette spé n'existe pas")

  @classmethod
  async def handler_Build(cls, bot, id, cLoadout):
    rSpe = await bot.dB.pull_spe_data(int(id))
    self = cls(bot, rSpe, cLoadout)
    return self

  def slot_nbr_max_items(self, cSlot):
    return cSlot.count

  def nbr_hit(self):
    return 0

  def demon_proc(self, dict_data):
      return False

  def add_spe_damage(self):
    self.bonuses["damage_s"] += self.damage

  def update_spe_damage(self):
    pass
  
  def refresh_stats(self):
    self.cLoadout.update_stats([])

  def activate_temporary_stat(self):
    pass

  def reduce_remaining_hit_temporary_stat(self):
    if self.remaining_hit_temporary_stat == 0:
      pass
    else:
      self.remaining_hit_temporary_stat -= 1
      if self.remaining_hit_temporary_stat == 0:
        self.cLoadout.deactivate_temporary_stat()

  def temporary_stats(self):
    return []

  def getDisplayStats(self, cObject2=None):
    return lib.get_display_stats(self, cObject2)
  
  def adapt_min(self, cap_min, statistic, dict_data):
    return cap_min

  def adapt_max(self, cap_max, statistic, dict_data):
    if "special_charge" in statistic:
      return int(float(self.bot.Variables["charge_gain_max_mult"]) * int(dict_data['stacks'] - dict_data.get('stacks_reduction', 0)))
    else:
      return cap_max
  
  def retreat_stats(self, dict_stats):
    return dict_stats

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
    self.update_spe_damage()

  def slot_nbr_max_items(self, cSlot):
    if cSlot.name == "shield":
      return cSlot.count + 1
    else:
      return cSlot.count
    
  def update_spe_damage(self):
    if self.cLoadout is not None : self.spe_damage = self.cLoadout.stats["armor"] 

class ChefdeGuerre(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

class Forgeron(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

class Stratège(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

  def adapt_max(self, cap_max, statistic, dict_data):
    cap_max = super().adapt_max(cap_max, statistic, dict_data)
    if statistic == "leta_per":
      return self.bot.Variables["chasseur_leta_per_cap_max"]
    else:
      return cap_max

class Démon(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)
  
  def demon_proc(self, dict_data):
    if random.choices((True, False), (float(self.bot.Variables["demon_chance_proc"]), 1-float(self.bot.Variables["demon_chance_proc"])), k=1)[0]:
      self.spe_damage += int(float(self.bot.Variables["demon_bonus_mult"]) * dict_data["damage_s"])
      return True
    else:
      self.spe_damage = 0
      return False

class Assassin(Spe):
  def __init__(self, bot, rSpe, cLoadout=None):
    super().__init__(bot, rSpe, cLoadout)

  def activate_temporary_stat(self):
    self.remaining_hit_temporary_stat = int(self.bot.Variables['assassin_nbr_hit_activation'])

  def temporary_stats(self):
    return [['crit_chance_l', float(self.bot.Variables['assassin_crit_chance_bonus'])], ['crit_chance_h', float(self.bot.Variables['assassin_crit_chance_bonus'])], ['crit_damage_l', float(self.bot.Variables['assassin_crit_damage_bonus'])], ['crit_damage_h', float(self.bot.Variables['assassin_crit_damage_bonus'])]]

  def retreat_stats(self, dict_stats):
    dict_stats = super().retreat_stats(dict_stats)
    dict_stats["crit_damage_l"] += max(dict_stats["crit_chance_l"] - 1, 0)
    dict_stats["crit_damage_h"] += max(dict_stats["crit_chance_h"] - 1, 0)
    dict_stats["crit_damage_s"] += max(dict_stats["crit_chance_s"] - 1, 0)
    return dict_stats

@dataclass
class Base_Slayer:
  def __init__(self, bot, rBase_Bonuses):
    self.bonuses = lib.get_bonuses(bot, rBase_Bonuses)