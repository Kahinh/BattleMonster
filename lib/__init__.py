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
from Classes.MainSlayers import MSlayer, Slayer
from Classes.Properties import Rarities, Elements
from Classes.Handler_Gatherables import Gather, GatherablesSpawn, Gatherables
from Classes.Opponents import Opponent, Monster, Banner, Mythique1, Mythique2, Mythique3, Mythique4, Mythique5, Mythique6
from Classes.Gamemodes import Gamemode, Hunt, FactionWar, Donjon
from Classes.Attributes import Spe, Faction
from Classes.Objects import Item, Mythic, Pet

#TODO TODELETE
from Classes.Queries import qGameModes, qOpponents, qChannels, qBaseBonuses, qRaritiesLootRates, qItems, qElements, qRarities, qGameModesSpawnRate, qSlots, qSpe, qGatherables, qGatherables_Spawn

#FUNCTIONS
import Functions.Messages.Embed as Embed
import Functions.Tools.Toolbox as Toolbox
from Functions.Tools.DisplayStats import get_display_stats

#Localisation

#DECORATORS
from Decorators import get_time
from Decorators import get_args

#LOGGING
import logging
logging.basicConfig(filename='logs.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s') 