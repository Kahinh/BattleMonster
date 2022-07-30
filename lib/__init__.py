#python3.8 -m pip install -U git+https://github.com/Rapptz/discord.py
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
import datetime
from copy import deepcopy
import psycopg2

#folders & files
import gitignore.tokens as tokens

#COGS
import Cogs.Buttons as Buttons
import Cogs.Main as Main
import Cogs.Commands_Admin as Commands_Admin

#CLASSES
from Classes.DamageDone import DamageDone
from Classes.Items import Item
from Classes.Monsters import Monster
from Classes.MainSlayers import MSlayer, Slayer
from Classes.Specialization import Specialization
from Classes.Queries import qGameModes, qMonsters, qSlayers, qChannels, qBaseBonuses, qRaritiesLootRates, qItems, qElements, qRarities

#FUNCTIONS
import Functions.Messages.Embed as Embed
import Functions.Messages.Ephemeral as Ephemeral
import Functions.Cogs_Functions.Battle_Functions as Battle_Functions
import Functions.Tools.Pickles as Pickles
import Functions.Tools.Toolbox as Toolbox

#Localisation