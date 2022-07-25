import datetime

class DamageDone:
  def __init__(
    self, 
    timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now()),
    total_damage = 0,
    eligible=False
    ):
    self.total_damage = total_damage
    self.timestamp_next_hit = timestamp_next_hit
    self.eligible = eligible

  def updateClass(self, Damage, Cooldown):
    self.timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now()) + Cooldown
    if Damage > 0:
      self.total_damage += Damage
      self.eligible = True