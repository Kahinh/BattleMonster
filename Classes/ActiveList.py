import datetime
from email import message
import os
import inspect
import sys
import asyncio

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from Classes.MainSlayers import MSlayer

class ActiveList:
  def __init__(
    self,
    bot
    ):
    self.bot = bot
    self.active_slayers = {}
    self.active_battles = {}
    self.active_lootrecap = {}
    self.active_gather = {}

  async def remove_inactive(self):
    inactive_slayers = []
    for id in self.active_slayers:
      if self.active_slayers[id].isInactive():
        inactive_slayers.append(id)
    
    if inactive_slayers != []:
      for id in inactive_slayers:
        self.active_slayers.pop(id)

  async def get_Slayer(self, user_id, user_name):
    if user_id not in self.active_slayers:
      #On init le Slayer
      Slayer = MSlayer(self.bot, user_id, user_name)
      await Slayer.constructClass()
      self.add_active_slayer(user_id, Slayer)
      return Slayer
    else:
      Slayer = self.active_slayers[user_id].Slayer
      self.active_slayers[user_id].timestamp = datetime.datetime.timestamp(datetime.datetime.now())
      return Slayer

  async def add_interface(self, id, interface_name, interface_class):
    #On check si on peut add une interface, et on retourne si elle est déjà utilisée
    if interface_name in self.active_slayers[id].interfaces:
      await self.active_slayers[id].interfaces[interface_name].close_view()
      self.active_slayers[id].interfaces[interface_name] = interface_class
    else:
      self.active_slayers[id].interfaces[interface_name] = interface_class
  
  async def update_interface(self, id, interface_name):
    if id in self.active_slayers:
      if interface_name in self.active_slayers[id].interfaces:
        await self.active_slayers[id].interfaces[interface_name].update_view()

  async def close_interface(self, id, interface):
    if interface in self.active_slayers[id].interfaces:
      await self.active_slayers[id].interfaces[interface].close_view()
      self.active_slayers[id].interfaces.pop(interface)

  def get_active_Slayer(self, user_id):
    if user_id in self.active_slayers:
      Slayer = self.active_slayers[user_id].Slayer
      self.active_slayers[user_id].timestamp = datetime.datetime.timestamp(datetime.datetime.now())
      return Slayer
    else:
      return None

  def add_active_slayer(self, id, Slayer):
    self.active_slayers[id] = ActiveSlayer(Slayer)

  def remove_interface(self, id, interface):
    if id in self.active_slayers:
      if interface in self.active_slayers[id].interfaces:
        self.active_slayers[id].interfaces.pop(interface)

  def obsolete_interfaces(self):
    for id in self.active_slayers:
      for interface in self.active_slayers[id].interfaces:
        self.active_slayers[id].interfaces[interface].obsolete = True
  
  def reset_slayers_activelist(self):
    self.active_slayers = {}
  
  def get_active_slayer_nbr(self):
    return int(len(self.active_slayers))
  
  ##########ACTIVE BATTLES
  def add_battle(self, message_id, Battle):
    self.active_battles[message_id] = Battle
  
  def remove_battle(self, message_id):
    if message_id in self.active_battles:
      self.active_battles.pop(message_id)

  async def clear_all_battles(self):
    for message_id, BattleView in list(self.active_battles.items()):
      await BattleView.updateBattle(poweroff=True, auto_remove_battle=False)
      await asyncio.sleep(2)
    self.active_battles = {}
  
  async def remove_eligibility(self, cSlayer):
    for message_id in self.active_battles:
      for cOpponent in self.active_battles[message_id].Battle.Opponents:
        if cSlayer in cOpponent.slayers_hits:
          cOpponent.slayers_hits[cSlayer.id].eligible = False

  async def timeout_timable_battle(self):
    for message_id, BattleView in list(self.active_battles.items()):
      if BattleView.Battle.timer_start is not None:
        if int(BattleView.Battle.timer_start) + int(self.bot.Variables["factionwar_timing_before_end_seconds"]) <= int(datetime.datetime.timestamp(datetime.datetime.now())):
          BattleView.Battle.end = True
          await BattleView.updateBattle(auto_remove_battle=False)
          self.active_battles.pop(message_id)

  ##########ACTIVE GATHER
  def add_gather(self, message_id, Gather):
    self.active_gather[message_id] = Gather
  
  def remove_gather(self, message_id):
    if message_id in self.active_gather:
      self.active_gather.pop(message_id)

  async def clear_all_gather(self):
    for message_id in self.active_gather:
      await self.active_gather[message_id].end_view(poweroff=True)
      await asyncio.sleep(2)
    self.active_gather = {}

  ###########ACTIVE LOOT RECAP
  def add_recap(self, message_id, Recap):
    self.active_lootrecap[message_id] = Recap
  
  def remove_recap(self, message_id):
    if message_id in self.active_lootrecap:
      self.active_lootrecap.pop(message_id)

  async def clear_all_recap(self):
    for message_id in self.active_lootrecap:
      await self.active_lootrecap[message_id].end_view(poweroff=True)
      await asyncio.sleep(2)
    self.active_lootrecap = {}

class ActiveSlayer:
  def __init__(
    self,
    Slayer
    ):
    self.timestamp = datetime.datetime.timestamp(datetime.datetime.now())
    self.Slayer = Slayer
    self.interfaces = {}

  def isInactive(self):
    if len(self.interfaces) == 0 and datetime.datetime.timestamp(datetime.datetime.now())-self.timestamp >= 3600:
      return True
    else:
      return False
