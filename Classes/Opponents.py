
from dataclasses import dataclass
import random
from datetime import datetime

from Classes.DamageDone import DamageDone

@dataclass
class Opponent:
  name: str
  description: str
  element: str
  rarity: str
  base_hp: int

  def __init__(self, gamemode, element, rarity, type):

    self.bot = gamemode.bot
    self.gamemode = gamemode

    self.element = element
    self.rarity = rarity
    self.type = type

    self.name = ""
    self.group_name = "Monstre"
    self.description = ""
    self.img_url_normal = ""
    self.img_url_enraged = ""
    self.bg_url = ""
    self.roll_dices = random.randint(gamemode.min_dice, gamemode.max_dice)

    #Storage
    self.last_hits = []
    self.slayers_hits = {}
    self.loot_table = []

    #Vie
    self.base_hp = 0
    self.total_hp = 0

    #Défensif
    self.armor = 0
    self.armor_cap = 0
    self.protect_crit = 0
    self.gearscore = 0
    self.parry = {
      "parry_chance_l" : 0,
      "parry_chance_h" : 0,
      "parry_chance_s" : 0
    }

    #Offensif
    self.damage = 0
    self.letality = 0
    self.letality_per = 0

  @staticmethod
  async def get_Opponent_Class(gamemode, element, rarity, type):
    if type == "banner":
      return await Banner.handler_Build(gamemode, element, rarity, type)
    else:
      if rarity == "mythic":
        return random.choice([ \
              await Mythique1.handler_Build(gamemode, element, rarity, type), \
              await Mythique2.handler_Build(gamemode, element, rarity, type), \
              await Mythique3.handler_Build(gamemode, element, rarity, type), \
              await Mythique4.handler_Build(gamemode, element, rarity, type), \
              await Mythique5.handler_Build(gamemode, element, rarity, type), \
              await Mythique6.handler_Build(gamemode, element, rarity, type)])
      else: 
        return await Monster.handler_Build(gamemode, element, rarity, type)

  @classmethod
  async def handler_Build(cls, gamemode, element, rarity, type):

    self = cls(gamemode, element, rarity, type)

    async def pullOpponentData():
      return await self.bot.dB.pull_OpponentData(self.rarity, self.element, self.type)

    async def pullOpponentLootTable():
      return await self.bot.dB.pull_OpponentLootTable(self.name, self.gamemode.lootslot)

    def compileOpponentData(OpponentData):
      self.name = OpponentData["name"]
      self.description = OpponentData["description"]
      self.element = OpponentData["element"]
      self.base_hp = int(OpponentData["base_hp"] * float(self.gamemode.scaling["hp"]) * (1 + (float(self.bot.ActiveList.get_active_slayer_nbr()) * int(self.bot.Variables["mult_active_slayers_hp"]))))
      self.total_hp = int(OpponentData["base_hp"] * float(self.gamemode.scaling["hp"]) * (1 + (float(self.bot.ActiveList.get_active_slayer_nbr()) * int(self.bot.Variables["mult_active_slayers_hp"]))))
      self.rarity = OpponentData["rarity"]
      self.gearscore = OpponentData["gearscore"]
      self.parry = {
        "parry_chance_l" : float(OpponentData["parry_chance_l"]) * float(self.gamemode.scaling["parry"]),
        "parry_chance_h" : float(OpponentData["parry_chance_h"]) * float(self.gamemode.scaling["parry"]),
        "parry_chance_s" : 0
      }
      self.damage = int(OpponentData["damage"] * self.gamemode.scaling["damage"])
      self.letality = int(OpponentData["letality"] * self.gamemode.scaling["letality"])
      self.letality_per = min(OpponentData["letality_per"] * max(int(self.gamemode.scaling["letality"]/3),1),1)
      self.armor = int(OpponentData["armor"] * int(self.gamemode.scaling["armor"]) * (1 + (int(self.bot.ActiveList.get_active_slayer_nbr()) * float(self.bot.Variables["mult_active_slayers_armor"]))))
      self.armor_cap = int(OpponentData["armor"])
      self.protect_crit = int(OpponentData["protect_crit"] * self.gamemode.scaling["protect_crit"])
      self.img_url_normal = OpponentData["img_url_normal"]
      self.img_url_enraged = OpponentData["img_url_enraged"]
      self.bg_url = OpponentData["bg_url"]
    
    OpponentData = await pullOpponentData()
    compileOpponentData(OpponentData)
    self.loot_table = await pullOpponentLootTable()

    return self

  def dealDamage(self, cSlayer):
    armor = int(self.reduceArmor(cSlayer.stats["armor"]))
    damage = int(self.damage)
    #Armor
    damage = int(max(damage * int(self.bot.Variables["ratio_armor"])/(int(self.bot.Variables["ratio_armor"])+armor), 0))
    #Max HP
    damage = int(min(damage, cSlayer.health - cSlayer.damage_taken))
    return damage, f"\n> ↪️ Parade: **-{int(damage)}** vie"

  def reduceArmor(self, armor):
      armor = max((int(armor*(1-float(self.letality_per)))-int(self.letality)), 0)
      return int(armor)

  def storeLastHits(self, damage, cSlayer, gamemode_type):
    if cSlayer.cSpe.id != 4 and damage != 0:

      #On check quelle liste il faut prendre
      list_lasthits = self.identify_lasthits_list(cSlayer)

      list_lasthits.append(int(damage*float(self.bot.Variables["cdg_malus_attack_in_stack"])))
      if len(list_lasthits) > int(self.bot.Variables["cdg_nbr_hit_stack"]):
        list_lasthits.pop(0)

  def identify_lasthits_list(self, cSlayer):
    return self.last_hits
  
  def extract_lasthits_list(self, cSlayer):
    extraction = sum(self.last_hits)
    self.last_hits = []
    return extraction

  def isParry(self, hit, cSlayer):
    if (self.parry["parry_chance_l"] + cSlayer.stats[f"parry_l"]) >= 1 and (self.parry["parry_chance_h"] + cSlayer.stats[f"parry_h"]) >= 1:
      return True
    else:
      ParryChance = min(max(self.parry[f"parry_chance_{hit}"] + cSlayer.stats[f"parry_{hit}"], 0), 1)
      return random.choices(population=[True, False], weights=[ParryChance, 1-ParryChance], k=1)[0]

  def getDamage(self, damage):
    self.base_hp -= int(damage)

  def recapDamageTaken(self, damage):  
    if self.base_hp == 0:
      return f"\n\n> Le {self.group_name} est mort ! 💀"
    else:
      return f"\n\n> Le {self.group_name} possède désormais {int(self.base_hp)}/{int(self.total_hp)} ❤️"

  def slayer_canAttack(self, cSlayer):
    if cSlayer.id in self.slayers_hits:
      if self.slayers_hits[cSlayer.id].canAttack():
        return True, ""
      else:
        return False, f"\n> Pas si vite ! Prends ton temps ! Prochaine attaque disponible dans **{int(self.slayers_hits[cSlayer.id].timestamp_next_hit - datetime.timestamp(datetime.now()))}s**"
    else:
      return True, ""

  def slayer_storeAttack(self, cSlayer, damage, hit):
    if cSlayer.id in self.slayers_hits:
      self.slayers_hits[cSlayer.id].updateClass(damage, None if hit == "s" else cSlayer.stats["cooldown"], cSlayer.stats["luck"])
    else:
      self.slayers_hits[cSlayer.id] = DamageDone(cSlayer, 0 if hit == "s" else cSlayer.stats["cooldown"], damage if damage > 0 else 0, True if damage > 0 else False, cSlayer.stats["luck"])
    content = self.slayers_hits[cSlayer.id].checkStatus(damage, self)
    return content
  
  def slayer_loses_eligibility(self, cSlayer):
    if cSlayer.id not in self.slayers_hits:
      return ""
    else:
      if not self.slayers_hits[cSlayer.id].eligible:
        return ""
      else:
        self.slayers_hits[cSlayer.id].eligible = False
        return " Tu n'es plus éligible au butin !"

  def isAlive(self):
    if self.base_hp is None:
      return True
    else:
      if self.base_hp > 0:
        return True
      else:
        return False

  def maybeDead(self):
    if self.base_hp is None:
      return True
    else:
      if self.base_hp == 0:
        return True
      else:
        return False

  def get_roll_dices(self, cSlayer):
    return self.roll_dices

@dataclass
class Monster(Opponent):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, rarity, type)

  def award_mythic_stones(self, cSlayer):
    return 0
  
class Banner(Opponent):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, rarity, type)
    self.bot = gamemode.bot
    self.roll_dices = gamemode.max_dice
    self.group_name = "Pilier"
  
  @classmethod
  async def handler_Build(cls, gamemode, element, rarity, type):
    self = await super().handler_Build(gamemode, element, rarity, type)
    self.base_hp = None
    self.total_hp = None

    #last hits
    self.last_hits = {}
    self.split_by_faction_last_hits()

    #factions_total_damage
    self.faction_total_damage = {}
    self.split_by_faction_total_damage()

    #factions_best_damage
    self.faction_best_damage = {}
    self.split_by_faction_best_damage()

    return self
  
  def split_by_faction_last_hits(self):
    for faction_id in self.bot.Factions:
      self.last_hits.update({faction_id: []})

  def split_by_faction_total_damage(self):
    for faction_id in self.bot.Factions:
      self.faction_total_damage.update({faction_id: []})

  def split_by_faction_best_damage(self):
    for faction_id in self.bot.Factions:
      self.faction_best_damage.update({faction_id: 0})

  def recapDamageTaken(self, damage, cSlayer):  
    self.faction_total_damage[cSlayer.faction].append(damage)
    if len(self.faction_total_damage[cSlayer.faction]) > int(self.bot.Variables["factionwar_nbr_hit_stack"]):
      self.faction_total_damage[cSlayer.faction].pop(0)
    
    if sum(self.faction_total_damage[cSlayer.faction]) > self.faction_best_damage[cSlayer.faction]:
      self.faction_best_damage[cSlayer.faction] = sum(self.faction_total_damage[cSlayer.faction])
      return f"\n> Cette attaque permet à ta faction d'atteindre un nouveau record de **{self.faction_best_damage[cSlayer.faction]}** dégâts"
    else:
      return ""
    
  def identify_lasthits_list(self, cSlayer):
    return self.last_hits[cSlayer.faction]

  def extract_lasthits_list(self, cSlayer):
    extraction = sum(self.last_hits[cSlayer.faction])
    self.last_hits[cSlayer.faction] = []
    return extraction

  def getDamage(self, damage):
    pass

  def get_roll_dices(self, cSlayer):
    listed_factions = dict(sorted(self.faction_best_damage.items(), key=lambda x:x[1], reverse=True))
    slayer_faction_positionning = list(listed_factions.keys()).index(cSlayer.faction)

    roll_dices = max(self.roll_dices - (slayer_faction_positionning * int(self.bot.Variables["factionwar_roll_dices_malus_by_positionning"])), 0)
    return int(roll_dices)

  def isParry(self, hit, cSlayer):
    return False
  
  def award_mythic_stones(self, cSlayer):
    listed_factions = dict(sorted(self.faction_best_damage.items(), key=lambda x:x[1], reverse=True))
    slayer_faction_positionning = list(listed_factions.keys()).index(cSlayer.faction)

    roll_dices = max(self.roll_dices - (slayer_faction_positionning * int(self.bot.Variables["factionwar_roll_dices_malus_by_positionning"])), 0)
    return int(roll_dices)

class Mythique(Opponent):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)

  def award_mythic_stones(self, cSlayer):
    return random.randint(int(self.bot.Variables["min_mythic_stones"]),int(self.bot.Variables["max_mythic_stones"]))

class Mythique1(Mythique):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass

class Mythique2(Mythique):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass

class Mythique3(Mythique):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass

class Mythique4(Mythique):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass

class Mythique5(Mythique):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass

class Mythique6(Mythique):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass