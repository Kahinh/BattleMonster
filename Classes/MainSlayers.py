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
        interaction
        ):
        self.bot = bot
        self.isExist = False
        self.interaction = interaction
        self.cSlayer = None
        self.requests = []

    async def extractdB(self):
        async with self.bot.db_pool.acquire() as conn:
            async with conn.transaction():
                self.rItemsSlayer = await conn.fetch(qSlayers.SELECT_SLAYER_ITEMS, self.interaction.user.id)
                self.rSlayer = await conn.fetchrow(qSlayers.SELECT_SLAYER, self.interaction.user.id)
                if self.rSlayer is not None:
                    self.rSlayerInventory = await conn.fetch(qSlayers.SELECT_SLAYER_ROW_INVENTORY, self.interaction.user.id)
                    self.rSlayerSpeInventory = await conn.fetch(qSlayers.SELECT_SLAYER_SPE_INVENTORY, self.interaction.user.id)
                    self.rSpe = await conn.fetchrow(qSpe.SELECT_SPE, 1)
                else:
                    self.rSpe = await conn.fetchrow(qSpe.SELECT_SPE, self.rSlayer["specialization"])
    
    async def constructClass(self):
        await self.extractdB()
        if self.rSlayer is None:
            self.cSlayer = Slayer(slayer_id=self.interaction.user.id, name=self.interaction.user.name, ratio_armor=self.bot.rBaseBonuses["ratio_armor"])
        else:
            self.isExist = True
            self.cSlayer = Slayer(
                slayer_id= self.rSlayer["slayer_id"],
                name= self.rSlayer["name"],
                ratio_armor=self.bot.rBaseBonuses["ratio_armor"],
                creation_date= self.rSlayer["creation_date"],
                dead= self.rSlayer["dead"],
                xp= self.rSlayer["xp"],
                money= self.rSlayer["money"],
                damage_taken= self.rSlayer["damage_taken"],
                special_stacks= self.rSlayer["special_stacks"],
                faction= self.rSlayer["faction"],
                specialization= self.rSlayer["specialization"],
                inventory_specializations=[int(dict(spe)['specialization_id']) for spe in self.rSlayerSpeInventory],
                slots= self.getSlots()
            )
        for item in self.rSlayerInventory:
            self.cSlayer.inventory_items.append(Item(item))
        self.cSlayer.Spe = Spe(self.rSpe)
        self.cSlayer.stats = self.cSlayer.calculateStats(self.bot.rBaseBonuses, self.rItemsSlayer)
        self.cSlayer.slots_count = self.cSlayer.Spe.adjust_slot_count(self.bot.rSlots)
    
    def getSlots(self):
        slots = {}
        if self.rItemsSlayer != []:
            for row in self.rItemsSlayer:
                if row["slot"] not in slots: slots[row["slot"]] = []
                slots[row["slot"]].append(Item(row))
        return slots

    async def pushdB(self):
        if self.requests != []:
            async with self.bot.db_pool.acquire() as conn:
                async with conn.transaction():
                    for request in self.requests:
                        await conn.execute(request)
            self.requests = []

    async def equip_item(self, cItem):
        isEquipped = False
        alreadyequipped_List = []
        #D'ABORD ON CHECK QUE L'ITEM EST BIEN DANS L'INVENTAIRE
        if self.isinInventory(cItem):
            #SI ON PEUT EQUIPER QU'UNE FOIS UN ITEM, ON S'EN FOUT. ON UPDATE OU INSERT
            if self.cSlayer.slots_count[cItem.slot]["count"] == 1:
                if cItem.slot in self.cSlayer.slots:
                    async with self.bot.db_pool.acquire() as conn:
                        await conn.execute(f'UPDATE "Slayers_Slots" SET item_id = {cItem.item_id} WHERE slayer_id = {self.cSlayer.slayer_id} AND slot = \'{cItem.slot}\'')
                else:
                    async with self.bot.db_pool.acquire() as conn:
                        await conn.execute(f'INSERT INTO "Slayers_Slots" (slayer_id, slot, item_id) VALUES ({self.cSlayer.slayer_id}, \'{cItem.slot}\', {cItem.item_id})')
                isEquipped = True
            #SI ON PEUT EQUIPER PLUSIEURS ITEMS SUR LE MEME EMPLACEMENT
            elif self.cSlayer.slots_count[cItem.slot]["count"] > 1:
                if cItem.slot in self.cSlayer.slots:
                    #ON CHECK SI L'ITEM EST PAS DEJA EQUIPEE
                    if not self.isinSlot(cItem):
                        if len(self.cSlayer.slots[cItem.slot]) < self.cSlayer.slots_count[cItem.slot]["count"]:
                            async with self.bot.db_pool.acquire() as conn:
                                await conn.execute(f'INSERT INTO "Slayers_Slots" (slayer_id, slot, item_id) VALUES ({self.cSlayer.slayer_id}, \'{cItem.slot}\', {cItem.item_id})')             
                            isEquipped = True
                        else:
                            isEquipped = False
                            alreadyequipped_List = deepcopy(self.cSlayer.slots[cItem.slot])
                    else:
                        isEquipped = False
                #SOIT ON A PAS ENCORE D'ITEMS DANS CET EMPLACEMENT ET Y A QUA INSERT
                else:
                    async with self.bot.db_pool.acquire() as conn:
                        await conn.execute(f'INSERT INTO "Slayers_Slots" (slayer_id, slot, item_id) VALUES ({self.cSlayer.slayer_id}, \'{cItem.slot}\', {cItem.item_id})')             
                    isEquipped = True                
            else:
                isEquipped = False
    
        return isEquipped, alreadyequipped_List

    async def sell_item(self, cItem):
        #On update la BDD avec la vente
        if self.isinInventory(cItem):
            async with self.bot.db_pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f'DELETE FROM "Slayers_Inventory_Items" WHERE slayer_id = {self.cSlayer.slayer_id} AND item_id = {cItem.item_id}')
                    await conn.execute(f'DELETE FROM "Slayers_Slots" WHERE slayer_id = {self.cSlayer.slayer_id} AND item_id = {cItem.item_id}')
                    await conn.execute(f'UPDATE "Slayers" SET money = money + {self.bot.rRarities[cItem.rarity]["price"]} WHERE slayer_id = {self.cSlayer.slayer_id}')
            self.removefromInventory(cItem)
            self.removefromSlots(cItem)
            return True
        else:
            return False

    def isinInventory(self, cItem):
        for item in self.cSlayer.inventory_items:
            if cItem.item_id == item.item_id:
                return True
        return False

    def isinSlot(self, cItem):
        if cItem.slot in self.cSlayer.slots:
            for item in self.cSlayer.slots[cItem.slot]:
                if cItem.item_id == item.item_id:
                    return True
        return False

    def removefromInventory(self, cItem):
        for item in self.cSlayer.inventory_items:
            if cItem.item_id == item.item_id:
                self.cSlayer.inventory_items.remove(item)
                return

    def removefromSlots(self, cItem):
        for item in self.cSlayer.slots[cItem.slot]:
            if cItem.item_id == item.item_id:
                self.cSlayer.slots[cItem.slot].remove(item)
                return

    def Slayer_update(self):
        self.requests.append('INSERT INTO "Slayers" (slayer_id, xp, money, damage_taken, special_stacks, faction, specialization, creation_date, name, dead)' \
            f" VALUES ({self.cSlayer.slayer_id}, {self.cSlayer.xp}, {self.cSlayer.money}, {self.cSlayer.damage_taken}, {self.cSlayer.special_stacks}, {self.cSlayer.faction}, {self.cSlayer.specialization}, {self.cSlayer.creation_date}, '{self.cSlayer.name}', {self.cSlayer.dead})" \
            ' ON CONFLICT (slayer_id) DO ' \
            f'UPDATE SET xp={self.cSlayer.xp}, money={self.cSlayer.money}, damage_taken={self.cSlayer.damage_taken}, special_stacks={self.cSlayer.special_stacks}, faction={self.cSlayer.faction}, specialization={self.cSlayer.specialization}, dead={self.cSlayer.dead}')      

class Slayer:
    def __init__(
        self,
        slayer_id,
        name,
        ratio_armor,
        creation_date=datetime.datetime.timestamp(datetime.datetime.now()),
        dead=False,
        xp=0,
        money=10,
        damage_taken=0,
        special_stacks=0,
        faction=0,
        specialization=1,
        Spe=None,
        inventory_items=[],
        inventory_specializations=[1],
        slots={},
        stats = {},
        slots_count = {}
        ):
        self.slayer_id = slayer_id
        self.name = name
        self.ratio_armor = ratio_armor
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

    def calculateBonuses(self, rBaseBonuses, rItemsSlayer):
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

        if rItemsSlayer is not None:
            for row in rItemsSlayer:
                cItem = Item(row)
                for bonus in cItem.bonuses:
                    bonuses[bonus] += cItem.bonuses[bonus]
        return bonuses

    def calculateStats(self, rBaseBonuses, rItemsSlayer=None):

        bonuses = self.calculateBonuses(rBaseBonuses, rItemsSlayer)
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
        return stats

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
            return True
        return False

    def GetGearScore(self):
        pass




