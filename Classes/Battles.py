battle_bonuses = {
    "pain_lasthit": 10
}

class Battles:
  def __init__(
    self, 
    gamemode,
    loots_slots,
    monster_class,
    last_hits,
    slayers_data
    ):
    self.gamemode = gamemode
    self.loots_slots = loots_slots
    self.monster_class = monster_class
    self.last_hits = last_hits
    self.slayers_data = slayers_data
  
  def GetDamage(self, damage, hit, slayer_class):
    self.monster_class.base_hp -= damage
    #On stock les last hits pour le special Douleur
    if (hit != "S" and slayer_class.specialization != 2) :
      self.last_hits.append(damage)
      if len(self.last_hits) > battle_bonuses["pain_lasthit"]:
        del self.last_hits[0]
