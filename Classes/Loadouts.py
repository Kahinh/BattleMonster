from dataclasses import dataclass
from Classes.Objects import Object, Mythic, Pet, Item, Improvable_Object
from Classes.Attributes import Spe
from copy import deepcopy

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
        self.gearscore = 0
        self.pre_stats = {}
        self.stats = {}

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

        cLoadout.gearscore = cLoadout.get_gear_score()
        cLoadout.init_pre_stats() #stats des items

        cLoadout.trigger_refreshes()

        return cLoadout

    def init_pre_stats(self):
        pre_stats = {}
        for cObject in self.items:
            pre_stats = lib.add_bonuses(self.bot, pre_stats, cObject.bonuses)
        self.pre_stats = pre_stats
        self.stats = pre_stats

    def trigger_refreshes(self):
        self.refresh_stats()
        self.cSpe.update_spe_damage()
        self.gearscore = self.get_gear_score()

    def update_stats(self, list_bonus_value):
        for couple in list_bonus_value:
            self.stats[couple[0]] += couple[1]

    def refresh_stats(self):
        
        stats = deepcopy(self.pre_stats)
        stats = lib.add_bonuses(self.bot, stats, self.cSpe.bonuses)
        stats = lib.add_bonuses(self.bot, stats, self.bot.Base_Player.bonuses)

        #temporary stats
        if self.cSpe.remaining_hit_temporary_stat > 0:
            for couple_stat in self.cSpe.temporary_stats():
                stats[couple_stat[0]] += couple_stat[1]
        
        stats = self.cSpe.retreat_stats(stats)
        stats = lib.cap_min_max_stats(self.bot, stats, self.cSpe)

        #On agrège
        stats.update({'armor': int(stats['armor'] * (1 + stats['armor_per']))})
        stats.pop('armor_per')
        stats.update({'health': int(stats['health'] * (1 + stats['health_per']))})
        stats.pop('health_per')
        stats.update({'damage_l': int(stats['damage_l'] * (1 + stats['damage_per_l']))})
        stats.pop('damage_per_l')
        stats.update({'damage_h': int(stats['damage_h'] * (1 + stats['damage_per_h']))})
        stats.pop('damage_per_h')
        stats.update({'damage_s': int(stats['damage_s'] * (1 + stats['damage_per_s']))})
        stats.pop('damage_per_s')
        stats.update({'stacks': int(stats['stacks'] - stats['stacks_reduction'])})
        stats.pop('stacks_reduction')
        stats.update({'cooldown': int(float(self.bot.Variables["cooldown"]) - stats['vivacity'])})
        self.stats = stats

    def activate_temporary_stat(self):
        self.cSpe.activate_temporary_stat()
        self.refresh_stats()

    def deactivate_temporary_stat(self):
        self.refresh_stats()

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
        self.pre_stats = lib.add_bonuses(self.bot, self.pre_stats, cObject.bonuses)
        self.trigger_refreshes()
        await self.cSlayer.adapt_damage_taken(damage_taken_percentage)

    async def unequip_item(self, cObject):
        damage_taken_percentage = self.cSlayer.damage_taken_percentage
        await self.bot.dB.unequip_item(self.cSlayer, cObject)
        cObject.equipped = False
        self.items.remove(cObject)
        self.pre_stats = lib.remove_bonuses(self.bot, self.pre_stats, cObject.bonuses)
        self.trigger_refreshes()
        await self.cSlayer.adapt_damage_taken(damage_taken_percentage)

    async def remove_item_for_enhancement(self, cObject):
        if self.is_current_loadout:
            damage_taken_percentage = self.cSlayer.damage_taken_percentage
        self.pre_stats = lib.remove_bonuses(self.bot, self.pre_stats, cObject.bonuses)
        if self.is_current_loadout:
            await self.cSlayer.adapt_damage_taken(damage_taken_percentage)

    async def add_item_for_enhancement(self, cObject):
        if self.is_current_loadout:
            damage_taken_percentage = self.cSlayer.damage_taken_percentage
        self.pre_stats = lib.add_bonuses(self.bot, self.pre_stats, cObject.bonuses)
        self.trigger_refreshes()
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
        self.trigger_refreshes()

    def get_loadout_list(self):
        loadout_list = [self.cSpe.id]
        loadout_list.extend([cObject.id for cObject in self.items])
        return loadout_list