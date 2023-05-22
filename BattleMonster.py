import lib
import asyncio
import asyncpg
import discord
from gitignore.postgresql import user, password, dbname, host, port
from gitignore.tokens import token

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

        super().__init__(
            command_prefix='$',
            intents=intents)
        self.initial_extensions = [
            'Cogs.Main',
            'Cogs.Commands_Admin',
            'Cogs.Sync',
            'Cogs.Commands_Slayer',
            'Cogs.Context_Menus',
            'Cogs.Commands_Enhancement'
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
                self.rGamemodes = await conn.fetch(lib.qGameModes.SELECT_ALL)    
                #TODO rBaseBonuses -> Class
                self.rBaseBonuses = await conn.fetchrow(lib.qBaseBonuses.SELECT_ALL)   
                rChannels = await conn.fetch(lib.qChannels.SELECT_ALL, lib.tokens.TestProd)  
                rElements = await conn.fetch(lib.qElements.SELECT_ALL)
                rRarities = await conn.fetch(lib.qRarities.SELECT_ALL)
                #TODO rSlots -> Class
                rSlots = await conn.fetch(lib.qSlots.SELECT_ALL)
                self.rSpe = await conn.fetch(lib.qSpe.SELECT_ALL)
                rGatherables = await conn.fetch(lib.qGatherables.SELECT_ALL)
                rGatherablesSpawn = await conn.fetch(lib.qGatherables_Spawn.SELECT_ALL)
                rPetFood = await conn.fetch("SELECT * FROM pet_food")
                rVariables = await conn.fetch("SELECT * FROM variables")
                rFactions = await conn.fetch("SELECT * FROM factions")

        self.rSlots = lib.Toolbox.transformSlots(rSlots) 
        self.rChannels = lib.Toolbox.transformChannels(rChannels)

        #Rarities
        for row in rRarities: self.Rarities.update({row["name"]: lib.Rarities(row)})
        #Elements
        for row in rElements: self.Elements.update({row["name"]: lib.Elements(row)})
        #Gatherables
        for row in rGatherables: self.Gatherables.update({row["id"]: lib.Gatherables(row, self.Rarities[row["rarity"]].gatherables_spawn)})
        #GatherablesSpawn
        for row in rGatherablesSpawn: self.GatherablesSpawn.update({row["id"]: lib.GatherablesSpawn(row, self.Gatherables)})
        #PetGood
        for row in rPetFood: self.PetFood.update({row["pet_id"]: self.Gatherables[row["food_id"]]})
        #Variables
        for row in rVariables: self.Variables.update({row["name"]: row["value"]})
        #Factions
        for row in rFactions: self.Factions.update({row["id"]: lib.Faction(row)})

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