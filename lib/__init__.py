#python3.10 -m pip install -U git+https://github.com/Rapptz/discord.py
#pip3 install nest_asyncio
#pip install asyncpg

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

#CLASSES
from Classes.DamageDone import DamageDone
from Classes.dBManager import dB
from Classes.ActiveList import ActiveList
from Classes.Items import Item
from Classes.MainSlayers import MSlayer, Slayer
from Classes.MainBattles import Battle, Monster
from Classes.Specialization import Spe
from Classes.Queries import qGameModes, qMonsters, qSlayers, qChannels, qBaseBonuses, qRaritiesLootRates, qItems, qElements, qRarities, qGameModesLootSlot, qGameModesSpawnRate, qLootSlot, qSlayersInventoryItems, qSlots, qSpe

#FUNCTIONS
import Functions.Messages.Embed as Embed
import Functions.Tools.Toolbox as Toolbox

#Localisation