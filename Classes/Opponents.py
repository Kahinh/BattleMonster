
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
    self.parry = {
      "parry_chance_l" : 0,
      "parry_chance_h" : 0,
      "parry_chance_s" : 0
    }

    #Offensif
    self.damage = 0
    self.letality = 0
    self.letality_per = 0

  def __getattr__(self, *args, **kwargs):
      def printf(*args, **kwargs):
          #print(args, kwargs)
          pass
      return printf

  async def handler_Build(self):
    OpponentData = await pullOpponentData()
    compileOpponentData(OpponentData)
    self.loot_table = await pullOpponentLootTable()

    async def pullOpponentData(self):
      return await self.bot.dB.pull_OpponentData(self.rarity, self.element, self.type)

    async def pullOpponentLootTable(self):
      return await self.bot.dB.pull_OpponentLootTable(self.name, self.gamemode.lootslot)

    def compileOpponentData(self, OpponentData):
      self.name = OpponentData["name"]
      self.description = OpponentData["description"]
      self.element = OpponentData["element"]
      self.base_hp = int(OpponentData["base_hp"] * int(max(1,len(self.bot.ActiveList.active_slayers)+1/2)) * self.gamemode.scaling["hp"])
      self.total_hp = int(OpponentData["base_hp"] * int(max(1,len(self.bot.ActiveList.active_slayers)+1/2)) * self.gamemode.scaling["hp"])
      self.rarity = OpponentData["rarity"]
      self.parry = {
        "parry_chance_l" : float(OpponentData["parry_chance_l"]) * float(self.gamemode.scaling["parry"]),
        "parry_chance_h" : float(OpponentData["parry_chance_h"]) * float(self.gamemode.scaling["parry"]),
        "parry_chance_s" : 0
      }
      self.damage = int(OpponentData["damage"] * self.gamemode.scaling["damage"])
      self.letality = int(OpponentData["letality"] * self.gamemode.scaling["letality"])
      self.letality_per = min(OpponentData["letality_per"] * max(int(self.gamemode.scaling["letality"]/3),1),1)
      self.armor = int(OpponentData["armor"] * self.gamemode.scaling["armor"])
      self.armor_cap = int(OpponentData["armor"])
      self.protect_crit = int(OpponentData["protect_crit"] * self.gamemode.scaling["protect_crit"])
      self.img_url_normal = OpponentData["img_url_normal"]
      self.img_url_enraged = OpponentData["img_url_enraged"]
      self.bg_url = OpponentData["bg_url"]

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

  def storeLastHits(self, damage, Spe, hit):
    #TODO NERF CDG : Les S ne comptent plus
    if Spe.id != 4 and damage != 0:
      self.last_hits.append(damage)
      if len(self.last_hits) > 5:
        self.last_hits.pop(0)

  def isParry(self, hit, Slayer):
    if self.parry["parry_chance_L"] >= 1 and self.parry["parry_chance_H"] >= 1:
      return True
    else:
      ParryChance = min(max(self.parry[f"parry_chance_{hit}"] + Slayer.cSlayer.stats[f"total_parry_{hit}"], 0), 1)
      return random.choices(population=[True, False], weights=[ParryChance, 1-ParryChance], k=1)[0]

  def getDamage(self, damage):
    self.base_hp -= int(damage)

  def recapDamageTaken(self, damage):  
    if self.base_hp == 0:
      return f"\n\n> Le monstre est mort ! 💀"
    else:
      return f"\n\n> Le monstre possède désormais {int(self.base_hp)}/{int(self.total_hp)} ❤️"

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
      self.slayers_hits[cSlayer.id].updateClass(damage, None if hit == "s" else cSlayer.stats["total_cooldown"], cSlayer.stats["total_luck"])
    else:
      self.slayers_hits[cSlayer.id] = DamageDone(0 if hit == "s" else cSlayer.stats["total_cooldown"], damage if damage > 0 else 0, True if damage > 0 else False, cSlayer.stats["total_luck"])
    content = self.slayers_hits[cSlayer.id].checkStatus(damage, self.base_hp)
    return content

@dataclass
class Monster(Opponent):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, rarity, type)
  
class Banner(Opponent):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, rarity, type)
  
  async def handler_Build(self):
    pass

class Mythique1(Opponent):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass

class Mythique2(Opponent):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass

class Mythique3(Opponent):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass

class Mythique4(Opponent):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass

class Mythique5(Opponent):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass

class Mythique6(Opponent):
  def __init__(self, gamemode, element, rarity, type):
    super().__init__(gamemode, element, "mythic", type)
    pass