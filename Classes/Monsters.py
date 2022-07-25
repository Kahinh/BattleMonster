#list_with_rarity = [key for key, val in Monsters_list.items() if val.rarity=="rare"]

class Monsters:
  def __init__(
    self, 
    name, 
    description, 
    element,
    base_hp,
    rarity,
    parry_chance_L,
    parry_chance_H,
    damage,
    armor,
    protect_crit,
    img_url_normal,
    img_url_enraged,
    bg_url,
    letality,
    letality_per,
    ):
    self.name = name
    self.description = description
    self.element = element
    self.base_hp = base_hp
    self.total_hp = base_hp
    self.rarity = rarity
    self.parry = {
      "parry_chance_L" : parry_chance_L,
      "parry_chance_H" : parry_chance_H,
      "parry_chance_S" : 0
    }
    self.damage = damage
    self.letality = letality
    self.letality_per = letality_per
    self.armor = armor
    self.protect_crit = protect_crit
    self.img_url_normal = img_url_normal
    self.img_url_enraged = img_url_enraged
    self.bg_url = bg_url
    self.roll_dices = 0
  
  def updateStats(self, monster_hp_scaling, monster_difficulty_scaling, roll_dices):

    self.base_hp *= monster_hp_scaling
    self.total_hp *= monster_hp_scaling

    self.roll_dices += roll_dices

    self.parry["parry_chance_L"] *= monster_difficulty_scaling
    self.parry["parry_chance_H"] *= monster_difficulty_scaling

    self.damage *= monster_difficulty_scaling
    self.armor *= monster_difficulty_scaling
    self.letality *= monster_difficulty_scaling
    self.letality_per *= monster_difficulty_scaling
    self.protect_crit *= monster_difficulty_scaling
