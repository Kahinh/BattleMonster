import random, os, inspect, sys

from dataclasses import dataclass
from Classes.Opponents import Monster

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import lib

class Battle:
  def __init__(
    self, 
    bot,
    gamemode,
    interaction=None
    ):
    self.bot = bot
    self.end = False
    self.name = gamemode["name"]
    self.lootslot = self.bot.rGameModesLootSlot[self.name]
    self.min_dice = gamemode["roll_dices_min"]
    self.max_dice = gamemode["roll_dices_max"]
    self.interaction = interaction
    self.loots = {}

    #Gestion du nombre de spawns
    self.spawns_count = gamemode["spawns_count"]
    self.count = 0
    self.Opponents = {}
    self.LootTable = {}

    self.EndNotPublished = True

    self.scaling = {
      'hp': gamemode["hp_scaling"],
      'armor': gamemode["armor_scaling"],
      'letality': gamemode["letality_scaling"],
      'parry': gamemode["parry_scaling"],
      'damage': gamemode["damage_scaling"],
      'protect_crit': gamemode["protect_crit_scaling"],
    }

    self.stats = {
      'attacks_received': 0,
      'attacks_done': 0,
      'loots': 0,
      'kills': 0,
      'money' : 0,
      'mythic_stones' : 0
    }

  def isDataOK(self):
    #TODO Logging
    if self.name not in self.bot.rGameModesLootSlot or self.name not in self.bot.rGameModesSpawnRate or (self.interaction is None and self.name not in self.bot.rChannels):
      if self.name not in self.bot.rGameModesLootSlot:
        print(f"{self.name} not in rGameModesLootSlot")
      if self.name not in self.bot.rGameModesSpawnRate:
        print(f"{self.name} not in rGameModesSpawnRate")
      if self.name not in self.bot.rChannels:
        print(f"{self.name} not in rChannels")
      return False
    else:
      return True
  
  async def fetchOpponents(self, raritiestospawn, elementstospawn):
    #TODO MEttre ça dans le dB Manager
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():
        for i in self.Opponents:
          self.Opponents[i] = await conn.fetchrow(lib.qOpponents.SELECT_RANDOM_ADVANCED, raritiestospawn[i], elementstospawn[i])   
          self.LootTable[i] = await self.bot.dB.pull_loottable(self.Opponents[i]["name"], self.lootslot) 
  
  def getclassMonster(self):
    for i in self.Opponents:
      self.Opponents[i] = Monster(i, self, len(self.bot.ActiveList.active_slayers)+1)
      self.Opponents[i].LootTable = self.LootTable[i]

  async def constructGamemode(self):
    if self.isDataOK():
      raritiestospawn = []
      elementstospawn = []
      for i in range(self.spawns_count):
        self.Opponents[i] = {}
        self.LootTable[i] = {}
        #TODO Mettre ça dans le dB Manager
        raritiestospawn.append(random.choices(list(self.bot.rGameModesSpawnRate[self.name].keys()), list(self.bot.rGameModesSpawnRate[self.name].values()), k=1)[0])
        elementstospawn.append(random.choice(list(self.bot.Elements.keys())))
      await self.fetchOpponents(raritiestospawn, elementstospawn)
      self.getclassMonster()
      #Puis, on invoque:
      await self.spawnBattle()
    else:
      print("Gamemode impossible à load")

  async def spawnBattle(self, interaction=None):
    embed = lib.Embed.create_embed_battle(self)
    view = lib.BattleView(self) if self.Opponents[self.count].base_hp != 0 else None
    
    if interaction is None:
      if self.interaction is None:
        channel = self.bot.get_channel(self.bot.rChannels[self.name])
        view.message = await channel.send(content=self.role_tracker_content(), embed=embed, view=view)
        self.bot.ActiveList.add_battle(view.message.id, view)
      else:
        channel = self.bot.get_channel(self.interaction.channel.id)
        self.interaction = None
        view.message = await channel.send(content=self.role_tracker_content(), embed=embed, view=view)
        self.bot.ActiveList.add_battle(view.message.id, view)
    else:
      await interaction.message.edit(content=self.role_tracker_content(), embed=embed, view=view)

  async def getAttack(self, interaction, hit):
    #ON RECUPERE LES DONNEES
    Slayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
    
    Attack = lib.Attack(Slayer, self, hit)
    content, damage = await Attack.AttackHandler()

    #On update l'embed du combat
    #TODO REGISTER LE SLAYER DANS LA LISTE DES SLAYERS A UPDATE EN MASSE
    await self.bot.dB.push_slayer_data(Slayer.cSlayer)

    monster_killed = False
    if self.Opponents[self.count].base_hp == 0:
        if self.count == self.spawns_count - 1:
            self.end = True
        else:
            self.count += 1
            monster_killed = True

    #On clôture l'action
    return content, damage, monster_killed

  def role_tracker_content(self):
    #TODO Colonne dans gamemode pour activer ou non le roletracker -> Remplacer self.name == "" avec cette donnée
    if self.name == "" or self.bot.Rarities[self.Opponents[self.count].rarity].tracker_role_id == 0:
      return ""
    else:
      return f"<@&{self.bot.Rarities[self.Opponents[self.count].rarity].tracker_role_id}>"