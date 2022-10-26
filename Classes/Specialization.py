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
    self.ability_name = rSpe["ability_name"]

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
  
  def get_damage(self, cMonster, cSlayer):
    if self.id == 3: #Templier
      return int(cSlayer.stats["total_armor"]*3), ""
    elif self.id == 4: #Chef de Guerre
      return sum(cMonster.last_hits), ""
    elif self.id == 5: #Forgeron
      for slayer_id in cMonster.slayers_hits:
        cMonster.slayers_hits[slayer_id].timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now())
      return 0, "(*Cooldown reset*)"
    elif self.id == 6: #Analyst Chasseur   
      if cMonster.armor == cMonster.armor_cap:
        return int(cSlayer.stats["total_letality_S"] * (1+cSlayer.stats["total_letality_per_S"])), ""
      else:
        armor_reduction = int((cMonster.armor * cSlayer.stats["total_letality_per_S"] + cSlayer.stats["total_letality_S"]) / 5)
        armor_reduction = int(min(armor_reduction, cMonster.armor - cMonster.armor_cap))
        cMonster.armor -= armor_reduction
        return 0, f"(-{armor_reduction} 🛡️)"
    else:
      return 0, ""
