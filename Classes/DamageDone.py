import datetime

class DamageDone:
  def __init__(
    self, 
    timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now()),
    total_damage = 0,
    eligible=False
    ):
    self.total_damage = total_damage
    self.mult_spe = 1
    self.timestamp_next_hit = timestamp_next_hit
    self.eligible = eligible

  def updateClass(self, Damage, Cooldown=None):
    if Cooldown is not None:
      self.timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now()) + Cooldown
    if Damage > 0:
      self.total_damage += Damage
      self.eligible = True