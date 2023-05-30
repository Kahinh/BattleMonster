from decimal import Decimal
import random
import datetime
import os
import inspect
import sys
from copy import deepcopy
from collections import defaultdict

from dataclasses import dataclass

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from Classes.Attributes import Spe
from Classes.Objects import Object, Item, Pet, Mythic
from Functions.Messages.Embed import create_embed_new_pet

class MSlayer:
    def __init__(
        self,
        bot,
        user_id,
        user_name
        ):
        self.bot = bot
        self.user_id = user_id
        self.user_name = user_name
        self.cSlayer = None
        
    async def constructClass(self):
        Slayer_Data, Slayer_Inventory_Items, Slayer_Spe_Inventory, Spe_Data, Slayer_Inventory_Gatherables = await self.bot.dB.pull_slayer_data(self.user_id)
        self.cSlayer = Slayer(
            id = self.user_id if Slayer_Data is None else Slayer_Data[0],
            name= self.user_name if Slayer_Data is None else Slayer_Data["name"],
            creation_date = datetime.datetime.timestamp(datetime.datetime.now()) if Slayer_Data is None else Slayer_Data["creation_date"],
            dead= False if Slayer_Data is None else Slayer_Data["dead"],
            xp= 0 if Slayer_Data is None else Slayer_Data["xp"],
            money= 0 if Slayer_Data is None else Slayer_Data["money"],
            damage_taken= 0 if Slayer_Data is None else Slayer_Data["damage_taken"],
            special_stacks= 0 if Slayer_Data is None else Slayer_Data["special_stacks"],
            faction= 0 if Slayer_Data is None else int(Slayer_Data["faction"]),
            beta_tester= False if Slayer_Data is None else Slayer_Data["beta_tester"],
            specialization= 1 if Slayer_Data is None else Slayer_Data["specialization"],
            Spe = self.bot.Specializations[1 if Slayer_Data is None else Slayer_Data["specialization"]],
            inventory_items = {}, #Gérer plus bas
            inventory_gatherables = {},
            inventory_specializations= [1] if Slayer_Spe_Inventory is None else Slayer_Spe_Inventory[0].strip('][').split(','),
            bot = self.bot,

            #Achievements
            monsters_killed = 0 if Slayer_Data is None else Slayer_Data["monsters_killed"],
            biggest_hit = 0 if Slayer_Data is None else Slayer_Data["biggest_hit"]
        )

        #Transforme liste inventaire en liste Class Items dans l'inventaire
        for row in Slayer_Inventory_Items:
            if row["slot"] == "pet":
                self.cSlayer.inventory_items.update({row["id"]: Pet(self.bot, row)})
            else:
                if row["rarity"] == "mythic":
                    self.cSlayer.inventory_items.update({row["id"]: Mythic(self.bot, row)})
                else:
                    self.cSlayer.inventory_items.update({row["id"]: Item(self.bot, row)})
        #On corrige la liste des specializations en liste d'int
        self.cSlayer.inventory_specializations = [eval(str(i)) for i in self.cSlayer.inventory_specializations]

        #Transforme la liste des Slayer Inventory Gatherables
        for row in Slayer_Inventory_Gatherables:
            self.cSlayer.inventory_gatherables.update({row['gatherable_id']: row["amount"]})

        #On crée les tables si besoin
        if Slayer_Data is None:
            await self.bot.dB.push_slayer_data(self.cSlayer)
            await self.bot.dB.push_achievement_data(self.cSlayer)
            await self.bot.dB.push_spe_list(self.cSlayer)

        await self.updateSlayer()   

    async def updateSlayer(self):

        #Spe
        self.cSlayer.slots_count = self.cSlayer.Spe.adjust_slot_count(self.bot.rSlots)

        #Slots
        self.cSlayer.slots = self.getSlots()
        await self.correctSlots()

        self.cSlayer.calculateStats(self.bot.rBaseBonuses)
        self.GetGearScore()

        await self.bot.ActiveList.update_interface(self.cSlayer.id, "profil")

    async def equip_item(self, cObject):
        hasbeenequipped = False
        alreadyequipped_list = []
        #D'ABORD ON CHECK QUE L'ITEM EST BIEN DANS L'INVENTAIRE
        if self.isinInventory(cObject.id):
            #SI ON PEUT EQUIPER QU'UNE FOIS UN ITEM, ON S'EN FOUT. ON UPDATE OU INSERT
            if self.cSlayer.slots_count[cObject.slot]["count"] == 1:
                #ON A DEJA UN ITEM EQUIPER ET IL FAUT SWITCH
                if cObject.slot in self.cSlayer.slots:
                    #On sécurise si jamais l'item est déjà équippé
                    if cObject.id not in self.cSlayer.slots[cObject.slot]:
                        self.cSlayer.inventory_items[self.cSlayer.slots[cObject.slot][0]].unequip()
                        cObject.equip()
                        await self.bot.dB.switch_item(self.cSlayer, cObject, self.cSlayer.inventory_items[self.cSlayer.slots[cObject.slot][0]])
                        hasbeenequipped = True
                #ON A PAS D'ITEM EQUIPER
                else:
                    cObject.equip()
                    await self.bot.dB.equip_item(self.cSlayer, cObject)
                    hasbeenequipped = True
            #SI ON PEUT EQUIPER PLUSIEURS ITEMS SUR LE MEME EMPLACEMENT
            elif self.cSlayer.slots_count[cObject.slot]["count"] > 1:  
                #SOIT ON A PAS ENCORE D'ITEMS
                if cObject.slot not in self.cSlayer.slots:
                    cObject.equip()
                    await self.bot.dB.equip_item(self.cSlayer, cObject)
                    hasbeenequipped = True    
                #SOIT ON A ENCORE DE LA PLACE
                else:
                    #On sécurise si jamais l'item est déjà équippé
                    if cObject.id not in self.cSlayer.slots[cObject.slot]:
                        if len(self.cSlayer.slots[cObject.slot]) < self.cSlayer.slots_count[cObject.slot]["count"]:
                            cObject.equip()
                            await self.bot.dB.equip_item(self.cSlayer, cObject)
                            hasbeenequipped = True                   
                        #SOIT ON A PLUS DE PLACE
                        else:
                            alreadyequipped_list = self.cSlayer.slots[cObject.slot]
        if hasbeenequipped:
            await self.bot.ActiveList.close_interface(self.cSlayer.id, cObject.id)
            await self.updateSlayer()
        return hasbeenequipped, alreadyequipped_list

    async def sell_item(self, cObject):
        #On update la BDD avec la vente
        if self.isinInventory(cObject.id):
            self.removefromInventory(cObject)
            await self.bot.ActiveList.close_interface(self.cSlayer.id, cObject.id)
            await self.updateSlayer()
            await self.bot.dB.sell_item(self.cSlayer, cObject)
            return True
        else:
            return False

    def getSlots(self):
        slots = {}
        for id in self.cSlayer.inventory_items:
            if self.cSlayer.inventory_items[id].equipped:
                if self.cSlayer.inventory_items[id].slot not in slots: slots[self.cSlayer.inventory_items[id].slot] = []
                slots[self.cSlayer.inventory_items[id].slot].append(id)
        return slots

    async def correctSlots(self):
        gotError = False
        for slot in self.cSlayer.slots:
            if len(self.cSlayer.slots[slot]) > self.cSlayer.slots_count[slot]["count"]:
                self.cSlayer.inventory_items[self.cSlayer.slots[slot][len(self.cSlayer.slots[slot])-1]].equipped = False
                await self.bot.dB.unequip_item(self.cSlayer, self.cSlayer.inventory_items[self.cSlayer.slots[slot][len(self.cSlayer.slots[slot])-1]])
                gotError = True
        
        if gotError:
            self.cSlayer.slots = self.getSlots()
    
    async def update_biggest_hit(self, damage):
        if damage > self.cSlayer.achievements["biggest_hit"]:
            self.cSlayer.achievements["biggest_hit"] = damage
            await self.bot.dB.push_biggest_hit_achievement(self.cSlayer)

    def isinInventory(self, id):
        if id in self.cSlayer.inventory_items:
            return True
        else:
            return False
    
    def isEquipped(self, id):
        if id in self.cSlayer.inventory_items:
            if self.cSlayer.inventory_items[id].equipped:
                return True
            else:
                return False
        else:
            return True
    
    def addtoInventory(self, cObject):
        self.cSlayer.inventory_items[cObject.id] = cObject

    def removefromInventory(self, cObject):
        self.cSlayer.inventory_items.pop(cObject.id)

    def addMoney(self, money):
        self.cSlayer.money += money

    def removeMoney(self, money):
        self.cSlayer.money -= money

    def GetGearScore(self):
        gearscore = 0
        for item in self.cSlayer.inventory_items:
            if self.cSlayer.inventory_items[item].equipped:
                gearscore += self.cSlayer.inventory_items[item].gearscore
        self.cSlayer.gearscore = gearscore

    def equippedonSlot(self, slot):
        items_list = ""
        for id in self.cSlayer.inventory_items:
            cObject = self.cSlayer.inventory_items[id]
            if cObject.equipped and cObject.slot == slot:
                items_list += f"\n- {self.bot.Elements[cObject.element].display_emote} {cObject.name} - *{self.bot.Rarities[cObject.rarity].display_text}*"
        
        if items_list != "":
            description = "\n\n__Objet(s) actuellement équipés à cet emplacement :__" + items_list
        else:
            description = ""
        return description

    def getListEquippedOnSlot(self, slot):
        items_list = []
        if slot in self.cSlayer.slots:
            for id in self.cSlayer.slots[slot]:
                items_list.append(self.cSlayer.inventory_items[id])
        return items_list
    
    async def getDrop(self, rate=0.01, pets=[]):
        if random.choices((True, False), (rate, 1-rate), k=1)[0]:
            pet_id = random.choice(pets)
            if not self.isinInventory(pet_id):
                rDrop = await self.bot.dB.get_rPet(pet_id)
                cObject = Object.get_Object_Class(self.bot, rDrop)

                #On ajoute au stuff
                self.addtoInventory(cObject)

                #On ajoute le stuff à la dB
                await self.bot.dB.add_item(self.cSlayer, cObject)

                #On poste le message
                embed = create_embed_new_pet(self.bot, self, cObject)
                channel = self.bot.get_channel(self.bot.rChannels["loots"])
                await channel.send(content=f"<@{self.cSlayer.id}>",embed=embed)

    async def update_inventory_gatherables(self, gatherable_id, amount):
        self.cSlayer.inventory_gatherables[gatherable_id] += amount
        await self.bot.dB.push_Gather(self.cSlayer.id, gatherable_id, self.cSlayer.inventory_gatherables[gatherable_id])

@dataclass
class Slayer:
    id: int
    name: str
    money: int
    damage_taken: int
    special_stacks: int
    faction: int
    specialization: int
    dead: bool

    def __init__(
        self,
        id,
        name,
        bot,
        creation_date=datetime.datetime.timestamp(datetime.datetime.now()),
        dead=False,
        xp=0,
        money=10,
        damage_taken=0,
        special_stacks=0,
        faction=0,
        beta_tester=False,
        specialization=1, #TODO Nettoyer pour eviter les deux Specialization & Spe
        Spe=None, #TODO Nettoyer pour eviter les deux Specialization & Spe
        inventory_items={},
        inventory_specializations=[1],
        inventory_gatherables={},
        slots={},
        stats = {},
        slots_count = {},

        #Achievements
        monsters_killed = 0,
        biggest_hit = 0

        ):
        self.bot = bot

        self.id = id
        self.name = name
        self.creation_date = creation_date
        self.dead = dead
        self.xp = xp
        self.damage_taken = damage_taken
        self.money = money
        self.special_stacks = special_stacks
        self.faction = faction
        self.beta_tester = beta_tester
        self.specialization = specialization
        self.Spe = Spe
        self.inventory_items = inventory_items
        self.inventory_specializations = inventory_specializations
        self.inventory_gatherables = inventory_gatherables
        self.inventory_gatherables = defaultdict(int)
        self.slots = slots
        self.stats = stats
        self.slots_count = slots_count

        #regen
        self.lastregen = datetime.datetime.timestamp(datetime.datetime.now()) - 1200
        self.firstregen = False

        self.gearscore = 0

        self.mult_damage = 0 #Spe Démon
        self.berserker_mode = 0

        #Achievements
        self.achievements = {
            'monsters_killed' : monsters_killed if monsters_killed is not None else 0,
            'biggest_hit' : biggest_hit if biggest_hit is not None else 0
        }

    def calculateBonuses(self, rBaseBonuses):
        bonuses = {
            "armor" : rBaseBonuses["armor"] + self.Spe.bonuses["armor"],
            "armor_per" : float(self.Spe.bonuses["armor_per"]),
            "health" : rBaseBonuses["hp"] + self.Spe.bonuses["health"],
            "health_per" : float(self.Spe.bonuses["health_per"]),
            "parry_l" : float(self.Spe.bonuses["parry_l"]),
            "parry_h" : float(self.Spe.bonuses["parry_h"]),
            "parry_s" : float(0),
            "damage_weapon" : self.Spe.bonuses["damage_weapon"],
            "damage_l" : rBaseBonuses["damage_l"] + self.Spe.bonuses["damage_l"],
            "damage_h" : rBaseBonuses["damage_h"] + self.Spe.bonuses["damage_h"],
            "damage_s" : self.Spe.damage + self.Spe.bonuses["damage_s"],
            "final_damage_l" : float(self.Spe.bonuses["final_damage_l"]),
            "final_damage_h" : float(self.Spe.bonuses["final_damage_h"]),
            "final_damage_s" : float(self.Spe.bonuses["final_damage_s"]),
            "damage_per_l" : float(self.Spe.bonuses["damage_per_l"]),
            "damage_per_h" : float(self.Spe.bonuses["damage_per_h"]),
            "damage_per_s" : float(self.Spe.bonuses["damage_per_s"]),
            "letality_l" : self.Spe.bonuses["letality_l"],
            "letality_h" : self.Spe.bonuses["letality_h"],
            "letality_s" : self.Spe.bonuses["letality_s"],
            "letality_per_l" : float(self.Spe.bonuses["letality_per_l"]),
            "letality_per_h" : float(self.Spe.bonuses["letality_per_h"]),
            "letality_per_s" : float(self.Spe.bonuses["letality_per_s"]),
            "crit_chance_l" : float(rBaseBonuses["crit_chance_l"]) + float(self.Spe.bonuses["crit_chance_l"]) + (float(self.bot.Variables["assassin_crit_chance_bonus"]) if self.berserker_mode > 0 else 0),
            "crit_chance_h" : float(rBaseBonuses["crit_chance_h"]) + float(self.Spe.bonuses["crit_chance_h"]) + (float(self.bot.Variables["assassin_crit_chance_bonus"]) if self.berserker_mode > 0 else 0),
            "crit_chance_s" : float(rBaseBonuses["crit_chance_s"]) + float(self.Spe.bonuses["crit_chance_s"]) + (float(self.bot.Variables["assassin_crit_chance_bonus"]) if self.berserker_mode > 0 else 0),
            "crit_damage_l" : float(rBaseBonuses["crit_damage_l"]) + float(self.Spe.bonuses["crit_damage_l"]) + (float(self.bot.Variables["assassin_crit_damage_bonus"]) if self.berserker_mode > 0 else 0),
            "crit_damage_h" : float(rBaseBonuses["crit_damage_h"]) + float(self.Spe.bonuses["crit_damage_h"]) + (float(self.bot.Variables["assassin_crit_damage_bonus"]) if self.berserker_mode > 0 else 0),
            "crit_damage_s" : float(rBaseBonuses["crit_damage_s"]) + float(self.Spe.bonuses["crit_damage_s"]) + (float(self.bot.Variables["assassin_crit_damage_bonus"]) if self.berserker_mode > 0 else 0),
            "special_charge_l" : rBaseBonuses["special_charge_l"] + self.Spe.bonuses["special_charge_l"],
            "special_charge_h" : rBaseBonuses["special_charge_h"] + self.Spe.bonuses["special_charge_h"],
            "special_charge_s" : self.Spe.bonuses["special_charge_s"],
            "stacks_reduction" : self.Spe.bonuses["stacks_reduction"],
            "luck": float(rBaseBonuses["luck"]) + float(self.Spe.bonuses["luck"]),
            "vivacity": rBaseBonuses["vivacity"] + self.Spe.bonuses["vivacity"]
        }

        for id in self.inventory_items:
            if self.inventory_items[id].equipped:
                for bonus in self.inventory_items[id].bonuses:
                        if isinstance(bonuses[bonus], int):
                            bonuses[bonus] += int(self.inventory_items[id].bonuses[bonus])
                        elif isinstance(bonuses[bonus], float):
                            bonuses[bonus] += float(round(self.inventory_items[id].bonuses[bonus],2))
                        else:
                            #print(bonuses)
                            bonuses[bonus] += self.inventory_items[id].bonuses[bonus]
        self.bonuses = bonuses

    def calculateStats(self, rBaseBonuses):

        self.calculateBonuses(rBaseBonuses)
        bonuses = self.bonuses
        stats = {
            "total_armor" : int(bonuses["armor"]*(1+bonuses["armor_per"])),
            "total_max_health" : int(bonuses["health"]*(1+bonuses["health_per"])),
            "total_parry_l" : float(bonuses["parry_l"]),
            "total_parry_h" : float(bonuses["parry_h"]),
            "total_parry_s" : 0,
            "total_damage_l" : int((bonuses["damage_l"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_l"])),
            "total_damage_h" : int((bonuses["damage_h"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_h"])),
            "total_damage_s" : int((bonuses["damage_s"] + bonuses["damage_weapon"])*(1+bonuses["damage_per_s"])),
            "total_final_damage_l" : float(max(bonuses["final_damage_l"],0)),
            "total_final_damage_h" : float(max(bonuses["final_damage_h"],0)),
            "total_final_damage_s" : float(max(bonuses["final_damage_s"],0)),
            "total_crit_chance_l" : float(min(bonuses["crit_chance_l"],1)),
            "total_crit_chance_h" : float(min(bonuses["crit_chance_h"],1)),
            "total_crit_chance_s" : float(min(bonuses["crit_chance_s"],1)),
            "total_crit_damage_l" : float(bonuses["crit_damage_l"] + (max(bonuses["crit_chance_l"] - 1, 0) if self.Spe.id == 8 else 0)),
            "total_crit_damage_h" : float(bonuses["crit_damage_h"] + (max(bonuses["crit_chance_h"] - 1, 0) if self.Spe.id == 8 else 0)),
            "total_crit_damage_s" : float(bonuses["crit_damage_s"] + (max(bonuses["crit_chance_s"] - 1, 0) if self.Spe.id == 8 else 0)),
            "total_letality_l" : int(max(bonuses["letality_l"], 0)),
            "total_letality_h" : int(max(bonuses["letality_h"], 0)),
            "total_letality_s" : int(max(bonuses["letality_s"], 0)),
            "total_letality_per_l" : float(max(bonuses["letality_per_l"], 0)),
            "total_letality_per_h" : float(max(bonuses["letality_per_h"], 0)),
            "total_letality_per_s" : float(max(bonuses["letality_per_s"], 0)),
            "total_special_charge_l" : int(max(bonuses["special_charge_l"], 0)),
            "total_special_charge_h" : int(max(bonuses["special_charge_h"], 0)),
            "total_special_charge_s" : int(max(bonuses["special_charge_s"], 0)),
            "total_stacks_reduction" : int(bonuses["stacks_reduction"]),
            "total_stacks" : int(max(self.Spe.stacks - bonuses["stacks_reduction"], 1)),
            "total_vivacity" : int(bonuses["vivacity"]),
            "total_cooldown" : int(max(rBaseBonuses["cooldown"] - bonuses["vivacity"], 1)),
            "total_luck" : float(min(max(bonuses["luck"],0),1))
        }
        if stats["total_max_health"] == self.damage_taken:
            self.dead = True
        if self.dead == True:
            self.damage_taken = stats["total_max_health"]
        else:
            self.damage_taken = min(self.damage_taken, stats["total_max_health"]-1)
        self.stats = stats

    def canSpecial(self):
        if self.special_stacks >= self.stats["total_stacks"]:
            return True, ""
        else:
            return False, f"\n> ☄️ Tu ne possèdes pas le nombre de charges nécessaires - Charge total : **{self.special_stacks}/{self.stats['total_stacks']}**"
    
    def isCrit(self, hit):
        isCrit = random.choices(population=[True, False], weights=[float(self.stats[f"total_crit_chance_{hit}"]), float(1-self.stats[f"total_crit_chance_{hit}"])], k=1)[0]
        return isCrit

    def dealDamage(self, hit, cOpponent, isCrit, CritMult, ProtectCrit, ArmorMult):
        if hit == "s":
            additionnal_damage, additionnal_ability = self.Spe.get_damage(cOpponent, self, hit)
            mult_damage = self.mult_damage
        else:
            additionnal_damage, additionnal_ability = 0, ""
            mult_damage = 0

        #Dégâts de base :
        damage = int(self.stats[f"total_damage_{hit}"] + additionnal_damage + mult_damage)
        #On applique les Mult : Crit & Finaux
        damage = int(damage*(1 + CritMult) * (1 + self.stats[f"total_final_damage_{hit}"]))
        #ProtectCrit
        damage = int(max(damage - ProtectCrit, 0))
        #ArmorMult
        damage = int(max(damage * ArmorMult, 0))
        #A ce stade, si damage = 0, alors le monstre a trop d'armures
        if damage == 0:
            return 0, f"\n> ⚔️ {self.Spe.ability_name if hit == 'S' else hit} : {int(damage)} - L'adversaire possédait trop de défense !"
        #Vie du monstre
        if cOpponent.base_hp is not None:
            damage = int(min(damage, cOpponent.base_hp))
            if damage == 0:
                return 0, f"\n> ⚔️ {self.Spe.ability_name if hit == 'S' else hit} : {int(damage)} - Le {cOpponent.group_name} est déjà mort !"

        content = f"\n> ⚔️ {self.Spe.ability_name if hit == 'S' else hit} : {int(damage)} {'‼️' if isCrit else ''} {'[🔥+' + str(mult_damage) + ']' if mult_damage > 0 else ''} {additionnal_ability if additionnal_ability != '' else ''} {'[🪓' + str(self.berserker_mode -1) + 'restants]' if self.berserker_mode > 0 else ''}"
            
        #Berserker
        if self.berserker_mode > 0 and hit != "S":
            self.berserker_mode -= 1
            if self.berserker_mode == 0:
                self.calculateStats(self.bot.rBaseBonuses)

        return damage, content
    
    def reduceArmor(self, hit, armor):
        #Reduction Fix
        armor = (armor-int(self.stats[f"total_letality_{hit}"]))
        #Reudction %
        if armor > 0:
            armor = armor*(1-float(self.stats[f"total_letality_per_{hit}"]))
        return int(armor)

    def getStacks(self, hit):
        if hit == "s":
            stacks_earned = max(min(int(self.stats["total_stacks"]*0.5) - self.special_stacks, self.stats[f"total_special_charge_{hit}"]),0)
        else:
            stacks_earned = min(self.stats["total_stacks"] - self.special_stacks, self.stats[f"total_special_charge_{hit}"])
        self.special_stacks += stacks_earned
        return stacks_earned

    def getDamage(self, damage):
        self.damage_taken += damage
        if self.stats["total_max_health"] == self.damage_taken:
            self.dead = True

    def isAlive(self):
        if self.dead:
            return False, "> Tu es mort ! Tu ne peux donc pas attaquer pour l'instant 💀"
        else:
            return True, ""

    def getNbrHit(self):
        return self.Spe.nbr_hit(self.bot.rBaseBonuses["hit_number"])

    def recap_useStacks(self, hit):
        if hit == "s":
            if self.Spe.id == 7 and self.special_stacks == self.stats['total_stacks']:
                content = f"\n> ☄️ Charge récupérées, spécial disponible : **{self.special_stacks}/{self.stats['total_stacks']}**"
            else:
                content = f"\n> ☄️ Charge consommée : {self.stats['total_stacks']} - Charge total : **{self.special_stacks}/{self.stats['total_stacks']}**"
            return content
        
    def useStacks(self, hit):
        if hit == "s":
            if self.Spe.id == 7:
                if random.choices((True, False), (float(self.bot.Variables["demon_chance_proc"]), 1-float(self.bot.Variables["demon_chance_proc"])), k=1)[0]:
                    self.mult_damage += int(float(self.bot.Variables["demon_bonus_mult"]) * self.stats["total_damage_s"])
                else:
                    self.mult_damage = 0
                    self.special_stacks = self.special_stacks - self.stats['total_stacks']
            else:
                self.special_stacks = self.special_stacks - self.stats['total_stacks']

    def recapStacks(self):
        if self.stats["total_stacks"] == self.special_stacks:
            content = f"\n\n> ☄️ Ta capacité spéciale est chargée : Charge total : **{self.special_stacks}/{self.stats['total_stacks']}**"
        else:
            content = f"\n\n ☄️ Charge total : **{self.special_stacks}/{self.stats['total_stacks']}**"
        return content

    def recapHealth(self, total_damage_taken):
        content = f"\n\n> Ton adversaire t'a infligé {int(total_damage_taken)} dégâts."
        if self.dead:
            content += f"\n> Tu es mort !"
            self.lastregen = datetime.datetime.timestamp(datetime.datetime.now())
            self.firstregen = True
        else:
            content += f"\n> Il te reste {int(self.stats['total_max_health'] - self.damage_taken)}/{self.stats['total_max_health']} ❤️ !"
        return self.dead, content
    
    def regen(self):
        regen = int(float(self.bot.Variables["regen_percentage"]) * self.stats["total_max_health"])
        regen = int(min(self.damage_taken, regen))
        self.damage_taken -= regen
        return regen