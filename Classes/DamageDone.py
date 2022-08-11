import datetime

class DamageDone:
  def __init__(
    self, 
    timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now()),
    total_damage = 0,
    eligible=False,
    luck = 0
    ):
    self.total_damage = total_damage
    self.mult_spe = 1
    self.timestamp_next_hit = timestamp_next_hit
    self.eligible = eligible
    self.luck = luck

  def updateClass(self, Damage, Cooldown=None, luck=0):
    if Cooldown is not None:
      self.timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now()) + Cooldown
      self.luck = luck
    if Damage > 0:
      self.total_damage += Damage
      self.eligible = True