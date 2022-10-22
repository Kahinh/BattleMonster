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
    self.emote = rSpe["display_emote"]

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
  
  def pain(self, cMonster, Slayer):
    if self.id == 4:
      damage, content = Slayer.cSlayer.dealDamage("S", cMonster, sum(cMonster.last_hits), "Vaillance du chef")
      return damage, content
    else:
      return 0, ""
  
  def shieldslam(self, cMonster, Slayer):
    if self.id == 3:
      damage, content = Slayer.cSlayer.dealDamage("S", cMonster, int(Slayer.cSlayer.stats["total_armor"]*3), "Impact de Bouclier")
      return damage, content
    else:
      return 0, ""
  
  def resetTimer(self, cMonster):
    if self.id == 5:
      for slayer_id in cMonster.slayers_hits:
        cMonster.slayers_hits[slayer_id].timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now())
      return cMonster.slayers_hits, f"\n\n>Vos alliés peuvent attaquer de nouveau."
    else:
      return cMonster.slayers_hits, f""
  
  def weakness(self, cMonster, Slayer):
    if self.id == 6:
      if cMonster.armor == cMonster.armor_cap:
        damage, content = Slayer.cSlayer.dealDamage("S", cMonster, int(Slayer.cSlayer.stats["total_letality_S"] * (1+Slayer.cSlayer.stats["total_letality_per_S"])), "Point Faible")
        return damage, content
      else:
        armor_reduction = int((cMonster.armor * Slayer.cSlayer.stats["total_letality_per_S"] + Slayer.cSlayer.stats["total_letality_S"]) / 5)
        armor_reduction = int(min(armor_reduction, cMonster.armor - cMonster.armor_cap))
        cMonster.armor -= armor_reduction
        return 0, f"\n\n> Tu as retiré {armor_reduction} 🛡️ au monstre !"
    else:
      return 0, ""
