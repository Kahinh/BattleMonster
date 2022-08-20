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

  def add_active_slayer(self, slayer_id, Slayer, interface):
    self.active_slayers[slayer_id] = ActiveSlayer(Slayer)
    self.active_slayers[slayer_id].interfaces[interface] = True

  def close_interface(self, slayer_id, interface):
    self.active_slayers[slayer_id].interfaces[interface] = False
  
  def add_interface(self, slayer_id, interface):
    #On check si on peut add une interface, et on retourne si elle est déjà utilisée
    if interface in self.active_slayers[slayer_id].interfaces:
      if self.active_slayers[slayer_id].interfaces[interface] == True:
        return False
      else:
        self.active_slayers[slayer_id].interfaces[interface] = True
        return True
    else:
      self.active_slayers[slayer_id].interfaces[interface] = True
      return True

  async def get_Slayer(self, user_id, user_name, interface):
    if user_id not in self.active_slayers:
        #On init le Slayer
        Slayer = MSlayer(self.bot, user_id, user_name)
        await Slayer.constructClass()
        self.add_active_slayer(user_id, Slayer, interface)
        InterfaceReady = True
        return Slayer, InterfaceReady
    else:
      try:
        if self.active_slayers[user_id].interfaces[interface] == True:
          Slayer = self.active_slayers[user_id].Slayer
          InterfaceReady = False
          return Slayer, InterfaceReady
        else:
          Slayer = self.active_slayers[user_id].Slayer
          InterfaceReady = True
          return Slayer, InterfaceReady      
      except:
        #On refresh le timestamp et on récupère le Slayer
        Slayer = self.active_slayers[user_id].Slayer
        self.active_slayers[user_id].interfaces[interface] = True
        self.active_slayers[user_id].timestamp = datetime.datetime.timestamp(datetime.datetime.now())
        InterfaceReady = True
        return Slayer, InterfaceReady

class ActiveSlayer:
  def __init__(
    self,
    Slayer
    ):
    self.timestamp = datetime.datetime.timestamp(datetime.datetime.now())
    self.Slayer = Slayer
    self.interfaces = {}
