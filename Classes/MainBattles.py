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
    self.Monsters = {}
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
  
  async def fetchMonsters(self, raritiestospawn, elementstospawn):
    #TODO MEttre ça dans le dB Manager
    async with self.bot.db_pool.acquire() as conn:
      async with conn.transaction():
        for i in self.Monsters:
          self.Monsters[i] = await conn.fetchrow(lib.qMonsters.SELECT_RANDOM_ADVANCED, raritiestospawn[i], elementstospawn[i])   
          self.LootTable[i] = await self.bot.dB.pull_loottable(self.Monsters[i]["name"], self.lootslot) 
  
  def getclassMonster(self):
    for i in self.Monsters:
      self.Monsters[i] = Monster(i, self, len(self.bot.ActiveList.active_slayers)+1)

  async def constructGamemode(self):
    if self.isDataOK():
      raritiestospawn = []
      elementstospawn = []
      for i in range(self.spawns_count):
        self.Monsters[i] = {}
        self.LootTable[i] = {}
        #TODO Mettre ça dans le dB Manager
        raritiestospawn.append(random.choices(list(self.bot.rGameModesSpawnRate[self.name].keys()), list(self.bot.rGameModesSpawnRate[self.name].values()), k=1)[0])
        elementstospawn.append(random.choice(list(self.bot.Elements.keys())))
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
    cMonster = self.Monsters[self.count]

    content = "**__Rapport de Combat :__**"
    damage = [] 
    parries = []

    #On check si on est vivant ou mort.
    if Slayer.cSlayer.isAlive()[0]:

      #Si on fait le spécial
      if hit == "s":
        if Slayer.cSlayer.canSpecial()[0]:
          Slayer.cSlayer.useStacks(hit)
          if Slayer.cSlayer.Spe.id != 8: #Berserker
            for i in range(Slayer.cSlayer.getNbrHit()):
              attack, contents = Slayer.cSlayer.dealDamage(hit, cMonster)

              #Pet crit
              if "‼️" in contents:
                await Slayer.getPet(rate=0.004, pets=[230])

              content += contents
              damage.append(attack)
              cMonster.getDamage(attack)

            #Recap fin des attaques
            content += cMonster.recapDamageTaken(sum(damage))
            cMonster.storeLastHits(sum(damage), Slayer.cSlayer.Spe)
            content += Slayer.cSlayer.recap_useStacks(hit)
            dump = Slayer.cSlayer.recapStacks()
            self.stats['attacks_received'] += 1
            content += cMonster.slayer_storeAttack(Slayer.cSlayer, sum(damage), hit)

            #Achievement Biggest_Hit
            await Slayer.update_biggest_hit(sum(damage))

          else: #Berserker activé:
            content += "\n> Vous avez activé le mode Berserker, vous obtenez 100% Chance Critique et 200% Dégâts Critiques pendant 5 coups !"
            content += Slayer.cSlayer.recap_useStacks(hit)
            Slayer.cSlayer.berserker_mode = 5
            Slayer.cSlayer.calculateStats(self.bot.rBaseBonuses)
        else:
          content += Slayer.cSlayer.canSpecial()[1]
        
      #Si on fait les autres attaques
      else:
        if cMonster.slayer_canAttack(Slayer.cSlayer)[0]:
          for i in range(Slayer.cSlayer.getNbrHit()):
            #On touche ou on fail ?
            ## TODO Mettre un Walrus Operator ici
            isSuccess, message = Slayer.cSlayer.isSuccess(hit)
            if isSuccess:
              #on est parry ou on hit ?
              if cMonster.isParry(hit, Slayer):
                parry, message = cMonster.dealDamage(Slayer)
                Slayer.cSlayer.getDamage(parry)
                parries.append(parry)
                content += message
              else:
                attack, contents = Slayer.cSlayer.dealDamage(hit, cMonster)
                #Pet crit
                if "‼️" in contents:
                  await Slayer.getPet(rate=0.004, pets=[230])

                content += contents
                damage.append(attack)
                cMonster.getDamage(attack)
            else:
              content += message

          #Recap fin des attaques
          if sum(damage) > 0:
            await Slayer.getPet(pets=[194])
            content += cMonster.recapDamageTaken(sum(damage))
            cMonster.storeLastHits(sum(damage), Slayer.cSlayer.Spe)
            content += Slayer.cSlayer.recapStacks()
            self.stats['attacks_received'] += 1
            
            #Achievement Biggest_Hit
            await Slayer.update_biggest_hit(sum(damage))

          if sum(parries) > 0:
            await Slayer.getPet(pets=[193])
            isDead, message = Slayer.cSlayer.recapHealth(parries)
            content += message
            self.stats['attacks_done'] += sum(parries)
            if isDead:
              self.stats['kills'] += 1
          content += cMonster.slayer_storeAttack(Slayer.cSlayer, sum(damage), hit)

        else:
          content += cMonster.slayer_canAttack(Slayer.cSlayer)[1]

    else:
      content += Slayer.cSlayer.isAlive()[1]

    #On update l'embed du combat
    await self.bot.dB.push_slayer_data(Slayer.cSlayer)

    monster_killed = False
    if self.Monsters[self.count].base_hp == 0:
        if self.count == self.spawns_count - 1:
            self.end = True
        else:
            self.count += 1
            monster_killed = True

    #On clôture l'action
    return content, damage, monster_killed

  async def calculateLoot(self):
    loots = {}
    behemoths_killed_achievement_request = []
    mythic_stones_request = []
    #On fait le tour des Monstres.
    for i in self.Monsters:
      if self.Monsters[i].base_hp == 0: #and len(self.LootTable[i]) > 0:
        #On fait le tour de tous les slayers ayant attaqué
        for id in self.Monsters[i].slayers_hits:
            #On ne considère que les éligibles
            if self.Monsters[i].slayers_hits[id].eligible:
                
                #On crée le storage des loots money / items / stones
                #Achievement Behemoths Killed
                Slayer = await self.bot.ActiveList.get_Slayer(id, "")
                Slayer.cSlayer.achievements["monsters_killed"] += 1
                behemoths_killed_achievement_request.append((1, id))
                if self.Monsters[i].rarity == "mythic":
                  stones_earned = lib.random.randint(1,3)
                  Slayer.cSlayer.inventory_gatherables[5] += stones_earned
                  mythic_stones_request.append((id, 5, stones_earned))
                  self.stats["mythic_stones"] += stones_earned

                  #mythic stone
                  if id not in self.loots: self.loots[id] = {}
                  if "mythic_stones" not in self.loots[id]: self.loots[id]["mythic_stones"] = 0
                  self.loots[id]["mythic_stones"] += stones_earned

                #On prend en compte le roll_dice
                for j in range(self.Monsters[i].roll_dices):
                  #On calcule le loot obtenu
                  isLoot = random.choices(population=[True, False], weights=[self.Monsters[i].slayers_hits[id].luck, 1-self.Monsters[i].slayers_hits[id].luck], k=1)[0]
                  if isLoot:

                    if id not in loots: loots[id] = []
                    loots[id].append(lib.random.choice(self.LootTable[i]))

    #Achievement Behemoths Killed
    await self.bot.dB.push_behemoths_killed_achievement(behemoths_killed_achievement_request)
    if self.Monsters[i].rarity == "mythic":
      await self.bot.dB.push_MythicStones(mythic_stones_request)
    #On requete les items dans la dB
    await self.getrowLoot(loots)

  async def getrowLoot(self, loots):

    money_request = []
    loots_request = []

    for id in loots:
      Slayer = await self.bot.ActiveList.get_Slayer(id, "")
      if id not in self.loots: self.loots[id] = {}
      if "items" not in self.loots[id]: self.loots[id]["items"] = []
      if "money" not in self.loots[id]: self.loots[id]["money"] = 0

      for row in loots[id]:

        cItem = lib.Item(row, self.bot)

        #ON VEND AUTOMATIQUEMENT L'ITEM
        if Slayer.isinInventory(cItem.id):
          self.stats["money"] += self.bot.Rarities[cItem.rarity].price
          money_request.append((self.bot.Rarities[cItem.rarity].price, id))
          Slayer.addMoney(self.bot.Rarities[cItem.rarity].price)
          self.loots[id]["money"] += self.bot.Rarities[cItem.rarity].price

        #ON AJOUTE DANS LA DB INVENTAIRE
        else:
          self.stats["loots"] += 1
          loots_request.append((id, cItem.id, 1, False))
          Slayer.addtoInventory(cItem)
          await self.bot.ActiveList.update_interface(id, "inventaire")
          self.loots[id]["items"].append(cItem)

    await self.bot.dB.push_loots_money(loots_request, money_request)

  def role_tracker_content(self):
    #TODO Colonne dans gamemode pour activer ou non le roletracker -> Remplacer self.name == "" avec cette donnée
    if self.name == "" or self.bot.Rarities[self.Monsters[self.count].rarity].tracker_role_id == 0:
      return ""
    else:
      return f"<@&{self.bot.Rarities[self.Monsters[self.count].rarity].tracker_role_id}>"