#python3.8 -m pip install -U git+https://github.com/Rapptz/discord.py

#librairies
import os
import ssl
import discord
from discord.ext import commands as commands
import discord.ext
from discord.ext import tasks
import pickle
import random
import datetime
from copy import deepcopy
import psycopg2

#folders & files
import gitignore.tokens as tokens

#SQL REQUESTS
import Functions.PostgreSQL.Functions as PostgreSQL

#COGS
import Cogs.Buttons as Buttons
import Cogs.Run as Run

#CLASSES
import Classes.Battles
import Classes.DamageDone
import Classes.Items
import Classes.Monsters
import Classes.Slayers
import Classes.Specialization

#FUNCTIONS
import Functions.Messages.Embed as Embed
import Functions.Messages.Ephemeral as Ephemeral
import Functions.Run.Functions

#DATA
import Data.Global.Global_Variables

#Localisation