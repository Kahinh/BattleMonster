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
    self.min_dice = gamemodedata["roll_dices_min"]
    self.max_dice = gamemodedata["roll_dices_max"]
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

    #Fin
    self.end = False
    self.endnotbeingpublished = True
    self.timer_start = None
  
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
    if self.name not in self.bot.rChannels:
      logging.warning(f"NO CHANNELS FOR GAMEMODE")
      return False
    return True

  def role_tracker_content(self):
    if self.role_tracker_activated and self.bot.Rarities[self.Opponents[self.count].rarity].tracker_role_id != 0:
      return f"<@&{self.bot.Rarities[self.Opponents[self.count].rarity].tracker_role_id}>"
    else:
      return ""

  async def handler_Spawn(self, channel_id=None):
    embed = lib.Embed.create_embed_battle(self)
    view = lib.BattleView(self)
    if channel_id is None :
      channel_id = self.bot.rChannels[self.name]
    channel = self.bot.get_channel(channel_id)
    view.message = await channel.send(content=self.role_tracker_content(), embed=embed, view=view)
    self.bot.ActiveList.add_battle(view.message.id, view)

  async def handler_Build(self):

    async def pullGamemodeLootSlot():
      rlootslot = await self.bot.dB.pull_GamemodeLootSlot(self.name)
      for row in rlootslot:
        self.lootslot.append(row["slot"])
    
    async def pullGamemodeSpawnRate():
      rspawnrate = await self.bot.dB.pullGamemodeSpawnRate(self.name)
      for row in rspawnrate:
        self.spawnrate.update({row["rarities"]:float(row["spawn_rate"])})

    async def createOpponents():
      for i in range(self.spawns_count):
        if self.type == "factionwar":
          rarity = random.choices(list(self.spawnrate.keys()), list(self.spawnrate.values()), k=1)[0]
          #Création de l'opponent
          banner = Banner(self, "neutral", rarity, "banner")
          await banner.handler_Build()
          self.Opponents.append(banner)
        else:
          rarity = random.choices(list(self.spawnrate.keys()), list(self.spawnrate.values()), k=1)[0]
          element = random.choice(list(self.bot.Elements.keys()))
          type = "monster"
          if rarity == "mythic":
            #Création de l'opponent
            mythic = random.choice([ \
              Mythique1(self, element, rarity, type), \
              Mythique2(self, element, rarity, type), \
              Mythique3(self, element, rarity, type), \
              Mythique4(self, element, rarity, type), \
              Mythique5(self, element, rarity, type), \
              Mythique6(self, element, rarity, type)])
            await mythic.handler_Build()
            self.Opponents.append(mythic)
          else:
            #Création de l'opponent
            monster = Monster(self, element, rarity, type)
            await monster.handler_Build()
            self.Opponents.append(monster)

    await pullGamemodeLootSlot()
    await pullGamemodeSpawnRate()
    await createOpponents()

  async def handler_Loot(self):
  #On crée les requests à la dB
    request_opponents_killed_achievement = []
    request_mythic_stones = []
    request_money = []
    request_items = []

    async def push_dB_request():
      await self.bot.dB.push_behemoths_killed_achievement(request_opponents_killed_achievement)
      await self.bot.dB.push_MythicStones(request_mythic_stones)
      await self.bot.dB.push_loots(request_items)
      await self.bot.dB.push_money(request_money)

    async def review_loots():
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

    def auto_sellItem(Slayer, cItem):
      #On rajoute la monnaie dans la Class Slayer
      Slayer.addMoney(self.bot.Rarities[cItem.rarity].price)

      #On store le give money
      self.storage_loots[Slayer.cSlayer.id]["money"] += self.bot.Rarities[cItem.rarity].price
      request_money.append((self.bot.Rarities[cItem.rarity].price, Slayer.cSlayer.id))

      #Puis on ajoute la monnaie gagnée au Battle
      self.stats["money"] += self.bot.Rarities[cItem.rarity].price

    def auto_addtoinventoryItem(Slayer, cItem):
      #On rajoute l'item dans la Class Slayer
      Slayer.addtoInventory(cItem)
      #On store le give item
      request_items.append((Slayer.cSlayer.id, cItem.id, 1, False))
      self.storage_loots[Slayer.cSlayer.id]["items"].append(cItem)
      #Puis on ajoute l'item gagné au Battle
      self.stats["loots"] += 1

    def award_loots(Slayer, cOpponent):

      #On calcule le nombre de roll_dices
      roll_dices = cOpponent.get_roll_dices(Slayer)

      #On prend en compte le roll_dice
      for j in range(roll_dices):
        #On calcule le loot obtenu
        if random.choices(population=[True, False], weights=[cOpponent.slayers_hits[Slayer.cSlayer.id].luck, 1-cOpponent.slayers_hits[Slayer.cSlayer.id].luck], k=1)[0]:
          
          #On positionne dans le storage_loot
          storage_loot_handler(Slayer)
          self.storage_loots[Slayer.cSlayer.id]["loots"].append(random.choice(cOpponent.loot_table))

    def achievement_opponents_killed(Slayer):
      Slayer.cSlayer.achievements["monsters_killed"] += 1
      request_opponents_killed_achievement.append((1, Slayer.cSlayer.id))

    def award_mythics_stones(Slayer):
        #Mythic Stones = gatherable 5
        stones_earned =cOpponent.award_mythic_stones(Slayer)
        Slayer.cSlayer.inventory_gatherables[5] += stones_earned
        request_mythic_stones.append((Slayer.cSlayer.id, 5, stones_earned))
        self.stats["mythic_stones"] += stones_earned

        #On positionne dans le storage_loot
        storage_loot_handler(Slayer)
        self.storage_loots[Slayer.cSlayer.id]["mythic_stones"] += stones_earned

    def storage_loot_handler(Slayer):
      if Slayer.cSlayer.id not in self.storage_loots:
        self.storage_loots[Slayer.cSlayer.id] = {
          "mythic_stones": 0,
          "items" : [],
          "money" : 0,
          "loots" : []
        }

    #On check les monstres 1 par 1
    for cOpponent in self.Opponents:
      if cOpponent.maybeDead and cOpponent.loot_table != []:
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
                award_mythics_stones(Slayer)
              #On distribue les loots
              award_loots(Slayer, cOpponent)

              #On revoit les butins : AutoVente ou vrai distrib ?
              await review_loots()

              #On push via le dB Manager
              await push_dB_request()

  async def handler_Attack(self, Slayer, hit):

    #Simplification des args
    cOpponent = self.Opponents[self.count]
    bot = self.bot
    cSlayer = Slayer.cSlayer

    def Slayer_Receive_Damage():
      isDead, message = cSlayer.recapHealth(total_damage_taken)
      content = message
      self.stats['attacks_done'] += total_damage_taken
      if isDead:
        self.stats['kills'] += 1
      return isDead, content

    def Opponent_Receive_Damage():
      content = ""
      content += cOpponent.recapDamageTaken(total_damage_dealt)
      cOpponent.storeLastHits(total_damage_dealt, cSlayer, self.type)
      self.stats['attacks_received'] += 1
      return content

    def Banner_Receive_Damage():
      content = ""
      content += cOpponent.recapDamageTaken(total_damage_dealt, cSlayer)
      cOpponent.storeLastHits(total_damage_dealt, cSlayer, self.type)
      self.stats['attacks_received'] += 1
      return content

    def isFail():
      #precision_score = min((max(cOpponent.gearscore-cSlayer.gearscore, 0)/100),1)
      #if random.choices(population=[True, False], weights=[precision_score, 1-precision_score], k=1)[0]:
      if cOpponent.gearscore > cSlayer.gearscore:
        return True
      else:
        return False

    def handler_Hit(Slayer, hit):

      #Initiation du content
      hit_content = ""
      is_Crit = False
      damage_dealt = 0
      damage_taken = 0
        
      def isParry():
        if cOpponent.isParry(hit, Slayer):
          return True
        else:
          return False
      
      def isCrit():
        return cSlayer.isCrit(hit)
      
      def CritMult(is_Crit):
        if is_Crit:
          return cSlayer.stats[f"total_crit_damage_{hit}"]
        else:
          return 0
      
      def ProtectCrit(is_Crit):
        if is_Crit:
          return cOpponent.protect_crit
        else:
          return 0
        
      def Armor():
        return cSlayer.reduceArmor(hit, cOpponent.armor)
      
      def ArmorMult(armor):
        if armor >= 0:
            return float((1000/(1000+armor)))
        if armor < 0:
            return float(1+(((1000+abs(armor))/1000)*float(bot.Variables["malus_negative_armor_with_leta"])))
      
      def getStacks():
        stacks_earned = cSlayer.getStacks(hit)
        if stacks_earned > 0:
          return f"[+{stacks_earned}☄️]"
        else:
          return ""

      if cSlayer.isAlive()[0]:
        if cOpponent.isAlive():
            if not isParry():
              is_Crit = isCrit()
              damage_dealt, hit_content = cSlayer.dealDamage(hit, cOpponent, is_Crit, CritMult(is_Crit), ProtectCrit(is_Crit), ArmorMult(Armor()))
              hit_content += getStacks()
            else:
              damage_taken, hit_content = cOpponent.dealDamage(Slayer)

      return damage_dealt, damage_taken, hit_content, is_Crit

    #Initiation du content
    content = "**__Rapport de Combat :__**"
    total_damage_dealt = 0
    total_damage_taken = 0

    if not cOpponent.isAlive():
      return f'Le {cOpponent.group_name} est déjà mort !', 0, False

    #On check si on est vivant ou mort.
    if (isAlive := cSlayer.isAlive()) and not isAlive[0]:
      return isAlive[1], 0, False
    
    #On peut special
    if ((canSpecial := cSlayer.canSpecial()) and not canSpecial[0]) and hit == "s":
      return canSpecial[1], 0, False
      
    #On peut attaquer selon le timing
    if (canAttack := cOpponent.slayer_canAttack(cSlayer)) and not canAttack[0] and hit != "s":
      return canAttack[1], 0, False
    
    if (int(cSlayer.faction) not in self.bot.Factions and self.type == "factionwar"):
      return "Tu dois faire parti d'une faction pour combattre ici", 0, False
    
    if isFail():
      return f"\n> **Raté !** Score insuffisant", 0, False
    
    #Spe Berserker
    if hit == "s" and cSlayer.Spe.id == 8:
      cSlayer.berserker_mode = 5
      cSlayer.calculateStats(self.bot.rBaseBonuses)
      content = f"\n> Vous avez activé le mode Berserker, vous obtenez {int(self.bot.Variables['assassin_crit_chance_bonus'])*100}% Chance Critique et {int(self.bot.Variables['assassin_crit_damage_bonus'])*100}% Dégâts Critiques pendant 5 coups !"
      cSlayer.useStacks(hit)
      content += cSlayer.recap_useStacks(hit)
      return content, 0, False

    #On consomme les stacks du S avant
    if hit == "s":
      cSlayer.useStacks(hit)
    
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
      if cOpponent.type != "banner":
        content += Opponent_Receive_Damage()
      else:
        content += Banner_Receive_Damage()

    #On utilise les stacks
    if hit == "s":
      content += cSlayer.recap_useStacks(hit)
    else:
      content += cSlayer.recapStacks()

    #On récap ce qui a été fait au Slayer  
    isDead = False
    if total_damage_taken > 0:
      isDead, message = Slayer_Receive_Damage()
      content += message

    #On store l'attaque
    content += cOpponent.slayer_storeAttack(cSlayer, total_damage_dealt, hit)

    if isDead:
      await self.bot.ActiveList.remove_eligibility(cSlayer)
      content = "Tu es mort ! Tu perds l'éligibilité aux butins sur tous les combats en cours."

    #Familier 
      #Critique
    if is_Crit:
      await Slayer.getDrop(rate=0.004, pets=[230])
      #Damage
    if total_damage_dealt > 0:
      await Slayer.getDrop(pets=[194])
      #Bworky Final Damage S
    if total_damage_dealt > 150000 and hit == 's':
      await Slayer.getDrop(rate=1, pets=[301])
      #Tirubima Final Damage H
    if total_damage_dealt > 50000 and hit == 'h':
      await Slayer.getDrop(rate=1, pets=[302])
      #Blokus Parry %
    if total_damage_taken > 1000:
      await Slayer.getDrop(rate=1, pets=[303])
      #Armor
    if total_damage_taken > 0:
      await Slayer.getDrop(pets=[193])
      #Leta
    if Slayer.cSlayer.stats["total_letality_l"] + Slayer.cSlayer.stats["total_letality_h"] + Slayer.cSlayer.stats["total_letality_s"] > 4000:
      await Slayer.getDrop(rate=1, pets=[409])

    #Achievement Biggest_Hit
    await Slayer.update_biggest_hit(total_damage_dealt)
      #1000
    if Slayer.cSlayer.achievements['monsters_killed'] >= 1000:
      await Slayer.getDrop(rate=1, pets=[411])
      #2000
    if Slayer.cSlayer.achievements['monsters_killed'] >= 2000:
      await Slayer.getDrop(rate=1, pets=[412])
      #5000
    if Slayer.cSlayer.achievements['monsters_killed'] >= 5000:
      await Slayer.getDrop(rate=1, pets=[413])
      #10000
    if Slayer.cSlayer.achievements['monsters_killed'] >= 10000:
      await Slayer.getDrop(rate=1, pets=[414])


    #On update le Slayer dans la dB
    await self.bot.dB.push_slayer_data(Slayer.cSlayer)

    #A t on tué un monstre ?
    monster_killed = False
    if self.Opponents[self.count].base_hp == 0:
      if self.count == self.spawns_count - 1:
          self.end = True
      else:
          self.count += 1
          monster_killed = True

    return content, total_damage_dealt, monster_killed

class Hunt(Gamemode):
  def __init__(self, bot, gamemodedata):
      super().__init__(bot, gamemodedata)
  pass

class FactionWar(Gamemode):
  def __init__(self, bot, gamemodedata):
      super().__init__(bot, gamemodedata)
      self.timer_start = lib.datetime.datetime.timestamp(lib.datetime.datetime.now())
      self.spawns_count = 1

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