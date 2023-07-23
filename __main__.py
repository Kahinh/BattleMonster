import lib
import asyncio
import asyncpg
import discord
from gitignore.postgresql import user, password, dbname, host, port
from gitignore.tokens import token

import datetime
from zoneinfo import ZoneInfo

import logging
logging.basicConfig(level=logging.INFO)

intents = lib.discord.Intents.default()
intents.members = True
intents.message_content = True

class BattleMonster(lib.commands.Bot):
    def __init__(self):

        self.Gatherables = {}
        self.GatherablesSpawn = {}
        self.Rarities = {}
        self.Elements = {}
        self.PetFood = {}
        self.Variables = {}
        self.Factions = {}
        self.Specializations = {}
        self.Slots = {}
        self.Statistics = {}
        self.Gamemodes = {}
        self.Gamemodes_spawn_time = {}
        self.Base_Player = None

        super().__init__(
            command_prefix='$',
            intents=intents)
        self.initial_extensions = [
            'Cogs.Main',
            'Cogs.Commands_Admin',
            'Cogs.Sync',
            'Cogs.Commands_Slayer',
            'Cogs.Context_Menus',
            'Cogs.Commands_Enhancement',
            'Cogs.Loop_time'
        ]

    async def setup_hook(self):
        await self.update_bot()
        self.ActiveList = lib.ActiveList(self)
        self.dB = lib.dB(self)
        for ext in self.initial_extensions:
            await self.load_extension(ext)
    
    async def update_bot(self):
        #TODO Mettre tout ça dans le dBManager
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                #TODO Faire sauter le self et corriger partout où nécessaire
                self.rGamemodes = await conn.fetch("SELECT * FROM gamemodes")
                rGamemodes_spawn_time = await conn.fetch("SELECT * FROM gamemodes_spawn_time")    
                rBaseBonuses = await conn.fetchrow("SELECT * FROM base_bonuses_slayers")   
                rChannels = await conn.fetch(lib.qChannels.SELECT_ALL, lib.tokens.TestProd)  
                rElements = await conn.fetch("SELECT * FROM elements")
                rRarities = await conn.fetch("SELECT * FROM rarities")
                rSlots = await conn.fetch("SELECT * FROM slots")
                rSpe = await conn.fetch("SELECT * FROM specializations")
                rGatherables = await conn.fetch("SELECT * FROM gatherables")
                rGatherablesSpawn = await conn.fetch("SELECT * FROM gatherables_spawn")
                rPetFood = await conn.fetch("SELECT * FROM pet_food")
                rVariables = await conn.fetch("SELECT * FROM variables")
                rFactions = await conn.fetch("SELECT * FROM factions")
                rStatistics = await conn.fetch("SELECT * FROM statistics")

        self.rChannels = lib.Toolbox.transformChannels(rChannels)

        #Rarities
        for row in rRarities: self.Rarities.update({row["name"]: lib.Rarity(row)})
        #Elements
        for row in rElements: self.Elements.update({row["name"]: lib.Element(row)})
        #Gatherables
        for row in rGatherables: self.Gatherables.update({row["id"]: lib.Gatherables(row, self.Rarities[row["rarity"]].gatherables_spawn)})
        #GatherablesSpawn
        for row in rGatherablesSpawn: self.GatherablesSpawn.update({row["id"]: lib.GatherablesSpawn(row, self.Gatherables)})
        #PetGood
        for row in rPetFood: self.PetFood.update({row["pet_id"]: self.Gatherables[row["food_id"]]})
        #Variables
        for row in rVariables: self.Variables.update({row["name"]: row["value"]})
        #Factions
        for row in rFactions: self.Factions.update({int(row["id"]): lib.Faction(row)})
        #Statistics
        for row in rStatistics: self.Statistics.update({row["name"] : lib.Statistic(row)})
        #Spe
        for row in rSpe: self.Specializations.update({int(row["id"]): lib.Spe.get_Spe_Class_row(self, row)})
        #Slots
        for row in rSlots: self.Slots.update({row["slot"] : lib.Slot(row)})
        #Base Bonuses
        self.Base_Player = lib.Base_Slayer(self, rBaseBonuses)
        #Gamemodes
        for row in self.rGamemodes: self.Gamemodes.update({row["name"]: row})
        #Gamemodes_spawn_time
        for row in rGamemodes_spawn_time: self.Gamemodes_spawn_time.update({datetime.time(hour=row["hour"], minute=row["min"], tzinfo=ZoneInfo('Europe/Paris')): row["gamemode"]})

    async def on_ready(self):
        print(">>>>>>>>>> BOT LIVE <<<<<<<<<<")

async def main():
    async with asyncpg.create_pool(user=user, password=password,
            database=dbname, host=host,
            port=port) as db_pool:
        client = BattleMonster()
        client.db_pool = db_pool
        client.power = True
        await client.start(token)

asyncio.run(main())