class Attack:
  #Une attack peut avoir plusieurs hits
  def __init__(
    self,
    Slayer,
    Battle,
    hit
    ):
      self.Slayer = Slayer
      self.Battle = Battle
      self.hit = hit

      #Simplification des args
      self.cOpponent = self.Battle.Opponents[self.Battle.count]
      self.cSlayer = self.Slayer.cSlayer

      #Initiation du content
      self.content = "**__Rapport de Combat :__**"
      self.total_damage_dealt = 0
      self.total_damage_taken = 0

      #Init des coups
      self.hits = []
  
  async def AttackHandler(self):

    #On check si on est vivant ou mort.
    if (isAlive := self.cSlayer.isAlive()) and not isAlive[0]:
      return isAlive[1], 0
    
    #On peut special
    if (canSpecial := self.cSlayer.canSpecial()) and not canSpecial[0] and self.hit == "S":
      return canSpecial[1], 0
      
    #On peut attaquer selon le timing
    if (canAttack := self.cOpponent.slayer_canAttack(self.cSlayer)) and not canAttack[0] and self.hit != "S":
      return canAttack[1], 0
    
    #Spe Berserker
    if self.hit == "S" and self.cSlayer.Spe.id == 8:
      self.cSlayer.berserker_mode = 5
      self.cSlayer.calculateStats(self.bot.rBaseBonuses)
      self.content = "\n> Vous avez activé le mode Berserker, vous obtenez 100% Chance Critique et 200% Dégâts Critiques pendant 5 coups !"
      self.content += self.cSlayer.recap_useStacks(self.hit)
      return self.content, 0

    
    #Nombre de hits que le Slayer peut faire :
    for i in range(self.cSlayer.getNbrHit()):
      HitData = Hit(self.Slayer, self.Battle, self.hit)
      self.total_damage_dealt += HitData.damage_dealt
      self.total_damage_taken += HitData.damage_taken
      #On prend le content
      self.content += HitData.content

      #Le monstre prend des dégâts
      if HitData.damage_dealt > 0:
        self.cOpponent.getDamage(HitData.damage_dealt)
      #Le joueur prend des dégâts.
      if HitData.damage_taken > 0:
        self.cSlayer.getDamage(HitData.damage_taken)

    #On récap ce qui a été fait à l'adversaire
    if self.total_damage_dealt > 0:
      self.Opponent_Receive_Damage()

    #On utilise les stacks
    if self.hit == "S":
      self.content += self.cSlayer.recap_useStacks(self.hit)
    else:
      self.content += self.cSlayer.recapStacks()

    #On récap ce qui a été fait au Slayer  
    if self.total_damage_taken > 0:
      self.Slayer_Receive_Damage()

    #Familier 
      #Critique
    if HitData.is_Crit:
      await self.Slayer.getPet(rate=0.004, pets=[230])
      #Damage
    if self.total_damage_dealt > 0:
      await self.Slayer.getPet(pets=[194])
      #Armor
    if self.total_damage_taken > 0:
      await self.Slayer.getPet(pets=[193])
    #Achievement Biggest_Hit
      await self.Slayer.update_biggest_hit(self.total_damage_dealt)

    return self.content, self.total_damage_dealt


  def Slayer_Receive_Damage(self):
    isDead, message = self.cSlayer.recapHealth(self.total_damage_taken)
    self.content += message
    self.Battle.stats['attacks_done'] += self.total_damage_taken
    if isDead:
      self.Battle.stats['kills'] += 1

  def Opponent_Receive_Damage(self):
    self.content += self.cOpponent.recapDamageTaken(self.total_damage_dealt)
    self.cOpponent.storeLastHits(self.total_damage_dealt, self.cSlayer.Spe)
    self.Battle.stats['attacks_received'] += 1
    self.content += self.cOpponent.slayer_storeAttack(self.cSlayer, self.total_damage_dealt, self.hit)


class Hit:
  def __init__(
    self,
    Slayer,
    Battle,
    hit
    ):

    self.Slayer = Slayer
    self.Battle = Battle
    self.hit = hit
  
    #Simplification des args
    self.cOpponent = self.Battle.Opponents[self.Battle.count]
    self.cSlayer = self.Slayer.cSlayer

    #Initiation du content
    self.content = ""
    self.damage_dealt = 0
    self.damage_taken = 0

    if self.cSlayer.isAlive()[0]:
      if self.cOpponent.base_hp > 0:
        if self.isSuccess_Fail():
          if self.isSuccess_Parry:
            self.is_Crit = self.isCrit()
            self.damage_dealt, self.content = self.cSlayer.dealDamage(hit, self.cOpponent, self.is_Crit, self.CritMult(), self.ProtectCrit(), self.ArmorMult(self.Armor()))
            self.getStacks()
          else:
            self.damage_taken, self.content = self.cOpponent.dealDamage(self.Slayer)

  def isSuccess_Fail(self):
    if True:
      return True
    else:
      self.content = f"\n> Raté !"
      return False
    
  def isSuccess_Parry(self):
    if self.cOpponent.isParry(self.hit, self.Slayer):
      return True
    else:
      return False
  
  def isCrit(self):
    return self.cSlayer.isCrit(self.hit)
  
  def CritMult(self):
    if self.is_Crit:
      return self.cSlayer.stats[f"total_crit_damage_{self.hit}"]
    else:
      return 0
  
  def ProtectCrit(self):
    if self.is_Crit:
      return self.cOpponent.protect_crit
    else:
      return 0
    
  def Armor(self):
    return self.cSlayer.reduceArmor(self.hit, self.cOpponent.armor)
  
  def ArmorMult(self, armor):
    if armor >= 0:
        return float((1000/(1000+armor)))
    if armor < 0:
        return float(1+(((1000+abs(armor))/1000)/5))
  
  def getStacks(self):
    stacks_earned = self.cSlayer.getStacks(self.hit)
    self.content += f"[+{stacks_earned}☄️]"