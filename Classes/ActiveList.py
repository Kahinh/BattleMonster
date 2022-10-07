import datetime
import os
import inspect
import sys

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

  async def add_interface(self, slayer_id, interface_name, interface_class):
    #On check si on peut add une interface, et on retourne si elle est déjà utilisée
    if interface_name in self.active_slayers[slayer_id].interfaces:
      await self.active_slayers[slayer_id].interfaces[interface_name].close_view()
      self.active_slayers[slayer_id].interfaces[interface_name] = interface_class
    else:
      self.active_slayers[slayer_id].interfaces[interface_name] = interface_class
  
  async def update_interface(self, slayer_id, interface_name):
    if slayer_id in self.active_slayers:
      if interface_name in self.active_slayers[slayer_id].interfaces:
        await self.active_slayers[slayer_id].interfaces[interface_name].update_view()

  async def close_interface(self, slayer_id, interface):
    if interface in self.active_slayers[slayer_id].interfaces:
      await self.active_slayers[slayer_id].interfaces[interface].close_view()
      self.active_slayers[slayer_id].interfaces.pop(interface)

  def add_active_slayer(self, slayer_id, Slayer):
    self.active_slayers[slayer_id] = ActiveSlayer(Slayer)

  def remove_interface(self, slayer_id, interface):
    if interface in self.active_slayers[slayer_id].interfaces:
      self.active_slayers[slayer_id].interfaces.pop(interface)
    
  def regen_health_all(self):
    for slayer_id in self.active_slayers:
      self.active_slayers[slayer_id].Slayer.cSlayer.regenHealth(self.bot.rBaseBonuses["regen"])

  def rez_all(self):
    for slayer_id in self.active_slayers:
      self.active_slayers[slayer_id].Slayer.cSlayer.regenHealth(self.bot.rBaseBonuses["regen"])
      self.active_slayers[slayer_id].Slayer.cSlayer.rez()

class ActiveSlayer:
  def __init__(
    self,
    Slayer
    ):
    self.timestamp = datetime.datetime.timestamp(datetime.datetime.now())
    self.Slayer = Slayer
    self.interfaces = {}
