import random
import os
import inspect
import sys

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

    self.stats = {
      'attacks': 0,
      'damage': 0,
      'loots': 0,
      'kills': 0,
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
      self.Monsters[i] = Monster(i, self, self.bot.SlayerCount)

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
      await self.spawnBattle()
    else:
      print("Gamemode impossible à load")

  async def spawnBattle(self, interaction=None):
    embed = lib.Embed.create_embed_battle(self)
    view = lib.BattleView(self) if self.Monsters[self.count].base_hp != 0 else None
    if interaction is None:
      if self.interaction is None:
        channel = self.bot.get_channel(self.bot.rChannels[self.name])
        view.message = await channel.send(embed=embed, view=view)
      else:
        view.interaction = self.interaction
        await self.interaction.response.send_message(embed=embed, view=view, ephemeral=False)
    else:
      await interaction.message.edit(embed=embed, view=view)

  async def getAttack(self, interaction, Hit):

    canAttack = False
    ephemeral_message = "ERREUR"
    Damage = 0

    Slayer, InterfaceReady = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name, "battle")
    if InterfaceReady:
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
            self.stats["attacks"] += 1
            Damage, Stacks_Earned = Slayer.cSlayer.CalculateDamage(Hit, self.Monsters[self.count])
            self.Monsters[self.count].slayers_hits[interaction.user.id].updateClass(Damage, None if Hit == "S" else Slayer.cSlayer.stats["total_cooldown"], Slayer.cSlayer.stats["total_luck"])
            if Damage > 0:
              self.Monsters[self.count].base_hp = max(0, self.Monsters[self.count].base_hp - Damage)
              #SI ON INFLIGE DES DEGATS
              ephemeral_message = lib.Ephemeral.get_ephemeralAttack(Damage, Stacks_Earned, Hit, Slayer.cSlayer, self, interaction.user.id, canAttack) 
              await self.updateBattle(Damage, Slayer, interaction)
            else:
              #SI FAIL OU PARRY
              if Damage < 0:
                if Slayer.cSlayer.dead == True:
                  self.stats["kills"] += 1
                self.stats["damage"] += abs(Damage)
              ephemeral_message = lib.Ephemeral.get_ephemeralAttack(Damage, Stacks_Earned, Hit, Slayer.cSlayer, self, interaction.user.id, canAttack) 
        else:
            #SI ON PEUT PAS ATTAQUER
            ephemeral_message = lib.Ephemeral.get_ephemeralAttack(0, 0, Hit, Slayer.cSlayer, self, interaction.user.id, canAttack) 
      else:
          #SI ON EST MORT
          ephemeral_message = lib.Ephemeral.get_ephemeralAttack(0, 0, Hit, Slayer.cSlayer, self, interaction.user.id, canAttack)  
      
      #Si Damage > 0 on a infligé donc stacks / si Damage < 0, on a subi, donc damage_taken à mettre à jour
      if Damage != 0:
          await Slayer.push_dB_Slayer()
      await interaction.response.send_message(f'{ephemeral_message}', ephemeral=True)
    else:
      await interaction.response.send_message("Une interface est déjà ouverte", ephemeral=True)

    self.bot.ActiveList.close_interface(interaction.user.id, "battle")
    return self.end

  async def updateBattle(self, Damage, Slayer, interaction):
    if self.Monsters[self.count].base_hp == 0:
      if self.count == self.spawns_count - 1:
        self.end = True
      else:
        self.count += 1
    await self.spawnBattle(interaction)

  async def endBattle(self, message, isEnd=True):
    embed = lib.Embed.create_embed_end_battle(self, isEnd)
    await message.edit(embed=embed, view=None)

  async def calculateLoot(self):
    requests = {}
    k = 0
    #On fait le tour des Monstres.
    for i in self.Monsters:
      if self.Monsters[i].base_hp == 0:
        #On fait le tour de tous les slayers ayant attaqué
        for slayer_id in self.Monsters[i].slayers_hits:
            #On ne considère que les éligibles
            if self.Monsters[i].slayers_hits[slayer_id].eligible:
                #On prend en compte le roll_dice
                for j in range(self.Monsters[i].roll_dices):
                  #On calcule le loot obtenu
                  isLoot = random.choices(population=[True, False], weights=[self.Monsters[i].slayers_hits[slayer_id].luck, 1-self.Monsters[i].slayers_hits[slayer_id].luck], k=1)[0]
                  if isLoot:
                    self.stats["loots"] += 1
                    loot_rarity = random.choices(population=list(self.bot.rRaritiesLootRate[self.Monsters[i].rarity].keys()), weights=list(self.bot.rRaritiesLootRate[self.Monsters[i].rarity].values()), k=1)[0]
                    requests[k] = {}
                    requests[k]["slayer-id"], requests[k]["element"], requests[k]["rarity"], requests[k]["loot"], requests[k]["already"] = slayer_id, self.Monsters[i].element, loot_rarity, None, False
                    k += 1
    await self.getrowLoot(requests)

  async def getrowLoot(self, requests):
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():
        for k in requests:
          #COMMENT FAIRE POUR RAJOUTER L'ITEM SUR LE SLAYER SI IL EXISTE PAS DEJA ? ET RECUP L'INFO POUR LE MESSAGE FINAL
          requests[k]["loot"] = await conn.fetchrow(lib.qItems.SELECT_RANDOM, requests[k]["rarity"], requests[k]["element"], self.lootslot)
          isAlready = await conn.fetchval(lib.qSlayersInventoryItems.SELECT_ALREADY, requests[k]["slayer-id"], requests[k]["loot"]["id"])
          if isAlready == None:
            if requests[k]["slayer-id"] in self.bot.ActiveList.active_slayers:
              self.bot.ActiveList.active_slayers[requests[k]["slayer-id"]].Slayer.cSlayer.inventory_items.append(lib.Item(requests[k]["loot"]))
            await conn.execute(f'INSERT INTO "Slayers_Inventory_Items" (slayer_id, item_id) VALUES ({requests[k]["slayer-id"]}, {requests[k]["loot"]["id"]})')
          else:
            requests[k]["already"] = True
            await conn.execute(f'UPDATE "Slayers" SET money = money + {self.bot.rRarities[requests[k]["rarity"]]["price"]} WHERE slayer_id = {requests[k]["slayer-id"]}')

    await self.distribLoot(requests)

  async def distribLoot(self, requests):
    #Embed and view
    channel = self.bot.get_channel(self.bot.rChannels["loots"])
    for k in requests:
      embed = lib.Embed.create_embed_loot(requests[k])
      view = lib.LootView(self.bot, requests[k])
      view.message = await channel.send(content=f"<@{requests[k]['slayer-id']}>", embed=embed, view=view)

class Monster:
  def __init__(
    self, 
    i,
    Battle,
    hp_scaling
    ):
    self.name = Battle.Monsters[i]["name"]
    self.description = Battle.Monsters[i]["description"]
    self.element = Battle.Monsters[i]["element"]
    self.base_hp = Battle.Monsters[i]["base_hp"] * hp_scaling * Battle.scaling["hp"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"])
    self.total_hp = Battle.Monsters[i]["base_hp"] * hp_scaling * Battle.scaling["hp"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"])
    self.rarity = Battle.Monsters[i]["rarity"]
    self.parry = {
      "parry_chance_L" : float(Battle.Monsters[i]["parry_chance_L"]) * int(Battle.scaling["parry"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"])),
      "parry_chance_H" : float(Battle.Monsters[i]["parry_chance_H"]) * int(Battle.scaling["parry"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"])),
      "parry_chance_S" : 0
    }
    self.damage = Battle.Monsters[i]["damage"] * Battle.scaling["damage"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"])
    self.letality = Battle.Monsters[i]["letality"] * Battle.scaling["letality"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"])
    self.letality_per = Battle.Monsters[i]["letality_per"] * Battle.scaling["letality"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"])
    self.armor = Battle.Monsters[i]["armor"] * Battle.scaling["armor"] * (1 + i * float(Battle.bot.rBaseBonuses["mult_battle"]))
    self.protect_crit = Battle.Monsters[i]["protect_crit"] * Battle.scaling["protect_crit"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"])
    self.img_url_normal = Battle.Monsters[i]["img_url_normal"]
    self.img_url_enraged = Battle.Monsters[i]["img_url_enraged"]
    self.bg_url = Battle.Monsters[i]["bg_url"]
    self.roll_dices = random.randint(Battle.min_dice, Battle.max_dice)

    self.last_hits = []
    self.slayers_hits = {}