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
        self.slayers_list = {}
        for ext in self.initial_extensions:
            await self.load_extension(ext)

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