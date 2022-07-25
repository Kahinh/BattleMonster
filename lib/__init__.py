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

#CLASSES
import Classes.Battles
import Classes.DamageDone
import Classes.Items
import Classes.Monsters
import Classes.Slayers
import Classes.Specialization

#FUNCTIONS
import Functions.Global.Tools
import Functions.Combat.Embed
import Functions.Combat.Functions

#DATA
import Data.Global.Global_Variables
import Data.Global.Rate
import Data.Combat.Combat_Variables
import Data.Items.Loots

#Localisation