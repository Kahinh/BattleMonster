from copy import deepcopy

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
    if self.id == 1:
      Slots["weapon"]["count"] = 2
    #TEMPLIER
    if self.id == 3:
      Slots["shield"]["count"] = 1
    return Slots
