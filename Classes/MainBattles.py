import random
import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import lib

class Gamemode:
  def __init__(
    self, 
    bot,
    gamemode,
    interaction=None
    ):
    self.bot = bot
    self.end = False
    self.name = gamemode["name"]
    self.min_dice = gamemode["roll_dices_min"]
    self.max_dice = gamemode["roll_dices_max"]
    self.interaction = interaction

    #Gestion du nombre de spawns
    self.spawns_count = gamemode["spawns_count"]
    self.count = 0
    self.Monsters = {}

    self.scaling = {
      'hp': gamemode["hp_scaling"],
      'armor': gamemode["armor_scaling"],
      'letality': gamemode["letality_scaling"],
      'parry': gamemode["parry_scaling"],
      'damage': gamemode["damage_scaling"],
      'protect_crit': gamemode["protect_crit_scaling"],
    }

  def isDataOK(self):
    if self.name not in self.bot.rGameModesLootSlot or self.name not in self.bot.rGameModesSpawnRate or (self.interaction is None and self.name not in self.bot.rChannels):
      return False
    else:
      return True
  
  async def fetchMonsters(self, raritiestospawn, elementstospawn):
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():
        for i in self.Monsters:
          self.Monsters[i] = await conn.fetchrow(lib.qMonsters.SELECT_RANDOM_ADVANCED, raritiestospawn[i], elementstospawn[i])    
  
  def getclassMonster(self):
    for i in self.Monsters:
      self.Monsters[i] = Monster(self.Monsters[i], self, self.bot.SlayerCount)

  async def constructGamemode(self):
    if self.isDataOK():
      raritiestospawn = []
      elementstospawn = []
      for i in range(self.spawns_count):
        self.Monsters[i] = {}
        raritiestospawn.append(random.choices(list(self.bot.rGameModesSpawnRate[self.name].keys()), list(self.bot.rGameModesSpawnRate[self.name].values()), k=1)[0])
        elementstospawn.append(random.choice(list(self.bot.rElements.keys())))
      await self.fetchMonsters(raritiestospawn, elementstospawn)
      self.getclassMonster()
      #Puis, on invoque:
      await self.spawnMonster()
    else:
      print("Gamemode impossible à load")

  async def spawnMonster(self, interaction=None):
    embed = lib.Embed.create_embed_spawn(self)
    view = lib.Buttons.Buttons_Battle(self) if self.Monsters[self.count].base_hp != 0 else None
    if interaction is None:
      if self.interaction is None:
        channel = self.bot.get_channel(self.bot.rChannels[self.name])
        message = await channel.send(embed=embed, view=view)
      else:
        await self.interaction.response.send_message(embed=embed, view=view, ephemeral=False)
    else:
      await interaction.message.edit(embed=embed, view=view)

  async def getAttack(self, interaction, Hit):

    canAttack = False
    ephemeral_message = "ERREUR"

    #On init le Slayer
    Slayer = lib.MSlayer(self.bot, interaction)
    await Slayer.constructClass()

    if Slayer.cSlayer.dead == False:
      #On documente la Class DamageDone
      if interaction.user.id not in self.Monsters[self.count].slayers_hits:
        self.Monsters[self.count].slayers_hits[interaction.user.id] = lib.DamageDone(eligible=False, total_damage=0, timestamp_next_hit=lib.datetime.datetime.timestamp(lib.datetime.datetime.now()))
        canAttack = True
      elif self.Monsters[self.count].slayers_hits[interaction.user.id].timestamp_next_hit < lib.datetime.datetime.timestamp(lib.datetime.datetime.now()):
        canAttack = True
      else:
        canAttack = False

      if (canAttack and Hit != "S") or (Hit == "S" and Slayer.cSlayer.canSpecial()):
          Damage, Stacks_Earned = Slayer.cSlayer.CalculateDamage(Hit, self.Monsters[self.count])
          self.Monsters[self.count].slayers_hits[interaction.user.id].updateClass(Damage, None if Hit == "S" else Slayer.cSlayer.stats["total_cooldown"])
          if Damage > 0:
            self.Monsters[self.count].base_hp = max(0, self.Monsters[self.count].base_hp - Damage)
            #SI ON INFLIGE DES DEGATS
            ephemeral_message = lib.Ephemeral.get_ephemeralAttack(Damage, Stacks_Earned, Hit, Slayer.cSlayer, self, interaction.user.id, canAttack) 
            await self.updateBattle(Damage, Slayer, interaction)
          else:
            #SI FAIL OU PARRY
            ephemeral_message = lib.Ephemeral.get_ephemeralAttack(Damage, Stacks_Earned, Hit, Slayer.cSlayer, self, interaction.user.id, canAttack) 
      else:
          #SI ON PEUT PAS ATTAQUER
          ephemeral_message = lib.Ephemeral.get_ephemeralAttack(0, 0, Hit, Slayer.cSlayer, self, interaction.user.id, canAttack) 
    else:
        #SI ON EST MORT
        ephemeral_message = lib.Ephemeral.get_ephemeralAttack(0, 0, Hit, Slayer.cSlayer, self, interaction.user.id, canAttack)  
    
    #Si Damage > 0 on a infligé donc stacks / si Damage < 0, on a subi, donc damage_taken à mettre à jour
    if Damage != 0:
        Slayer.Slayer_update()
        await Slayer.pushdB()
    await interaction.response.send_message(f'{ephemeral_message}', ephemeral=True)

    return self.end

  async def updateBattle(self, Damage, Slayer, interaction):
    if self.Monsters[self.count].base_hp == 0:
      if self.count == self.spawns_count - 1:
        self.end = True
      else:
        self.count += 1
    await self.spawnMonster(interaction)

  async def calculateLoot(self):
    pass

class Monster:
  def __init__(
    self, 
    rMonster,
    Gamemode,
    hp_scaling
    ):
    self.name = rMonster["name"]
    self.description = rMonster["description"]
    self.element = rMonster["element"]
    self.base_hp = rMonster["base_hp"] * hp_scaling * Gamemode.scaling["hp"]
    self.total_hp = rMonster["base_hp"] * hp_scaling * Gamemode.scaling["hp"]
    self.rarity = rMonster["rarity"]
    self.parry = {
      "parry_chance_L" : float(rMonster["parry_chance_L"]) * int(Gamemode.scaling["parry"]),
      "parry_chance_H" : float(rMonster["parry_chance_H"]) * int(Gamemode.scaling["parry"]),
      "parry_chance_S" : 0
    }
    self.damage = rMonster["damage"] * Gamemode.scaling["damage"]
    self.letality = rMonster["letality"] * Gamemode.scaling["letality"]
    self.letality_per = rMonster["letality_per"] * Gamemode.scaling["letality"]
    self.armor = rMonster["armor"] * Gamemode.scaling["armor"]
    self.protect_crit = rMonster["protect_crit"] * Gamemode.scaling["protect_crit"]
    self.img_url_normal = rMonster["img_url_normal"]
    self.img_url_enraged = rMonster["img_url_enraged"]
    self.bg_url = rMonster["bg_url"]
    self.roll_dices = random.randint(Gamemode.min_dice, Gamemode.max_dice)

    self.last_hits = []
    self.slayers_hits = {}