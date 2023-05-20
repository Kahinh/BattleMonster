import random
from Classes.Objects import Item, Mythic
from Classes.Opponents import Monster, Banner, Mythique1, Mythique2, Mythique3, Mythique4, Mythique5, Mythique6

import logging
logging.basicConfig(filename='logs.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s') 

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import lib

#TODO @dataclass
class Gamemode:
  def __init__(self, bot, gamemodedata):
    self.bot = bot

    #Données de base
    self.name = gamemodedata["name"]
    self.type = gamemodedata["type"]
    self.role_tracker_activated = gamemodedata["role_tracker_activated"]
    self.min_dice = gamemodedata["min_dice"]
    self.max_dice = gamemodedata["max_dice"]
    self.stats = {
      'attacks_received': 0,
      'attacks_done': 0,
      'loots': 0,
      'kills': 0,
      'money' : 0,
      'mythic_stones' : 0
    }
    self.scaling = {
      'hp': gamemodedata["hp_scaling"],
      'armor': gamemodedata["armor_scaling"],
      'letality': gamemodedata["letality_scaling"],
      'parry': gamemodedata["parry_scaling"],
      'damage': gamemodedata["damage_scaling"],
      'protect_crit': gamemodedata["protect_crit_scaling"],
    }
    
    #Données opponent
    self.spawns_count = gamemodedata["spawns_count"]
    self.count = 0

    #A calculer
    self.lootslot = []
    self.spawnrate = {}
    self.Opponents = []

    #Butin
    self.storage_loots = {}
  
  def isReady(self):
    if self.lootslot == []:
      logging.warning(f"NO LOOTSLOT FOR GAMEMODE {self.name}")
      return False
    if self.spawnrate == {}:
      logging.warning(f"NO SPAWNRATE FOR GAMEMODE {self.name}")
      return False
    if self.Opponents == []:
      logging.warning(f"NO OPPONENTS FOR GAMEMODE {self.name}")
      return False
    return True

  def role_tracker_content(self):
    if self.role_tracker_activated and self.bot.Rarities[self.Opponents[self.count].rarity].tracker_role_id != 0:
      return f"<@&{self.bot.Rarities[self.Opponents[self.count].rarity].tracker_role_id}>"
    else:
      return ""

  async def handler_Spawn(self):
    embed = lib.Embed.create_embed_battle(self)
    view = lib.BattleView(self) if self.Opponents[self.count].base_hp != 0 else None
    channel = self.bot.get_channel(self.bot.rChannels[self.name])
    view.message = await channel.send(content=self.role_tracker_content(), embed=embed, view=view)
    self.bot.ActiveList.add_battle(view.message.id, view)

  async def handler_Build(self):
    await pullGamemodeLootSlot()
    await pullGamemodeSpawnRate()
    await createOpponents()

    async def pullGamemodeLootSlot(self):
      rlootslot = await self.bot.dB.pull_GamemodeLootSlot(self.name)
      for row in rlootslot:
        self.lootslot.append(row["slot"])
    
    async def pullGamemodeSpawnRate(self):
      rspawnrate = await self.bot.dB.pullGamemodeSpawnRate(self.name)
      for row in rspawnrate:
        self.spawnrate.update({[row["rarities"]]:float(row["spawn_rate"])})

    async def createOpponents(self):
      for i in range(self.spawns_count):
        if self.type == "factionwar":
          rarity = random.choices(list(self.spawnrate.keys()), list(self.spawnrate.values()), k=1)[0]
          banner = await Banner(self.gamemode, "neutral", rarity, "banner").handler_Build()
          self.Opponents.append(banner)
        else:
          rarity = random.choices(list(self.spawnrate.keys()), list(self.spawnrate.values()), k=1)[0]
          element = random.choice(list(self.bot.Elements.keys()))
          type = "monster"
          if rarity == "mythic":
            mythic = random.choice([ \
              Mythique1(self.gamemode, element, rarity, type), \
              Mythique2(self.gamemode, element, rarity, type), \
              Mythique3(self.gamemode, element, rarity, type), \
              Mythique4(self.gamemode, element, rarity, type), \
              Mythique5(self.gamemode, element, rarity, type), \
              Mythique6(self.gamemode, element, rarity, type)])
            mythic = mythic.handler_Build()
            self.Opponents.append(mythic)
          else:
            monster = await Monster(self.gamemode, element, rarity, type).handler_Build()
            self.Opponents.append(monster)

  async def handler_Loot(self):
  #On crée les requests à la dB
    request_opponents_killed_achievement = []
    request_mythic_stones = []
    request_money = []
    request_items = []

    async def push_dB_request(self):
      await self.bot.dB.push_behemoths_killed_achievement(request_opponents_killed_achievement)
      await self.bot.dB.push_MythicStones(request_mythic_stones)
      await self.bot.dB.push_loots(request_items)
      await self.bot.dB.push_money(request_money)

    async def review_loots(self):
      for id in self.storage_loots:
        Slayer = await self.bot.ActiveList.get_Slayer(id, "")
        storage_loot_handler(Slayer)
        for row in self.storage_loots[Slayer.cSlayer.id]["loots"]:
          
          if row["rarity"] == "mythic":
            cItem = Mythic(self.bot, row)
          else:
            cItem = Item(self.bot, row)

          #ON VEND AUTOMATIQUEMENT L'ITEM
          if Slayer.isinInventory(cItem.id):
            auto_sellItem(Slayer, cItem)
          #ON AJOUTE DANS LA DB INVENTAIRE
          else:
            auto_addtoinventoryItem(Slayer, cItem)

    def auto_sellItem(self, Slayer, cItem):
      #On rajoute la monnaie dans la Class Slayer
      Slayer.addMoney(self.bot.Rarities[cItem.rarity].price)

      #On store le give money
      self.storage_loots[Slayer.cSlayer.id]["money"] += self.bot.Rarities[cItem.rarity].price
      request_money.append((self.bot.Rarities[cItem.rarity].price, Slayer.cSlayer.id))

      #Puis on ajoute la monnaie gagnée au Battle
      self.stats["money"] += self.bot.Rarities[cItem.rarity].price

    def auto_addtoinventoryItem(self, Slayer, cItem):
      #On rajoute l'item dans la Class Slayer
      Slayer.addtoInventory(cItem)
      #On store le give item
      request_items.append((Slayer.cSlayer.id, cItem.id, 1, False))
      self.storage_loots[Slayer.cSlayer.id]["items"].append(cItem)
      #Puis on ajoute l'item gagné au Battle
      self.stats["loots"] += 1

    def award_loots(self, Slayer, cOpponent):
      #On prend en compte le roll_dice
      for j in range(cOpponent.roll_dices):
        #On calcule le loot obtenu
        if random.choices(population=[True, False], weights=[cOpponent.slayers_hits[Slayer.cSlayer.id].luck, 1-cOpponent.slayers_hits[Slayer.cSlayer.id].luck], k=1)[0]:
          
          #On positionne dans le storage_loot
          storage_loot_handler(Slayer)
          self.storage_loots[Slayer.cSlayer.id]["loots"].append(random.choice(cOpponent.LootTable))

    def achievement_opponents_killed(self, Slayer):
      Slayer.cSlayer.achievements["monsters_killed"] += 1
      request_opponents_killed_achievement.append((1, Slayer.cSlayer.id))

    def award_mythics_stones(self, Slayer):
        #Mythic Stones = gatherable 5
        stones_earned = random.randint(1,3)
        Slayer.cSlayer.inventory_gatherables[5] += stones_earned
        request_mythic_stones.append((Slayer.cSlayer.id, 5, stones_earned))
        self.stats["mythic_stones"] += stones_earned

        #On positionne dans le storage_loot
        storage_loot_handler(Slayer)
        self.storage_loots[Slayer.cSlayer.id]["mythic_stones"] += stones_earned

    def storage_loot_handler(self, Slayer):
      if Slayer.cSlayer.id not in self.storage_loots:
        self.storage_loots[Slayer.cSlayer.id] = {
          "mythic_stones": 0,
          "items" : [],
          "money" : 0,
          "loots" : []
        }

    #On check les monstres 1 par 1
    for i in self.Opponents:
      cOpponent = self.Opponents[i]
      if cOpponent.base_hp == 0 and cOpponent.loot_table != []:
        #On fait le tour de tous les slayers ayant attaqué
        for id in cOpponent.slayers_hits:
            #On ne considère que les éligibles
            if cOpponent.slayers_hits[id].eligible:
              #On récupère le Slayer
              Slayer = await self.bot.ActiveList.get_Slayer(id, "")
              #On distribue l'achievement Monsters killed
              achievement_opponents_killed(Slayer)
              #On distribue les mythiques
              if cOpponent.rarity == "mythic":
                award_mythics_stones(Slayer, cOpponent)
              #On distribue les loots
              award_loots(Slayer, cOpponent)

              #On revoit les butins : AutoVente ou vrai distrib ?
              await review_loots()

              #On push via le dB Manager
              await push_dB_request()

  async def handler_Attack(self, Slayer, hit):

    #Simplification des args
    cOpponent = self.Opponents[self.count]
    cSlayer = Slayer.cSlayer

    #Initiation du content
    content = "**__Rapport de Combat :__**"
    total_damage_dealt = 0
    total_damage_taken = 0

    #Init des coups
    hits = []

    #On check si on est vivant ou mort.
    if (isAlive := cSlayer.isAlive()) and not isAlive[0]:
      return isAlive[1], 0
    
    #On peut special
    if (canSpecial := cSlayer.canSpecial()) and not canSpecial[0] and hit == "S":
      return canSpecial[1], 0
      
    #On peut attaquer selon le timing
    if (canAttack := cOpponent.slayer_canAttack(cSlayer)) and not canAttack[0] and hit != "S":
      return canAttack[1], 0
    
    #Spe Berserker
    if hit == "S" and cSlayer.Spe.id == 8:
      cSlayer.berserker_mode = 5
      cSlayer.calculateStats(self.bot.rBaseBonuses)
      content = "\n> Vous avez activé le mode Berserker, vous obtenez 100% Chance Critique et 200% Dégâts Critiques pendant 5 coups !"
      content += cSlayer.recap_useStacks(self.hit)
      return content, 0

    
    #Nombre de hits que le Slayer peut faire :
    for i in range(cSlayer.getNbrHit()):
      damage_dealt, damage_taken, hit_content, is_Crit = handler_Hit(Slayer, hit)
      total_damage_dealt += damage_dealt
      total_damage_taken += damage_taken
      content += hit_content

      #Le monstre prend des dégâts
      if damage_dealt > 0:
        cOpponent.getDamage(damage_dealt)
      #Le joueur prend des dégâts.
      if damage_taken > 0:
        cSlayer.getDamage(damage_taken)

    #On récap ce qui a été fait à l'adversaire
    if total_damage_dealt > 0:
      Opponent_Receive_Damage()

    #On utilise les stacks
    if hit == "S":
      content += cSlayer.recap_useStacks(hit)
    else:
      content += cSlayer.recapStacks()

    #On récap ce qui a été fait au Slayer  
    if total_damage_taken > 0:
      Slayer_Receive_Damage()

    #Familier 
      #Critique
    if is_Crit:
      await Slayer.getPet(rate=0.004, pets=[230])
      #Damage
    if total_damage_dealt > 0:
      await Slayer.getPet(pets=[194])
      #Armor
    if total_damage_taken > 0:
      await Slayer.getPet(pets=[193])
    #Achievement Biggest_Hit
      await Slayer.update_biggest_hit(total_damage_dealt)

    def Slayer_Receive_Damage(self):
      isDead, message = cSlayer.recapHealth(total_damage_taken)
      content += message
      self.stats['attacks_done'] += total_damage_taken
      if isDead:
        self.stats['kills'] += 1

    def Opponent_Receive_Damage(self):
      content += cOpponent.recapDamageTaken(total_damage_dealt)
      cOpponent.storeLastHits(total_damage_dealt, Slayer.Spe, hit)
      self.stats['attacks_received'] += 1
      content += cOpponent.slayer_storeAttack(cSlayer, total_damage_dealt, hit)

    def handler_Hit(self, Slayer, hit):
      #Simplification des args
      cOpponent = self.Opponents[self.count]
      cSlayer = Slayer.cSlayer

      #Initiation du content
      hit_content = ""
      damage_dealt = 0
      damage_taken = 0

      if cSlayer.isAlive()[0]:
        if cOpponent.base_hp > 0:
          if isSuccess_Fail():
            if isSuccess_Parry():
              is_Crit = isCrit()
              damage_dealt, hit_content = cSlayer.dealDamage(hit, cOpponent, is_Crit, CritMult(), ProtectCrit(), ArmorMult(Armor()))
              getStacks()
            else:
              damage_taken, hit_content = self.cOpponent.dealDamage(self.Slayer)

      def isSuccess_Fail(self):
        if True:
          return True
        else:
          hit_content = f"\n> Raté !"
          return False
        
      def isSuccess_Parry(self):
        if cOpponent.isParry(hit, Slayer):
          return True
        else:
          return False
      
      def isCrit(self):
        return cSlayer.isCrit(hit)
      
      def CritMult(self):
        if is_Crit:
          return cSlayer.stats[f"total_crit_damage_{hit}"]
        else:
          return 0
      
      def ProtectCrit(self):
        if is_Crit:
          return cOpponent.protect_crit
        else:
          return 0
        
      def Armor(self):
        return cSlayer.reduceArmor(hit, cOpponent.armor)
      
      def ArmorMult(self, armor):
        if armor >= 0:
            return float((1000/(1000+armor)))
        if armor < 0:
            return float(1+(((1000+abs(armor))/1000)))
      
      def getStacks(self):
        stacks_earned = cSlayer.getStacks(hit)
        hit_content += f"[+{stacks_earned}☄️]"
      
      return damage_dealt, damage_taken, hit_content, is_Crit

    return self.content, self.total_damage_dealt

class Hunt(Gamemode):
  def __init__(self, bot, gamemodedata):
      super().__init__(bot, gamemodedata)
  pass

class FactionWar(Gamemode):
  def __init__(self, bot, gamemodedata):
      super().__init__(bot, gamemodedata)

  def role_tracker_content(self):
    if self.role_tracker_activated and self.bot.Rarities[self.Opponents[self.count].rarity].tracker_role_id_banner != 0:
      return f"<@&{self.bot.Rarities[self.Opponents[self.count].rarity].tracker_role_id_banner}>"
    else:
      return ""

class Donjon(Gamemode):
  def __init__(self, bot, gamemodedata):
      super().__init__(bot, gamemodedata)

  def role_tracker_content(self):
    return ""