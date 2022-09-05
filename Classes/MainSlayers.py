import random
import datetime
import os
import inspect
import sys
from copy import deepcopy

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from Classes.Specialization import Spe
from Classes.Items import Item
from Classes.Queries import qSlayers, qSlayersInventoryItems, qSpe

class MSlayer:
    def __init__(
        self,
        bot,
        user_id,
        user_name
        ):
        self.bot = bot
        self.isExist = False
        self.user_id = user_id
        self.user_name = user_name
        self.cSlayer = None
        self.requests = []

    async def extractdB(self):
        async with self.bot.db_pool.acquire() as conn:
            async with conn.transaction():
                self.rSlayer = await conn.fetchrow(qSlayers.SELECT_SLAYER, self.user_id)
                if self.rSlayer is not None:
                    self.rSlayerInventory = await conn.fetch(qSlayers.SELECT_SLAYER_ROW_INVENTORY, self.user_id)
                    self.rSlayerSpeInventory = await conn.fetch(qSlayers.SELECT_SLAYER_SPE_INVENTORY, self.user_id)
                    self.rSpe = await conn.fetchrow(qSpe.SELECT_SPE, self.rSlayer["specialization"])
                else:
                    self.rSpe = await conn.fetchrow(qSpe.SELECT_SPE, 2)
                    self.rSlayerInventory = []
    
    async def constructClass(self):
        await self.extractdB()
        if self.rSlayer is None:
            self.cSlayer = Slayer(slayer_id=self.user_id, name=self.user_name, bot=self.bot)
            await self.bot.dB.push_slayer_data(self.cSlayer)
        else:
            self.cSlayer = Slayer(
                slayer_id= self.rSlayer["slayer_id"],
                name= self.rSlayer["name"],
                creation_date= self.rSlayer["creation_date"],
                dead= self.rSlayer["dead"],
                xp= self.rSlayer["xp"],
                money= self.rSlayer["money"],
                damage_taken= self.rSlayer["damage_taken"],
                special_stacks= self.rSlayer["special_stacks"],
                faction= self.rSlayer["faction"],
                specialization= self.rSlayer["specialization"],
                inventory_items={},
                inventory_specializations=[int(dict(spe)['specialization_id']) for spe in self.rSlayerSpeInventory],
                bot = self.bot
            )

        for row in self.rSlayerInventory:
            self.cSlayer.inventory_items[row["id"]] = Item(row)

        await self.updateSlayer()   

    async def updateSlayer(self):
            #SLOTS
        self.cSlayer.slots = self.getSlots()
        self.cSlayer.Spe = Spe(self.rSpe)
        self.cSlayer.slots_count = self.cSlayer.Spe.adjust_slot_count(self.bot.rSlots)

        self.cSlayer.calculateStats(self.bot.rBaseBonuses)
        self.GetGearScore()

        await self.bot.ActiveList.update_interface(self.cSlayer.slayer_id, "profil")

    async def equip_item(self, cItem):
        hasbeenequipped = False
        alreadyequipped_list = []
        #D'ABORD ON CHECK QUE L'ITEM EST BIEN DANS L'INVENTAIRE
        if self.isinInventory(cItem.item_id):
            #SI ON PEUT EQUIPER QU'UNE FOIS UN ITEM, ON S'EN FOUT. ON UPDATE OU INSERT
            if self.cSlayer.slots_count[cItem.slot]["count"] == 1:
                #ON A DEJA UN ITEM EQUIPER ET IL FAUT SWITCH
                if cItem.slot in self.cSlayer.slots:
                    #On sécurise si jamais l'item est déjà équippé
                    if cItem.item_id not in self.cSlayer.slots[cItem.slot]:
                        self.cSlayer.inventory_items[self.cSlayer.slots[cItem.slot][0]].unequip()
                        cItem.equip()
                        await self.bot.dB.switch_item(self.cSlayer, cItem, self.cSlayer.inventory_items[self.cSlayer.slots[cItem.slot][0]])
                        hasbeenequipped = True
                #ON A PAS D'ITEM EQUIPER
                else:
                    cItem.equip()
                    await self.bot.dB.equip_item(self.cSlayer, cItem)
                    hasbeenequipped = True
            #SI ON PEUT EQUIPER PLUSIEURS ITEMS SUR LE MEME EMPLACEMENT
            elif self.cSlayer.slots_count[cItem.slot]["count"] > 1:  
                #SOIT ON A PAS ENCORE D'ITEMS
                if cItem.slot not in self.cSlayer.slots:
                    cItem.equip()
                    await self.bot.dB.equip_item(self.cSlayer, cItem)
                    hasbeenequipped = True    
                #SOIT ON A ENCORE DE LA PLACE
                else:
                    #On sécurise si jamais l'item est déjà équippé
                    if cItem.item_id not in self.cSlayer.slots[cItem.slot]:
                        if len(self.cSlayer.slots[cItem.slot]) < self.cSlayer.slots_count[cItem.slot]["count"]:
                            cItem.equip()
                            await self.bot.dB.equip_item(self.cSlayer, cItem)
                            hasbeenequipped = True                   
                        #SOIT ON A PLUS DE PLACE
                        else:
                            alreadyequipped_list = self.cSlayer.slots[cItem.slot]
        if hasbeenequipped:
            await self.updateSlayer()
        return hasbeenequipped, alreadyequipped_list

    async def sell_item(self, cItem):
        #On update la BDD avec la vente
        if self.isinInventory(cItem.item_id):
            self.removefromInventory(cItem)
            await self.updateSlayer()
            await self.bot.dB.sell_item(self.cSlayer, cItem)
            return True
        else:
            return False

    def getSlots(self):
        slots = {}
        for item_id in self.cSlayer.inventory_items:
            if self.cSlayer.inventory_items[item_id].equipped:
                if self.cSlayer.inventory_items[item_id].slot not in slots: slots[self.cSlayer.inventory_items[item_id].slot] = []
                slots[self.cSlayer.inventory_items[item_id].slot].append(item_id)
        return slots

    def isinInventory(self, item_id):
        if item_id in self.cSlayer.inventory_items:
            return True
        else:
            return False
    
    def addtoInventory(self, cItem):
        self.cSlayer.inventory_items[cItem.item_id] = cItem

    def removefromInventory(self, cItem):
        self.cSlayer.inventory_items.pop(cItem.item_id)

    def addMoney(self, money):
        self.cSlayer.money += money
    
    def removeMoney(self, money):
        self.cSlayer.monney -= money

    def GetGearScore(self):
        gearscore = 0
        for item in self.cSlayer.inventory_items:
            if self.cSlayer.inventory_items[item].equipped:
                gearscore += self.bot.rRarities[self.cSlayer.inventory_items[item].rarity]["gearscore"]
        self.cSlayer.gearscore = gearscore

class Slayer:
    def __init__(
        self,
        slayer_id,
        name,
        bot,
        creation_date=datetime.datetime.timestamp(datetime.datetime.now()),
        dead=False,
        xp=0,
        money=10,
        damage_taken=0,
        special_stacks=0,
        faction=0,
        specialization=2,
        Spe=None,
        inventory_items={},
        inventory_specializations=[1],
        slots={},
        stats = {},
        slots_count = {}
        ):
        self.slayer_id = slayer_id
        self.name = name
        self.creation_date = creation_date
        self.dead = dead
        self.xp = xp
        self.damage_taken = damage_taken
        self.money = money
        self.special_stacks = special_stacks
        self.faction = faction
        self.specialization = specialization
        self.Spe = Spe
        self.inventory_items = inventory_items
        self.inventory_specializations = inventory_specializations
        self.slots = slots
        self.stats = stats
        self.slots_count = slots_count
        self.bot = bot

    def calculateBonuses(self, rBaseBonuses):
        bonuses = {
            "armor" : rBaseBonuses["armor"],
            "armor_per" : 0,
            "health" : rBaseBonuses["hp"],
            "health_per" : 0,
            "parry_L" : 0,
            "parry_H" : 0,
            "parry_S" : 0,
            "fail_L" : rBaseBonuses["fail_L"],
            "fail_H" : rBaseBonuses["fail_H"],
            "damage_weapon" : 0,
            "damage_L" : rBaseBonuses["damage_L"],
            "damage_H" : rBaseBonuses["damage_H"],
            "damage_S" : self.Spe.damage,
            "final_damage_L" : 0,
            "final_damage_H" : 0,
            "final_damage_S" : 0,
            "damage_per_L" : 0,
            "damage_per_H" : 0,
            "damage_per_S" : 0,
            "letality_L" : 0,
            "letality_H" : 0,
            "letality_S" : 0,
            "letality_per_L" : 0,
            "letality_per_H" : 0,
            "letality_per_S" : 0,
            "crit_chance_L" : rBaseBonuses["crit_chance_L"],
            "crit_chance_H" : rBaseBonuses["crit_chance_H"],
            "crit_chance_S" : rBaseBonuses["crit_chance_S"],
            "crit_damage_L" : rBaseBonuses["crit_damage_L"],
            "crit_damage_H" : rBaseBonuses["crit_damage_H"],
            "crit_damage_S" : rBaseBonuses["crit_damage_S"],
            "special_charge_L" : rBaseBonuses["special_charge_L"],
            "special_charge_H" : rBaseBonuses["special_charge_H"],
            "special_charge_S" : 0,
            "stacks_reduction" : 0,
            "luck": rBaseBonuses["luck"],
            "vivacity": rBaseBonuses["vivacity"]
        }

        for item_id in self.inventory_items:
            if self.inventory_items[item_id].equipped:
                for bonus in self.inventory_items[item_id].bonuses:
                    bonuses[bonus] += self.inventory_items[item_id].bonuses[bonus]
        self.bonuses = bonuses

    def calculateStats(self, rBaseBonuses):

        self.calculateBonuses(rBaseBonuses)
        bonuses = self.bonuses
        stats = {
            "total_armor" : int(bonuses["armor"]*(1+bonuses["armor_per"])),
            "total_max_health" : int(bonuses["health"]*(1+bonuses["health_per"])),
            "total_fail_L" : float(min(max(bonuses["fail_L"],0),1)),
            "total_fail_H" : float(min(max(bonuses["fail_H"],0),1)),
            "total_fail_S" : 0,
            "total_parry_L" : float(bonuses["parry_L"]),
            "total_parry_H" : float(bonuses["parry_H"]),
            "total_parry_S" : 0,
            "total_damage_L" : int((bonuses["damage_L"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_L"])),
            "total_damage_H" : int((bonuses["damage_H"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_H"])),
            "total_damage_S" : int((bonuses["damage_S"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_S"])),
            "total_final_damage_L" : float(bonuses["final_damage_L"]),
            "total_final_damage_H" : float(bonuses["final_damage_H"]),
            "total_final_damage_S" : float(bonuses["final_damage_S"]),
            "total_crit_chance_L" : float(min(bonuses["crit_chance_L"],1)),
            "total_crit_chance_H" : float(min(bonuses["crit_chance_H"],1)),
            "total_crit_chance_S" : float(min(bonuses["crit_chance_S"],1)),
            "total_crit_damage_L" : float(bonuses["crit_damage_L"]),
            "total_crit_damage_H" : float(bonuses["crit_damage_H"]),
            "total_crit_damage_S" : float(bonuses["crit_damage_S"]),
            "total_letality_L" : int(bonuses["letality_L"]),
            "total_letality_H" : int(bonuses["letality_H"]),
            "total_letality_S" : int(bonuses["letality_S"]),
            "total_letality_per_L" : float(bonuses["letality_per_L"]),
            "total_letality_per_H" : float(bonuses["letality_per_H"]),
            "total_letality_per_S" : float(bonuses["letality_per_S"]),
            "total_special_charge_L" : int(bonuses["special_charge_L"]),
            "total_special_charge_H" : int(bonuses["special_charge_H"]),
            "total_special_charge_S" : int(bonuses["special_charge_S"]),
            "total_stacks_reduction" : int(bonuses["stacks_reduction"]),
            "total_stacks" : int(max(self.Spe.stacks - bonuses["stacks_reduction"], 1)),
            "total_vivacity" : int(bonuses["vivacity"]),
            "total_cooldown" : int(rBaseBonuses["cooldown"] - bonuses["vivacity"]),
            "total_luck" : float(min(max(bonuses["luck"],0),1))
        }
        if stats["total_max_health"] == self.damage_taken:
            self.dead = True
        self.stats = stats

    def CalculateDamage(self, Hit, cMonster):
        #On check si on fail
        isFail = False if Hit == "S" else random.choices(population=[True, False], weights=[self.stats[f"total_fail_{Hit}"], 1-self.stats[f"total_fail_{Hit}"]], k=1)[0]
        isFail = False
        if isFail:
            Damage = 0
            Stacks_Earned = 0
        else: 
            #On check si on est parrty
            isParry = False if Hit == "S" else random.choices(population=[True, False], weights=[min(max(cMonster.parry[f"parry_chance_{Hit}"] - self.stats[f"total_parry_{Hit}"], 0),1), 1-min(max(cMonster.parry[f"parry_chance_{Hit}"] - self.stats[f"total_parry_{Hit}"], 0), 1)], k=1)[0]
            isParry = False
            if isParry:
                Damage = -int(min(cMonster.damage * (1000/(1000 + (self.stats["total_armor"] * (1 - cMonster.letality_per) - cMonster.letality))), self.stats["total_max_health"] - self.damage_taken))
                Stacks_Earned = 0
                #On subit les dégâts
                self.damage_taken += abs(Damage)
                if self.damage_taken == self.stats["total_max_health"]:
                    self.dead = True
            else:
                #On check si on crit
                isCrit = random.choices(population=[True, False], weights=[float(self.stats[f"total_crit_chance_{Hit}"]), float(1-self.stats[f"total_crit_chance_{Hit}"])], k=1)

                #Calcul des dégâts
                Damage = min(int(max((((self.stats[f"total_damage_{Hit}"]*(1 + (self.stats[f"total_crit_damage_{Hit}"] if isCrit[0] else 0)) * (1 + self.stats[f"total_final_damage_{Hit}"]))) - (cMonster.protect_crit if isCrit[0] else 0)), 0)*(1000/(1000+max(((cMonster.armor*(1-self.stats[f"total_letality_per_{Hit}"]))-self.stats[f"total_letality_{Hit}"]),0)))), cMonster.base_hp)
                if Hit == "S":
                    Stacks_Earned = -self.special_stacks
                else:
                    Stacks_Earned = min(self.stats["total_stacks"] - self.special_stacks, self.stats[f"total_special_charge_{Hit}"])
                self.special_stacks += Stacks_Earned

        return Damage, Stacks_Earned

    def canSpecial(self):
        if self.stats["total_stacks"] == self.special_stacks:
            return True, ""
        else:
            return False, f"\n> ☄️ Tu ne possèdes pas le nombre de charges nécessaires - Charge total : **{self.special_stacks}/{self.stats['total_stacks']}**"

    def isSuccess(self, hit):
        isFail = random.choices(population=[True, False], weights=[self.stats[f"total_fail_{hit}"], 1-self.stats[f"total_fail_{hit}"]], k=1)[0]
        if isFail :
            return False, f"\n> - **Attaque esquivée !**"
        else:
            return True, ""
    
    def isCrit(self, hit):
        isCrit = random.choices(population=[True, False], weights=[float(self.stats[f"total_crit_chance_{hit}"]), float(1-self.stats[f"total_crit_chance_{hit}"])], k=1)[0]
        return isCrit

    def dealDamage(self, hit, cMonster):
        armor = self.reduceArmor(hit, cMonster.armor)
        protect_crit = cMonster.protect_crit
        stacks_earned = self.getStacks(hit)
        if self.isCrit(hit):
            damage = min(max(int(self.stats[f"total_damage_{hit}"]*(1 + (self.stats[f"total_crit_damage_{hit}"])) * (1 + self.stats[f"total_final_damage_{hit}"])),0), cMonster.base_hp)
            if damage == 0:
                content = f"\n> Le montre est déjà mort."
            else:
                content = f"\n> ⚔️ {hit} Dégâts infligés : {int(damage)} ‼️ [+{stacks_earned}☄️]"
        else:
            damage = min(max(int(self.stats[f"total_damage_{hit}"] * (1 + self.stats[f"total_final_damage_{hit}"])), 0), cMonster.base_hp)
            if damage == 0:
                content = f"\n> Le montre est déjà mort."
            else:
                content = f"\n> ⚔️ {hit} Dégâts infligés : {int(damage)} [+{stacks_earned}☄️]"
        return damage, content
    
    def reduceArmor(self, hit, armor):
        armor = max(((armor*(1-self.stats[f"total_letality_per_{hit}"]))-self.stats[f"total_letality_{hit}"]),0)
        return armor
    
    def reduceDamage(self, damage, armor):
        damage = -int(min(damage * (1000/(1000 + (armor))), self.stats["total_max_health"] - self.damage_taken))
        return damage

    def getStacks(self, hit):
        stacks_earned = min(self.stats["total_stacks"] - self.special_stacks, self.stats[f"total_special_charge_{hit}"])
        self.special_stacks += stacks_earned
        return stacks_earned

    def useStacks(self, hit):
        if hit == "S":
            content = f"\n> ☄️ Charge consommée : {self.special_stacks} - Charge total : **0/{self.stats['total_stacks']}**"
            self.special_stacks = 0
            return content

    def getDamage(self, damage):
        self.damage_taken += damage

    def isAlive(self):
        if self.dead:
            return False, "> Tu es mort ! Tu ne peux donc pas attaquer pour l'instant 💀"
        else:
            return True, ""

    def getNbrHit(self):
        return self.Spe.nbr_hit(self.bot.rBaseBonuses["hit_number"])

    def recapStacks(self):
        if self.stats["total_stacks"] == self.special_stacks:
            content = f"\n\n> ☄️ Ta capacité spéciale est chargée : Charge total : **{self.special_stacks}/{self.stats['total_stacks']}**"
        else:
            content = f"\n\n ☄️ Charge total : **{self.special_stacks}/{self.stats['total_stacks']}**"
        
        return content

    def recapHealth(self, parries):
        content = f"\n\n> Le monstre t'a infligé {sum(parries)} dégâts."
        if self.stats["total_max_health"] == self.damage_taken:
            content += f"\n> Tu es mort !"
        else:
            content += f"\n> Il te reste {self.stats['total_max_health'] - self.damage_taken}/{self.stats['total_max_health']} ❤️ !"
        return content