from copy import deepcopy
import datetime

class Spe:
  def __init__(
    self, 
    rSpe
    ):
    self.id = rSpe["id"]
    self.name = rSpe["name"]
    self.description = rSpe["description"]
    self.damage = rSpe["damage"]
    self.stacks = rSpe["stacks"]
    self.cost = rSpe["cost"]

  def adjust_slot_count(self, rSlots):
    Slots = deepcopy(rSlots)
    #SURAREMENT
    if self.id == 2:
      Slots["weapon"]["count"] = 2
    #TEMPLIER
    if self.id == 3:
      Slots["shield"]["count"] = 1
    return Slots

  def nbr_hit(self, standard):
    base = deepcopy(standard)
    if self.id == 2:
      base += 1
    return base
  
  def pain(self, cMonster):
    if self.id == 4:
      damage = int(min(sum(cMonster.last_hits), cMonster.base_hp))
      if damage == 0:
        return 0, f"\n> Il n'y avait pas d'attaques chargées.", []
      else:
        return damage, f"\n> Vaillance du chef : Dégâts infligés {damage}", []
    else:
      return 0, "", cMonster.last_hits
  
  def shieldslam(self, cMonster, Slayer):
    if self.id == 3:
      damage = int(min(Slayer.cSlayer.stats["total_armor"]*3, cMonster.base_hp))
      if damage == 0:
        return 0, f"\n> Oups, à côté !."
      else: 
        if Slayer.cSlayer.isCrit("S"):
          damage = int(min(damage * (1 + Slayer.cSlayer.stats["total_crit_damage_S"]), cMonster.base_hp))
          return damage, f"\n> Impact de Bouclier : Dégâts infligés {damage} ‼️ "
        else:
          return damage, f"\n> Impact de Bouclier : Dégâts infligés {damage}"
    else:
      return 0, ""
  
  def resetTimer(self, cMonster):
    if self.id == 5:
      for slayer_id in cMonster.slayers_hits:
        cMonster.slayers_hits[slayer_id].timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now())
      return cMonster.slayers_hits, f"\n\nVos alliés peuvent attaquer de nouveau."
    else:
      return cMonster.slayers_hits, f""
