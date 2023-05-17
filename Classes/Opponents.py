import os, sys, inspect

from dataclasses import dataclass
import random

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import lib

@dataclass
class Monster:
  name: str
  description: str
  element: str
  rarity: str
  base_hp: int

  def __init__(
    self, 
    i,
    Battle,
    hp_scaling
    ):
    self.name = Battle.Opponents[i]["name"]
    self.description = Battle.Opponents[i]["description"]
    self.element = Battle.Opponents[i]["element"]
    self.base_hp = int(Battle.Opponents[i]["base_hp"] * int(max(1,hp_scaling/2)) * Battle.scaling["hp"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"]))
    self.total_hp = int(Battle.Opponents[i]["base_hp"] * int(max(1,hp_scaling/2)) * Battle.scaling["hp"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"]))
    self.rarity = Battle.Opponents[i]["rarity"]
    self.parry = {
      "parry_chance_l" : float(Battle.Opponents[i]["parry_chance_l"]) * float(Battle.scaling["parry"]) * float((1 + i * Battle.bot.rBaseBonuses["mult_battle"])),
      "parry_chance_h" : float(Battle.Opponents[i]["parry_chance_h"]) * float(Battle.scaling["parry"]) * float((1 + i * Battle.bot.rBaseBonuses["mult_battle"])),
      "parry_chance_s" : 0
    }
    self.damage = int(Battle.Opponents[i]["damage"] * Battle.scaling["damage"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"]))
    self.letality = int(Battle.Opponents[i]["letality"] * Battle.scaling["letality"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"]))
    self.letality_per = min(Battle.Opponents[i]["letality_per"] * max(int(Battle.scaling["letality"]/3),1) * (1 + i * Battle.bot.rBaseBonuses["mult_battle"]),1)
    self.armor = int(Battle.Opponents[i]["armor"] * Battle.scaling["armor"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"]))
    self.armor_cap = int(Battle.Opponents[i]["armor"])
    self.protect_crit = int(Battle.Opponents[i]["protect_crit"] * Battle.scaling["protect_crit"] * (1 + i * Battle.bot.rBaseBonuses["mult_battle"]))
    self.img_url_normal = Battle.Opponents[i]["img_url_normal"]
    self.img_url_enraged = Battle.Opponents[i]["img_url_enraged"]
    self.bg_url = Battle.Opponents[i]["bg_url"]
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

  def storeLastHits(self, damage, Spe):
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
        return False, f"\n> Pas si vite ! Prends ton temps ! Prochaine attaque disponible dans **{int(self.slayers_hits[cSlayer.id].timestamp_next_hit - lib.datetime.datetime.timestamp(lib.datetime.datetime.now()))}s**"
    else:
      return True, ""

  def slayer_storeAttack(self, cSlayer, damage, hit):
    if cSlayer.id in self.slayers_hits:
      self.slayers_hits[cSlayer.id].updateClass(damage, None if hit == "s" else cSlayer.stats["total_cooldown"], cSlayer.stats["total_luck"])
    else:
      self.slayers_hits[cSlayer.id] = lib.DamageDone(0 if hit == "s" else cSlayer.stats["total_cooldown"], damage if damage > 0 else 0, True if damage > 0 else False, cSlayer.stats["total_luck"])
    content = self.slayers_hits[cSlayer.id].checkStatus(damage, self.base_hp)
    return content