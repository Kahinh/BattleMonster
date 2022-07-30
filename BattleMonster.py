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
            'Cogs.Sync'
        ]

    async def setup_hook(self):
        await self.update_bot()
        for ext in self.initial_extensions:
            await self.load_extension(ext)
    
    async def update_bot(self):
        async with self.db_pool.acquire() as conn:
            self.rGamemodes = await conn.fetch(lib.qGameModes.SELECT_ALL)     
            self.rBaseBonuses = await conn.fetch(lib.qBaseBonuses.SELECT_ALL)   
            rChannels = await conn.fetch(lib.qChannels.SELECT_ALL, lib.tokens.TestProd)  
            rElements = await conn.fetch(lib.qElements.SELECT_ALL)
            rRarities = await conn.fetch(lib.qRarities.SELECT_ALL)

        self.rElements = await lib.Toolbox.transformRecords(rElements)  
        self.rRarities = await lib.Toolbox.transformRecords(rRarities)
        self.rChannels = await lib.Toolbox.transformChannels(rChannels)

    async def on_ready(self):
        print('Bot is Ready!')

async def main():
    async with asyncpg.create_pool(user=user, password=password,
            database=dbname, host=host,
            port=port) as db_pool:
        client = BattleMonster()
        client.db_pool = db_pool
        await client.start(token)

asyncio.run(main())