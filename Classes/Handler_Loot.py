import random

import os, inspect, sys
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from Classes.Items import Item

class Loot:
  def __init__(
    self,
    Battle
    ):
    self.bot = Battle.bot
    self.Battle = Battle

    #On crée les requests à la dB
    self.storage_loots = {}
    self.request_opponents_killed_achievement = []
    self.request_mythic_stones = []
    self.request_money = []
    self.request_items = []

  async def award_eligibleLooters(self):
    #On check les monstres 1 par 1
    for i in self.Battle.Opponents:
      if self.Battle.Opponents[i].base_hp == 0 and len(self.Battle.LootTable[i]) > 0:
        #On fait le tour de tous les slayers ayant attaqué
        for id in self.Battle.Opponents[i].slayers_hits:
            #On ne considère que les éligibles
            if self.Battle.Opponents[i].slayers_hits[id].eligible:
              #On récupère le Slayer
              Slayer = await self.bot.ActiveList.get_Slayer(id, "")
              
              #On distribue l'achievement Monsters killed
              self.achievement_opponents_killed(Slayer)

              #On distribue les mythiques
              self.award_mythics_stones(Slayer, self.Battle.Opponents[i])

              #On distribue les loots
              self.award_loots(Slayer, self.Battle.Opponents[i])

              #On revoit les butins : AutoVente ou vrai distrib ?
              await self.review_loots()

              #On rajoute les loots dans le Battle (Pour le recaploot)
              self.Battle.loots = self.storage_loots

              #On push via le dB Manager
              await self.push_dB_request()

  async def push_dB_request(self):
    await self.bot.dB.push_behemoths_killed_achievement(self.request_opponents_killed_achievement)
    await self.bot.dB.push_MythicStones(self.request_mythic_stones)
    await self.bot.dB.push_loots_money(self.request_items, self.request_money)

  async def review_loots(self):
    for id in self.storage_loots:
      Slayer = await self.bot.ActiveList.get_Slayer(id, "")
      self.storage_loot_handler(Slayer)
      for row in self.storage_loots[Slayer.cSlayer.id]["loots"]:

        cItem = Item(row, self.bot)

        #ON VEND AUTOMATIQUEMENT L'ITEM
        if Slayer.isinInventory(cItem.id):
          self.auto_sellItem(Slayer, cItem)
        #ON AJOUTE DANS LA DB INVENTAIRE
        else:
          self.auto_addtoinventoryItem(Slayer, cItem)

  def auto_sellItem(self, Slayer, cItem):
    #On rajoute la monnaie dans la Class Slayer
    Slayer.addMoney(self.bot.Rarities[cItem.rarity].price)

    #On store le give money
    self.storage_loots[Slayer.cSlayer.id]["money"] += self.bot.Rarities[cItem.rarity].price
    self.request_money.append((self.bot.Rarities[cItem.rarity].price, Slayer.cSlayer.id))

    #Puis on ajoute la monnaie gagnée au Battle
    self.Battle.stats["money"] += self.bot.Rarities[cItem.rarity].price

  def auto_addtoinventoryItem(self, Slayer, cItem):
    #On rajoute l'item dans la Class Slayer
    Slayer.addtoInventory(cItem)
    #On store le give item
    self.request_items.append((Slayer.cSlayer.id, cItem.id, 1, False))
    self.storage_loots[Slayer.cSlayer.id]["items"].append(cItem)
    #Puis on ajoute l'item gagné au Battle
    self.Battle.stats["loots"] += 1

  def award_loots(self, Slayer, Opponent):
    #On prend en compte le roll_dice
    for j in range(Opponent.roll_dices):
      #On calcule le loot obtenu
      if random.choices(population=[True, False], weights=[Opponent.slayers_hits[Slayer.cSlayer.id].luck, 1-Opponent.slayers_hits[Slayer.cSlayer.id].luck], k=1)[0]:
        
        #On positionne dans le storage_loot
        self.storage_loot_handler(Slayer)
        self.storage_loots[Slayer.cSlayer.id]["loots"].append(random.choice(Opponent.LootTable))

  def achievement_opponents_killed(self, Slayer):
    Slayer.cSlayer.achievements["monsters_killed"] += 1
    self.request_opponents_killed_achievement.append((1, Slayer.cSlayer.id))

  def award_mythics_stones(self, Slayer, Opponent):
      #Mythic Stones = gatherable 5
      stones_earned = random.randint(1,3)
      Slayer.cSlayer.inventory_gatherables[5] += stones_earned
      self.request_mythic_stones.append((Slayer.cSlayer.id, 5, stones_earned))
      self.Battle.stats["mythic_stones"] += stones_earned

      #On positionne dans le storage_loot
      self.storage_loot_handler(Slayer)
      self.storage_loots[Slayer.cSlayer.id]["mythic_stones"] += stones_earned

  def storage_loot_handler(self, Slayer):
    if Slayer.cSlayer.id not in self.storage_loots:
      self.storage_loots[Slayer.cSlayer.id] = {
        "mythic_stones": 0,
        "items" : [],
        "money" : 0,
        "loots" : []
      }

