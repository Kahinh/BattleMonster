import datetime

class DamageDone:
  def __init__(
    self, 
    cooldown = 0,
    total_damage = 0,
    eligible=False,
    luck = 0
    ):
    self.total_damage = total_damage
    self.mult_spe = 0
    self.timestamp_next_hit = cooldown + datetime.datetime.timestamp(datetime.datetime.now())
    self.eligible = eligible
    self.luck = luck

  def checkStatus(self, damage, monster_base_hp):
    content = ""
    if self.total_damage > damage and self.total_damage > 0:
        content += f"\n> 🔱 Dégâts infligés totaux : {int(self.total_damage)}"
    #If Battle.eligible == False, on rajoute que le mec est pas éligible ! Sinon on affiche qu'il est éligible !
    if self.eligible:
        #En ayant infligé des dégâts au Monstre, tu es éligible !
        content += f"\n\n> ✨ **En ayant infligé des dégâts au Monstre, tu es éligible à l'obtention de butin !**"
    else:
        content += f"\n\n> 🛑 **Tu n'es, pour l'instant, pas éligible à l'obtention de butin !**"

    #Puis, on rajoute la vivacité !
    if self.timestamp_next_hit - datetime.datetime.timestamp(datetime.datetime.now()) <= 1:
        content += f"\n\n> Tu peux **attaquer avec une Attaque Légère ou une Attaque Lourde !**"
    else:
        if monster_base_hp > 0:
            content += f"\n\n> Grâce à ta vivacité, tu pourras attaquer, ce monstre, de nouveau dans **{int(self.timestamp_next_hit - datetime.datetime.timestamp(datetime.datetime.now()))}s**."
    return content

  def updateClass(self, Damage, Cooldown=None, luck=0):
    if Cooldown is not None:
      self.timestamp_next_hit = datetime.datetime.timestamp(datetime.datetime.now()) + Cooldown
    if Damage > 0:
      self.total_damage += Damage
      self.eligible = True
      self.luck = luck
    
  def canAttack(self):
    if self.timestamp_next_hit < datetime.datetime.timestamp(datetime.datetime.now()):
      return True
    else:
      return False