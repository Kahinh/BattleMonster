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
        super().__init__(
            command_prefix='$',
            intents=intents)
        self.initial_extensions = [
            'Cogs.Main',
            'Cogs.Commands_Admin',
            'Cogs.Sync',
            'Cogs.Commands_Slayer',
            'Cogs.Context_Menus'
        ]

    async def setup_hook(self):
        await self.update_bot()
        self.ActiveList = lib.ActiveList(self)
        self.dB = lib.dB(self)
        for ext in self.initial_extensions:
            await self.load_extension(ext)
    
    async def update_bot(self):
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                self.rGamemodes = await conn.fetch(lib.qGameModes.SELECT_ALL)    
                rGameModesLootSlot = await conn.fetch(lib.qGameModesLootSlot.SELECT_ALL) 
                rGameModesSpawnRate = await conn.fetch(lib.qGameModesSpawnRate.SELECT_ALL)
                self.rBaseBonuses = await conn.fetchrow(lib.qBaseBonuses.SELECT_ALL)   
                rChannels = await conn.fetch(lib.qChannels.SELECT_ALL, lib.tokens.TestProd)  
                rElements = await conn.fetch(lib.qElements.SELECT_ALL)
                rRarities = await conn.fetch(lib.qRarities.SELECT_ALL)
                rSlots = await conn.fetch(lib.qSlots.SELECT_ALL)
                self.rSpe = await conn.fetch(lib.qSpe.SELECT_ALL)

        self.rGameModesLootSlot = lib.Toolbox.transformGamemodesLootSlot(rGameModesLootSlot)
        self.rGameModesSpawnRate = lib.Toolbox.transformGamemodesSpawnRate(rGameModesSpawnRate)
        self.rSlots = lib.Toolbox.transformSlots(rSlots) 
        self.rElements = lib.Toolbox.transformRaritiesANDElements(rElements) 
        self.rRarities = lib.Toolbox.transformRaritiesANDElements(rRarities)
        self.rChannels = lib.Toolbox.transformChannels(rChannels)
        

    async def on_ready(self):
        print('Bot is Ready!')

async def main():
    async with asyncpg.create_pool(user=user, password=password,
            database=dbname, host=host,
            port=port) as db_pool:
        client = BattleMonster()
        client.db_pool = db_pool
        client.power = True
        await client.start(token)

asyncio.run(main())