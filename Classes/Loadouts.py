from dataclasses import dataclass
from Classes.Objects import Object, Mythic, Pet, Item, Improvable_Object
from Classes.Attributes import Spe
from collections import Counter


import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import lib

@dataclass
class Loadout:
    name: str
    items: list
    gearscore: int

    def __init__(
        self,
        bot,
        name,
        cSlayer,
        is_current_loadout
        ):
        self.bot = bot
        self.name = name
        self.cSlayer = cSlayer
        self.is_current_loadout = is_current_loadout

        #First init
        self.items = []
        self.cSpe = None

        #Second init
        self.items_stats = {}
        self.buffs_stats = {}

    @staticmethod
    async def get_Object_Class_from_db(bot, name, cSlayer, spe_id, items_list, is_current_loadout=False):
        return await Loadout.handler_Build(bot, name, cSlayer, spe_id, items_list, is_current_loadout, True)

    @staticmethod
    async def get_Object_Class_from_cSlayer(bot, name, cSlayer, spe_id, items_list, is_current_loadout=False):
        return await Loadout.handler_Build(bot, name, cSlayer, spe_id, items_list, is_current_loadout, False)

    @classmethod
    async def handler_Build(cls, bot, name, cSlayer, spe_id, items_list, is_current_loadout, item_to_compile):

        cLoadout = cls(bot, name, cSlayer, is_current_loadout)

        if item_to_compile:
            list_items = []
            for id in items_list:
                if id in cSlayer.inventories["items"]:
                    list_items.append(cSlayer.inventories["items"][id])
        else:
            list_items = items_list
        
        cSpe = await Spe.get_Spe_Class(bot, spe_id, cLoadout)
        cLoadout.cSpe = cSpe
        cLoadout.items = list_items

        cLoadout.init_items_stats() #stats des items

        return cLoadout

    @property
    def gearscore(self):
        return self.get_gear_score()
    
    @property
    def remaining_hit_temporary_stat(self):
        return self.cSpe.remaining_hit_temporary_stat
    
    @property
    def spe_stats(self):
        return self.cSpe.bonuses
    
    @property
    def base_stats(self):
        return self.bot.Base_Player.bonuses
    
    @property
    def temporary_stats(self):
        return self.cSpe.temporary_stats()
    
    @property
    def additional_stats(self):
        return self.cSpe.additional_stats()
    
    def init_items_stats(self):
        items_stats = {}
        for cObject in self.items:
            items_stats = lib.add_bonuses(self.bot, items_stats, cObject.bonuses)
        self.items_stats = items_stats

    def stats(self, bonus, capped=True):
        match bonus:
            case "armor":
                return int((self.items_stats.get(bonus, 0) + self.spe_stats.get(bonus, 0) + self.base_stats.get(bonus, 0) + self.temporary_stats.get(bonus, 0) + self.additional_stats.get(bonus, 0) + self.buffs_stats.get(bonus, 0)) * (1 + self.stats("armor_per")))
            case "health":
                return int((self.items_stats.get(bonus, 0) + self.spe_stats.get(bonus, 0) + self.base_stats.get(bonus, 0) + self.temporary_stats.get(bonus, 0) + self.additional_stats.get(bonus, 0) + self.buffs_stats.get(bonus, 0)) * (1 + self.stats("health_per")))
            case "damage_l":
                return int((self.items_stats.get(bonus, 0) + self.spe_stats.get(bonus, 0) + self.base_stats.get(bonus, 0) + self.temporary_stats.get(bonus, 0) + self.additional_stats.get(bonus, 0) + self.buffs_stats.get(bonus, 0) + self.stats("damage_weapon")) * (1 + self.stats("damage_per_l")))
            case "damage_h":
                return int((self.items_stats.get(bonus, 0) + self.spe_stats.get(bonus, 0) + self.base_stats.get(bonus, 0) + self.temporary_stats.get(bonus, 0) + self.additional_stats.get(bonus, 0) + self.buffs_stats.get(bonus, 0) + self.stats("damage_weapon")) * (1 + self.stats("damage_per_h")))
            case "damage_s":
                return int((self.items_stats.get(bonus, 0) + self.spe_stats.get(bonus, 0) + self.base_stats.get(bonus, 0) + self.temporary_stats.get(bonus, 0) + self.additional_stats.get(bonus, 0) + self.buffs_stats.get(bonus, 0) + self.stats("damage_weapon")) * (1 + self.stats("damage_per_s")))
            case "stacks":
                return int((self.items_stats.get(bonus, 0) + self.spe_stats.get(bonus, 0) + self.base_stats.get(bonus, 0) + self.temporary_stats.get(bonus, 0) + self.additional_stats.get(bonus, 0)) - self.stats("stacks_reduction"))
            case "cooldown":
                return int(max(float(self.bot.Variables["cooldown"]) - self.stats("vivacity"), 10))
            case _:
                if capped:
                    return lib.cap_min_max_bonus(bonus, self.items_stats.get(bonus, 0) + self.spe_stats.get(bonus, 0) + self.base_stats.get(bonus, 0) + self.temporary_stats.get(bonus, 0) + self.additional_stats.get(bonus, 0), self.bot, self.cSpe) + self.buffs_stats.get(bonus, 0)
                else:
                    return self.items_stats.get(bonus, 0) + self.spe_stats.get(bonus, 0) + self.base_stats.get(bonus, 0) + self.temporary_stats.get(bonus, 0) + self.additional_stats.get(bonus, 0) + self.buffs_stats.get(bonus, 0)

    def get_gear_score(self):
        gearscore = 0
        for cObject in self.items:
            gearscore += cObject.gearscore
        return gearscore
    
    async def correct_slots_after_changing_spe(self):
        for _, cSlot in self.bot.Slots.items():
            while len(self.slot_items_equipped(cSlot)) > self.slot_nbr_max_items(cSlot):
                await self.unequip_item(self.slot_items_equipped(cSlot)[0])

    def slot_items_equipped(self, cSlot):
        return [cObject for cObject in self.items if cObject.slot == cSlot.name]
    
    def slot_nbr_max_items(self, cSlot):
        return self.cSpe.slot_nbr_max_items(cSlot)

    def item_can_be_equipped(self, cSlot):
        
        empty_slot = False
        only_one_place_on_slot = False

        if self.slot_items_equipped(cSlot) == []: empty_slot = True
        if len(self.slot_items_equipped(cSlot)) < self.slot_nbr_max_items(cSlot): empty_slot = True
        if self.slot_nbr_max_items(cSlot) == 1: only_one_place_on_slot = True

        return empty_slot, only_one_place_on_slot


    async def equip_item(self, cObject):
        damage_taken_percentage = self.cSlayer.damage_taken_percentage
        await self.bot.dB.equip_item(self.cSlayer, cObject)
        cObject.equipped = True
        self.items.append(cObject)
        self.items_stats = lib.add_bonuses(self.bot, self.items_stats, cObject.bonuses)
        await self.cSlayer.adapt_damage_taken(damage_taken_percentage)

    async def unequip_item(self, cObject):
        damage_taken_percentage = self.cSlayer.damage_taken_percentage
        await self.bot.dB.unequip_item(self.cSlayer, cObject)
        cObject.equipped = False
        self.items.remove(cObject)
        self.items_stats = lib.remove_bonuses(self.bot, self.items_stats, cObject.bonuses)
        await self.cSlayer.adapt_damage_taken(damage_taken_percentage)

    async def remove_item_for_enhancement(self, cObject):
        if self.is_current_loadout:
            damage_taken_percentage = self.cSlayer.damage_taken_percentage
        self.items_stats = lib.remove_bonuses(self.bot, self.items_stats, cObject.bonuses)
        if self.is_current_loadout:
            await self.cSlayer.adapt_damage_taken(damage_taken_percentage)

    async def add_item_for_enhancement(self, cObject):
        if self.is_current_loadout:
            damage_taken_percentage = self.cSlayer.damage_taken_percentage
        self.items_stats = lib.add_bonuses(self.bot, self.items_stats, cObject.bonuses)
        if self.is_current_loadout:
            await self.cSlayer.adapt_damage_taken(damage_taken_percentage)

    def already_equipped(self, slot):
        items_list = []
        for cObject in self.items:
            if cObject.slot == slot:
                items_list.append(cObject)
        return items_list
    
    async def set_specialization(self, spe_id):
        cSpe = await Spe.get_Spe_Class(self.bot, spe_id, self)
        self.cSpe = cSpe
        await self.correct_slots_after_changing_spe()

    def get_loadout_list(self):
        loadout_list = [self.cSpe.id]
        loadout_list.extend([cObject.id for cObject in self.items])
        return loadout_list