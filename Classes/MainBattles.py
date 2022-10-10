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
    self.LootTable = {}

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
          self.LootTable[i] = await self.bot.dB.pull_loottable(self.Monsters[i]["element"], self.Monsters[i]["rarity"], self.lootslot) 
  
  def getclassMonster(self):
    for i in self.Monsters:
      self.Monsters[i] = Monster(i, self, self.bot.SlayerCount)
      print(self.Monsters[i].slayers_hits)

  async def constructGamemode(self):
    if self.isDataOK():
      raritiestospawn = []
      elementstospawn = []
      for i in range(self.spawns_count):
        self.Monsters[i] = {}
        self.LootTable[i] = {}
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

  async def getAttack(self, interaction, hit):
    #ON RECUPERE LES DONNEES
    Slayer = await self.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
    cMonster = self.Monsters[self.count]

    content = "**__Rapport de Combat :__**\n"

    #On check si on est vivant ou mort.
    if Slayer.cSlayer.isAlive()[0]:
      damage = [] 
      parries = []

      #Si on fait le spécial
      if hit == "S":
        if Slayer.cSlayer.canSpecial()[0]:
          for i in range(Slayer.cSlayer.getNbrHit()):
            attack = int(Slayer.cSlayer.dealDamage(hit, cMonster)[0])
            damage.append(attack)
            content += Slayer.cSlayer.dealDamage(hit, cMonster)[1]
            cMonster.getDamage(attack)
          
          #Spéciaux
            #PAIN
          attack, message, cMonster.last_hits = Slayer.cSlayer.Spe.pain(cMonster)
          if message != "":
            cMonster.getDamage(attack)
            damage.append(attack)
            content += message

          #RESETTIMER
          cMonster.slayers_hits, message = Slayer.cSlayer.Spe.resetTimer(cMonster)
          if message != "":
            content += message

          #Recap fin des attaques
          content += cMonster.recapDamageTaken(sum(damage))
          cMonster.storeLastHits(sum(damage))
          content += Slayer.cSlayer.useStacks(hit)
          dump = Slayer.cSlayer.recapStacks()
          content += cMonster.slayer_storeAttack(Slayer.cSlayer, sum(damage), hit)
        else:
          content += Slayer.cSlayer.canSpecial()[1]
        
      #Si on fait les autres attaques
      else:
        if cMonster.slayer_canAttack(Slayer.cSlayer)[0]:
          for i in range(Slayer.cSlayer.getNbrHit()):
            #On touche ou on fail ?
            isSuccess, message = Slayer.cSlayer.isSuccess(hit)
            if isSuccess:
              #on est parry ou on hit ?
              if cMonster.isParry(hit, Slayer):
                parry, message = cMonster.dealDamage(Slayer)
                Slayer.cSlayer.getDamage(parry)
                parries.append(parry)
                content += message
              else:
                attack, content = Slayer.cSlayer.dealDamage(hit, cMonster)
                damage.append(attack)
                cMonster.getDamage(attack)
            else:
              content += message

          #Recap fin des attaques
          if sum(damage) > 0:
            content += cMonster.recapDamageTaken(sum(damage))
            cMonster.storeLastHits(sum(damage))
            content += Slayer.cSlayer.recapStacks()
          if sum(parries) > 0:
            content += Slayer.cSlayer.recapHealth(parries)
          content += cMonster.slayer_storeAttack(Slayer.cSlayer, sum(damage), hit)

        else:
          content += cMonster.slayer_canAttack(Slayer.cSlayer)[1]

    else:
      content += Slayer.cSlayer.isAlive()[1]

    #On update l'embed du combat
    await self.bot.dB.push_slayer_data(Slayer.cSlayer)

    if self.Monsters[self.count].base_hp == 0:
        if self.count == self.spawns_count - 1:
            self.end = True
        else:
            self.count += 1

    #On clôture l'action
    return content

  async def calculateLoot(self):
    loots = {}
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
                    if slayer_id not in loots: loots[slayer_id] = []
                    loots[slayer_id].append(lib.random.choice(self.LootTable[i]))
    #On requete les items dans la dB
    await self.getrowLoot(loots)

  async def getrowLoot(self, loots):

    channel = self.bot.get_channel(self.bot.rChannels["loots"])
    money_request = []
    loots_request = []

    for slayer_id in loots:
      Slayer = await self.bot.ActiveList.get_Slayer(slayer_id, "")

      for row in loots[slayer_id]:

        cItem = lib.Item(row)

        #ON VEND AUTOMATIQUEMENT L'ITEM
        if Slayer.isinInventory(cItem.item_id):
          money_request.append((self.bot.rRarities[cItem.rarity]["price"], slayer_id))
          Slayer.addMoney(self.bot.rRarities[cItem.rarity]["price"])

          embed = lib.Embed.create_embed_money_loot(self.bot, Slayer, cItem)
          view = lib.LootView(self.bot, Slayer, cItem)
          view.message = await channel.send(content=f"<@{slayer_id}>", embed=embed, view=view)

        #ON AJOUTE DANS LA DB INVENTAIRE
        else:
          loots_request.append((slayer_id, cItem.item_id, 1, False))
          Slayer.addtoInventory(cItem)

          await self.bot.ActiveList.update_interface(slayer_id, "inventaire")

          embed = lib.Embed.create_embed_new_loot(self.bot, Slayer, cItem)
          view = lib.LootView(self.bot, Slayer, cItem, True)
          await self.bot.ActiveList.add_interface(slayer_id, cItem.item_id, view)
          view.message = await channel.send(content=f"<@{slayer_id}>", embed=embed, view=view)

    await self.bot.dB.push_loots_money(loots_request, money_request)

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

  def dealDamage(self, Slayer):
    armor = int(self.reduceArmor(Slayer.cSlayer.stats["total_armor"]))
    damage = int(self.damage)
    #Armor
    damage = int(max(damage * 1000/(1000+armor), 0))
    #Max HP
    damage = int(min(damage, Slayer.cSlayer.stats["total_max_health"] - Slayer.cSlayer.damage_taken))
    return damage, f"\n> - Attaque contrée : Le monstre t'a infligé {int(damage)} dégâts"

  def reduceArmor(self, armor):
      armor = max((int(armor*(1-float(self.letality_per)))-int(self.letality)), 0)
      return int(armor)

  def storeLastHits(self, damage):
    self.last_hits.append(damage)
    if len(self.last_hits) > 10:
      self.last_hits.pop(0)

  def isParry(self, hit, Slayer):
    ParryChance = min(max(self.parry[f"parry_chance_{hit}"] - Slayer.cSlayer.stats[f"total_parry_{hit}"], 0), 1)
    isParry = random.choices(population=[True, False], weights=[ParryChance, 1-ParryChance], k=1)[0]
    if isParry:
      return True
    else:
      return False

  def getDamage(self, damage):
    self.base_hp -= int(damage)

  def recapDamageTaken(self, damage):  
    if self.base_hp == 0:
      return f"\n\n> Le monstre est mort ! 💀"
    else:
      return f"\n\n> Le monstre possède désormais {int(self.base_hp)}/{int(self.total_hp)} ❤️"

  def slayer_canAttack(self, cSlayer):
    if cSlayer.slayer_id in self.slayers_hits:
      if self.slayers_hits[cSlayer.slayer_id].canAttack():
        return True, ""
      else:
        return False, f"> Pas si vite ! Prends ton temps ! Prochaine attaque disponible dans **{int(self.slayers_hits[cSlayer.slayer_id].timestamp_next_hit - lib.datetime.datetime.timestamp(lib.datetime.datetime.now()))}s**"
    else:
      return True, ""

  def slayer_storeAttack(self, cSlayer, damage, hit):
    if cSlayer.slayer_id in self.slayers_hits:
      self.slayers_hits[cSlayer.slayer_id].updateClass(damage, None if hit == "S" else cSlayer.stats["total_cooldown"], cSlayer.stats["total_luck"])
    else:
      self.slayers_hits[cSlayer.slayer_id] = lib.DamageDone(0 if hit == "S" else cSlayer.stats["total_cooldown"], damage if damage > 0 else 0, True if damage > 0 else False, cSlayer.stats["total_luck"])
    content = self.slayers_hits[cSlayer.slayer_id].checkStatus(damage, self.base_hp)
    return content