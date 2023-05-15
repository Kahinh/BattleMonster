class Attack:
  #Une attack peut avoir plusieurs hits
  def __init__(
    self
    ):
      pass
  
  async def AttackHandler(self, Slayer, cMonster):
      content = "**__Rapport de Combat :__**"
      damage = [] 
      parries = []

      #On check si on est vivant ou mort.
      if Slayer.cSlayer.isAlive()[0]:

        #Si on fait le spécial
        if hit == "s":
          if Slayer.cSlayer.canSpecial()[0]:
            Slayer.cSlayer.useStacks(hit)
            if Slayer.cSlayer.Spe.id != 8: #Berserker
              for i in range(Slayer.cSlayer.getNbrHit()):
                attack, contents = Slayer.cSlayer.dealDamage(hit, cMonster)

                #Pet crit
                if "‼️" in contents:
                  await Slayer.getPet(rate=0.004, pets=[230])

                content += contents
                damage.append(attack)
                cMonster.getDamage(attack)

              #Recap fin des attaques
              content += cMonster.recapDamageTaken(sum(damage))
              cMonster.storeLastHits(sum(damage), Slayer.cSlayer.Spe)
              content += Slayer.cSlayer.recap_useStacks(hit)
              dump = Slayer.cSlayer.recapStacks()
              self.stats['attacks_received'] += 1
              content += cMonster.slayer_storeAttack(Slayer.cSlayer, sum(damage), hit)

              #Achievement Biggest_Hit
              await Slayer.update_biggest_hit(sum(damage))

            else: #Berserker activé:
              content += "\n> Vous avez activé le mode Berserker, vous obtenez 100% Chance Critique et 200% Dégâts Critiques pendant 5 coups !"
              content += Slayer.cSlayer.recap_useStacks(hit)
              Slayer.cSlayer.berserker_mode = 5
              Slayer.cSlayer.calculateStats(self.bot.rBaseBonuses)
          else:
            content += Slayer.cSlayer.canSpecial()[1]
          
        #Si on fait les autres attaques
        else:
          if cMonster.slayer_canAttack(Slayer.cSlayer)[0]:
            for i in range(Slayer.cSlayer.getNbrHit()):
              #On touche ou on fail ?
              ## TODO Mettre un Walrus Operator ici
              isSuccess, message = Slayer.cSlayer.isSuccess(hit)
              if isSuccess:
                #on est parry ou on hit ?
                if cMonster.isParry(hit, Slayer):
                  parry, message = cMonster.dealDamage(Slayer)
                  Slayer.cSlayer.getDamage(parry)
                  parries.append(parry)
                  content += message
                else:
                  attack, contents = Slayer.cSlayer.dealDamage(hit, cMonster)
                  #Pet crit
                  if "‼️" in contents:
                    await Slayer.getPet(rate=0.004, pets=[230])

                  content += contents
                  damage.append(attack)
                  cMonster.getDamage(attack)
              else:
                content += message

            #Recap fin des attaques
            if sum(damage) > 0:
              await Slayer.getPet(pets=[194])
              content += cMonster.recapDamageTaken(sum(damage))
              cMonster.storeLastHits(sum(damage), Slayer.cSlayer.Spe)
              content += Slayer.cSlayer.recapStacks()
              self.stats['attacks_received'] += 1
              
              #Achievement Biggest_Hit
              await Slayer.update_biggest_hit(sum(damage))

            if sum(parries) > 0:
              await Slayer.getPet(pets=[193])
              isDead, message = Slayer.cSlayer.recapHealth(parries)
              content += message
              self.stats['attacks_done'] += sum(parries)
              if isDead:
                self.stats['kills'] += 1
            content += cMonster.slayer_storeAttack(Slayer.cSlayer, sum(damage), hit)

          else:
            content += cMonster.slayer_canAttack(Slayer.cSlayer)[1]

      else:
        content += Slayer.cSlayer.isAlive()[1]

      #On update l'embed du combat
      await self.bot.dB.push_slayer_data(Slayer.cSlayer)

      monster_killed = False
      if self.Monsters[self.count].base_hp == 0:
          if self.count == self.spawns_count - 1:
              self.end = True
          else:
              self.count += 1
              monster_killed = True

      #On clôture l'action
      return content, damage, monster_killed


class Hit:
  def __init__(
    self
    ):
    pass