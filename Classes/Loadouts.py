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
        cSpe,
        items
        ):
        self.bot = bot
        self.name = name
        self.cSlayer = cSlayer
        self.items = items
        self.cSpe = cSpe
        self.gearscore = self.get_gear_score()
        self.init_pre_stats() #stats des items

    @classmethod
    async def handler_Build(cls, bot, name, cSlayer, row):
        cSpe = await Spe.handler_Build(bot, row[0], cSlayer)
        list_items = []
        for id in [eval(str(i)) for i in row["loadout"].strip('][').split(',')][1:]:
            if id in cSlayer.inventories["items"]:
                list_items.append(cSlayer.inventories["items"][id])
        cLoadout = Loadout(bot, name, cSlayer, cSpe, list_items)
        return cLoadout

    def init_pre_stats(self):
        pre_stats = {}
        for cObject in self.items:
            pre_stats = lib.add_bonuses(self.bot, pre_stats, cObject.bonuses)
        self.pre_stats = pre_stats
        self.stats = pre_stats

    def trigger_refreshes(self):
        self.refresh_stats()
        self.cSpe.refresh_stats()

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
        pass

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
        cObject.equipped = True
        self.items.append(cObject)
        await self.bot.dB.equip_item(self.cSlayer, cObject)
        self.pre_stats = lib.add_bonuses(self.bot, self.pre_stats, cObject.bonuses)
        self.trigger_refreshes()
        await self.cSlayer.adapt_damage_taken(damage_taken_percentage)

    async def unequip_item(self, cObject):
        damage_taken_percentage = self.cSlayer.damage_taken_percentage
        cObject.equipped = False
        self.items.remove(cObject)
        await self.bot.dB.unequip_item(self.cSlayer, cObject)
        self.pre_stats = lib.remove_bonuses(self.bot, self.pre_stats, cObject.bonuses)
        self.trigger_refreshes()
        await self.cSlayer.adapt_damage_taken(damage_taken_percentage)

    def already_equipped(self, slot):
        items_list = []
        for cObject in self.items:
            if cObject.slot == slot:
                items_list.append(cObject)
        return items_list
    
    async def set_specialization(self, spe_id):
        cSpe = await Spe.get_Spe_Class(self.bot, spe_id, self.cSlayer)
        self.cSpe = cSpe
        await self.correct_slots_after_changing_spe()
        self.trigger_refreshes()