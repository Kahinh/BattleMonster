#list_with_rarity = [key for key, val in Monsters.items() if val.rarity=="rare"]
battle_bonuses = {
    "pain_lasthit": 10
}

import random

class Monster:
  def __init__(
    self, 
    rMonster,
    rGamemode,
    hp_scaling
    ):
    self.name = rMonster["name"]
    self.description = rMonster["description"]
    self.element = rMonster["element"]
    self.base_hp = rMonster["base_hp"] * hp_scaling * rGamemode["hp_scaling"]
    self.total_hp = rMonster["base_hp"] * hp_scaling * rGamemode["hp_scaling"]
    self.rarity = rMonster["rarity"]
    self.parry = {
      "parry_chance_L" : float(rMonster["parry_chance_L"]) * int(rGamemode["parry_scaling"]),
      "parry_chance_H" : float(rMonster["parry_chance_H"]) * int(rGamemode["parry_scaling"]),
      "parry_chance_S" : 0
    }
    self.damage = rMonster["damage"] * rGamemode["damage_scaling"]
    self.letality = rMonster["letality"] * rGamemode["letality_scaling"]
    self.letality_per = rMonster["letality_per"] * rGamemode["letality_scaling"]
    self.armor = rMonster["armor"] * rGamemode["armor_scaling"]
    self.protect_crit = rMonster["protect_crit"] * rGamemode["protect_crit_scaling"]
    self.img_url_normal = rMonster["img_url_normal"]
    self.img_url_enraged = rMonster["img_url_enraged"]
    self.bg_url = rMonster["bg_url"]
    self.roll_dices = random.randint(rGamemode["roll_dices_min"], rGamemode["roll_dices_max"])

    self.rGamemode = rGamemode
    self.last_hits = []
    self.slayers_hits = {}

  def GetDamage(self, damage, hit, slayer_class):
    self.base_hp -= damage
    #On stock les last hits pour le special Douleur
    if (hit != "S" and slayer_class.specialization != 2) :
      self.last_hits.append(damage)
      if len(self.last_hits) > battle_bonuses["pain_lasthit"]:
        del self.last_hits[0]
