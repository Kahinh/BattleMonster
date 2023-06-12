
from datetime import datetime
from dataclasses import dataclass
from Classes.Objects import Object, Item, Mythic, Pet
from Classes.Loadouts import Loadout
from Classes.Attributes import Spe
from collections import defaultdict
import random
from Functions.Messages.Embed import create_embed_new_pet

@dataclass
class Slayer:
    id: int
    name: str
    achievements: dict

    def __init__(
        self,
        bot,
        user_id,
        user_name,
        slayer_data
        ):
        self.bot = bot
        self.id = user_id if slayer_data is None else slayer_data["id"]
        self.name= user_name if slayer_data is None else slayer_data["name"]
        self.creation_date = datetime.timestamp(datetime.now()) if slayer_data is None else slayer_data["creation_date"]
        self.dead= False if slayer_data is None else slayer_data["dead"]
        self.xp= 0 if slayer_data is None else slayer_data["xp"]
        self.money= 0 if slayer_data is None else slayer_data["money"]
        self.damage_taken= 0 if slayer_data is None else slayer_data["damage_taken"]
        self.special_stacks= 0 if slayer_data is None else slayer_data["special_stacks"]
        self.faction= 0 if slayer_data is None else int(slayer_data["faction"])
        self.beta_tester= False if slayer_data is None else slayer_data["beta_tester"]
        self.current_loadout = None
        self.inventories = {
            "items" : {},
            "specializations" : [],
            "gatherables" : {},
            "loadouts" : {}
        }
        self.achievements = {}
        self.loadouts = {}

        #regen
        self.lastregen = datetime.timestamp(datetime.now()) - int(bot.Variables["regen_waiting_time_rez"])
        self.firstregen = False

    @classmethod
    async def handler_Build(cls, bot, user_id, user_name):
        slayer_data, slayer_inventory_items, slayer_spe_inventory, slayer_inventory_gatherables, slayer_achievements, slayer_loadouts = await bot.dB.pull_slayer_data(user_id)
        cSlayer = Slayer(bot, user_id, user_name, slayer_data)
        
        def build_achievements():
            for row in slayer_achievements:
                cSlayer.achievements.update({row["achievement"] : row["value"]})

        def build_inventory_specializations():
            if slayer_spe_inventory is None:
                cSlayer.inventories["specializations"] = [1] 
            else:
                cSlayer.inventories["specializations"] = [eval(str(i)) for i in slayer_spe_inventory[0].strip('][').split(',')]

        def build_inventory_gatherables():
            cSlayer.inventories["gatherables"] = defaultdict(int)
            for row in slayer_inventory_gatherables:
                cSlayer.inventories["gatherables"].update({row['gatherable_id']: row["amount"]})
        
        def build_inventory_items():
            for row in slayer_inventory_items:
                cObject = Object.get_Object_Class(bot, row)
                cSlayer.inventories["items"].update({row["id"]: cObject})

        async def build_current_loadout():
            cSlayer.current_loadout = await Loadout.get_Object_Class_from_cSlayer(bot, "Current", cSlayer, 1 if slayer_data is None else slayer_data["specialization"], [cSlayer.inventories["items"][id] for id in cSlayer.inventories["items"] if cSlayer.inventories["items"][id].equipped == True], True)
        
        async def build_loadouts():
            for row in slayer_loadouts:
                cSlayer.loadouts.update({int(row["id"]) : await Loadout.get_Object_Class_from_db(bot, row["name"], cSlayer, [eval(str(i)) for i in row["loadout"].strip('][').split(',')][0], [eval(str(i)) for i in row["loadout"].strip('][').split(',')][1:])})

        #On trigger les builds
        build_achievements()
        build_inventory_gatherables()
        build_inventory_items()
        build_inventory_specializations()
        await build_current_loadout()
        await build_loadouts()

        return cSlayer

    @property
    def gearscore(self):
        return self.current_loadout.gearscore
    @property
    def cSpe(self):
        return self.current_loadout.cSpe
    @property
    def stats(self):
        return self.current_loadout.stats
    @property
    def health(self):
        return self.current_loadout.stats["health"]
    @property
    def current_health(self):
        return self.current_loadout.stats["health"] - self.damage_taken
    @property
    def damage_taken_percentage(self):
        return float(self.damage_taken/self.health)
    
    @property
    def remaining_hit_temporary_stat(self):
        return self.cSpe.remaining_hit_temporary_stat
    
    def trigger_refreshes(self):
        self.current_loadout.trigger_refreshes()

    def item_can_be_equipped(self, cSlot):
        empty_slot, only_one_place_on_slot = self.current_loadout.item_can_be_equipped(cSlot)
        return empty_slot, only_one_place_on_slot

    def slot_nbr_max_items(self, cSlot):
        return self.current_loadout.slot_nbr_max_items(cSlot)

    def slot_items_equipped(self, cSlot):
        return self.current_loadout.slot_items_equipped(cSlot)

    async def set_inventory_specializations(self, spe_id):
        self.inventories["specializations"].append(int(spe_id))
        await self.bot.dB.push_spe_list(self) 

    async def set_specialization(self, spe_id):
        self.special_stacks = 0
        await self.bot.dB.push_special_stacks(self.id, self.special_stacks)
        await self.bot.dB.push_spe(self.id, spe_id)
        await self.current_loadout.set_specialization(spe_id)
    
    async def add_remove_money(self, amount):
        if self.money + amount < 0:
            return False
        self.money += amount
        await self.bot.dB.push_money(self.id, amount)
        return True

    async def add_remove_gatherables(self, gatherable_id, amount):
        if self.inventories["gatherables"].get(gatherable_id, 0) + amount < 0:
            return False
        self.inventories["gatherables"][gatherable_id] += amount
        await self.bot.dB.push_Gather(self.id, gatherable_id, self.inventories["gatherables"][gatherable_id])
        return True
    
    async def adapt_damage_taken(self, damage_taken_percentage):
        self.damage_taken = int(damage_taken_percentage * self.health)
        await self.bot.dB.push_damage_taken(self.id, self.damage_taken)

    def isinInventory(self, id):
        if id in self.inventories["items"]:
            return True
        else:
            return False
        
    def isEquipped(self, id):
        if id in self.inventories["items"]:
            if self.inventories["items"][id].equipped:
                return True
            else:
                return False
        else:
            return True
    
    def activate_temporary_stat(self):
        self.current_loadout.activate_temporary_stat()

    async def equip_item(self, cObject):
        await self.current_loadout.equip_item(cObject)

    async def unequip_item(self, cObject):
        await self.current_loadout.unequip_item(cObject)

    async def addtoInventory(self, cObject):
        self.inventories["items"][cObject.id] = cObject
        await self.bot.dB.add_item(self, cObject)

    async def update_inventory_gatherables(self, gatherable_id, amount):
        self.inventories["gatherables"][gatherable_id] += amount
        await self.bot.dB.push_Gather(self.id, gatherable_id, self.inventories["gatherables"][gatherable_id])
        
    async def getDrop(self, rate=0.01, pets=[]):
        if random.choices((True, False), (rate, 1-rate), k=1)[0]:
            pet_id = random.choice(pets)
            if not self.isinInventory(pet_id):
                rDrop = await self.bot.dB.get_rPet(pet_id)
                cObject = Object.get_Object_Class(self.bot, rDrop)

                #On ajoute au stuff
                await self.addtoInventory(cObject)

                #On poste le message
                embed = create_embed_new_pet(self.bot, self, cObject)
                channel = self.bot.get_channel(self.bot.rChannels["loots"])
                await channel.send(content=f"<@{self.id}>",embed=embed)

    def canSpecial(self):
        if self.special_stacks >= self.stats["stacks"]:
            return True, ""
        else:
            return False, f"\n> ☄️ Tu ne possèdes pas le nombre de charges nécessaires - Charge total : **{self.special_stacks}/{self.stats['stacks']}**"
    
    def isCrit(self, hit):
        isCrit = random.choices(population=[True, False], weights=[float(self.stats[f"crit_chance_{hit}"]), float(1-self.stats[f"crit_chance_{hit}"])], k=1)[0]
        return isCrit

    def dealDamage(self, hit, cOpponent, isCrit, CritMult, ProtectCrit, ArmorMult):
        #Dégâts de base :
        damage = int(self.stats[f"damage_{hit}"])

        #Add CDG :
        if self.cSpe.id == 4 and hit == "s":
            damage += int(cOpponent.extract_lasthits_list(self))

        #Add Chasseur
        armor_reduction = 0
        if self.cSpe.id == 6 and hit == "s":
            if cOpponent.armor == cOpponent.armor_cap:
                damage = (damage + int(self.stats["total_letality_s"])) * (1 + self.stats["total_letality_per"])
            else:
                print(cOpponent.armor, self.reduceArmor(hit, cOpponent.armor), self.bot.Variables["chasseur_armor_reduction_mult"])
                armor_reduction = int((cOpponent.armor - self.reduceArmor(hit, cOpponent.armor)) * self.bot.Variables["chasseur_armor_reduction_mult"])
                armor_reduction = int(min(armor_reduction, cOpponent.armor - cOpponent.armor_cap))
                cOpponent.armor -= armor_reduction

        #On applique les Mult : Crit & Finaux
        damage = int(damage*(1 + CritMult) * (1 + self.stats[f"final_damage_{hit}"]))
        #ArmorMult
        damage = int(max(damage * ArmorMult, 0))
        #ProtectCrit
        damage = int(max(damage - ProtectCrit, 0))
        #A ce stade, si damage = 0, alors le monstre a trop d'armures
        if damage == 0:
            return 0, f"\n> ⚔️ {self.cSpe.ability_name if hit == 's' else hit} : {int(damage)} - L'adversaire possédait trop de défense !"
        #Vie du monstre
        if cOpponent.base_hp is not None:
            damage = int(min(damage, cOpponent.base_hp))
            if damage == 0:
                return 0, f"\n> ⚔️ {self.cSpe.ability_name if hit == 's' else hit} : {int(damage)} - Le {cOpponent.group_name} est déjà mort !"

        content = f"\n> ⚔️ {self.cSpe.ability_name if hit == 's' else hit} : {int(damage)} {'‼️' if isCrit else ''} {'(-' + str(armor_reduction) + '🛡️)' if armor_reduction > 0 else ''} {'[🔥+' + str(self.current_loadout.cSpe.spe_damage) + ']' if self.current_loadout.cSpe.spe_damage > 0 else ''} {'[🪓' + str(self.remaining_hit_temporary_stat -1) + 'restants]' if self.remaining_hit_temporary_stat > 0 else ''}"
        self.cSpe.reduce_remaining_hit_temporary_stat()
        #content = f"\n> ⚔️ {self.cSpe.ability_name if hit == 'S' else hit} : {int(damage)} {'‼️' if isCrit else ''} {'[🔥+' + str(mult_damage) + ']' if mult_damage > 0 else ''} {additionnal_ability if additionnal_ability != '' else ''} {'[🪓' + str(self.berserker_mode -1) + 'restants]' if self.berserker_mode > 0 else ''}"

        return damage, content
    
    def reduceArmor(self, hit, armor):
        #Reduction Fix
        armor = (armor-int(self.stats[f"letality_{hit}"]))
        #Reudction %
        if armor > 0:
            armor = armor*(1-float(self.stats[f"letality_per_{hit}"]))
        return int(armor)

    def getStacks(self, hit):
        if hit == "s":
            stacks_earned = int(max(min(int(self.stats["stacks"]*0.5) - self.special_stacks, self.stats[f"special_charge_{hit}"]),0))
        else:
            stacks_earned = int(min(self.stats["stacks"] - self.special_stacks, self.stats[f"special_charge_{hit}"]))
        self.special_stacks += stacks_earned
        return stacks_earned

    def getDamage(self, damage):
        self.damage_taken += damage
        if self.health == 0:
            self.dead = True

    def isAlive(self):
        if self.dead:
            return False, "> Tu es mort ! Tu ne peux donc pas attaquer pour l'instant 💀"
        else:
            return True, ""

    def getNbrHit(self):
        nbr = int(self.bot.Variables["slayer_base_hit_number"])
        nbr += self.cSpe.nbr_hit()
        return nbr

    def recap_useStacks(self, hit):
        if hit == "s":
            if self.cSpe.id == 7 and self.special_stacks == self.stats['stacks']:
                content = f"\n> ☄️ Charge récupérées, spécial disponible : **{self.special_stacks}/{self.stats['stacks']}**"
            else:
                content = f"\n> ☄️ Charge consommée : {self.stats['stacks']} - Charge total : **{self.special_stacks}/{self.stats['stacks']}**"
            return content
        
    def useStacks(self, hit):
        if hit == "s":
            if not self.cSpe.demon_proc(self.current_loadout.stats):
                self.special_stacks = self.special_stacks - self.stats['stacks']

    def recapStacks(self):
        if self.stats["stacks"] == self.special_stacks:
            content = f"\n\n> ☄️ Ta capacité spéciale est chargée : Charge total : **{self.special_stacks}/{self.stats['stacks']}**"
        else:
            content = f"\n\n ☄️ Charge total : **{self.special_stacks}/{self.stats['stacks']}**"
        return content

    def recapHealth(self, total_damage_taken):
        content = f"\n\n> Ton adversaire t'a infligé {int(total_damage_taken)} dégâts."
        if self.dead:
            content += f"\n> Tu es mort !"
            self.lastregen = datetime.timestamp(datetime.now())
            self.firstregen = True
        else:
            content += f"\n> Il te reste {int(self.current_health)}/{self.health} ❤️ !"
        return self.dead, content
    
    def regen(self):
        regen = int(float(self.bot.Variables["regen_percentage"]) * self.health)
        regen = int(min(self.damage_taken, regen))
        self.damage_taken -= regen
        return regen