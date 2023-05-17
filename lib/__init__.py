#python3.10 -m pip install -U git+https://github.com/Rapptz/discord.py
#pip3 install nest_asyncio
#pip install asyncpg

#TODO Remove la lib et faire un truc import dans chaque page.

#librairies
import os
import ssl
import discord
from discord.ext import commands as commands
from discord import app_commands
from discord.app_commands import Choice
import discord.ext
from discord.ext import tasks
import pickle
import random
import asyncio
import datetime
from copy import deepcopy

#folders & files
import gitignore.tokens as tokens

#COGS
import Cogs.Main as Main
import Cogs.Commands_Admin as Commands_Admin

#VIEWS
from Views.Inventory import InventoryView
from Views.Loot import LootView
from Views.LootRecap import LootRecapView
from Views.Battle import BattleView
from Views.Slayer import SlayerView
from Views.MultEquip import MultEquipView
from Views.Spe import SpeView
from Views.LootReview import LootReviewView
from Views.CmdEvent import CmdEvent
from Views.Gather import GatherView
from Views.Enhancement_Pets import EnhancementPetsView
from Views.Enhancement_Mythics import EnhancementMythicsView

#CLASSES
from Classes.DamageDone import DamageDone
from Classes.dBManager import dB
from Classes.ActiveList import ActiveList
from Classes.Items import Item
from Classes.MainSlayers import MSlayer, Slayer
from Classes.MainBattles import Battle, Monster
from Classes.Specialization import Spe
from Classes.Rarities import Rarities
from Classes.Elements import Elements
from Classes.Gatherables import Gatherables
from Classes.GatherablesSpawn import GatherablesSpawn
from Classes.Gather import Gather
from Classes.Handler_Attack import Attack, Hit
from Classes.Handler_Loot import Loot
from Classes.Queries import qGameModes, qOpponents, qChannels, qBaseBonuses, qRaritiesLootRates, qItems, qElements, qRarities, qGameModesLootSlot, qGameModesSpawnRate, qSlots, qSpe, qGatherables, qGatherables_Spawn

#FUNCTIONS
import Functions.Messages.Embed as Embed
import Functions.Tools.Toolbox as Toolbox

#Localisation

#DECORATORS
from Decorators import get_time
from Decorators import get_args

#LOGGING
import logging
logging.basicConfig(filename='logs.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s') 