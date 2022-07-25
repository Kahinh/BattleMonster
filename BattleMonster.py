import lib

intents = lib.discord.Intents.default()
intents.members = True

class BattleMonster(lib.commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='$',
            intents=intents)
        self.initial_extensions = [
            'Cogs.Run'
        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def on_ready(self):
        await bot.change_presence(activity=lib.discord.Game('Hunting Monsters ...'))
        print('Ready!')

bot = BattleMonster()
bot.run(lib.tokens.BattleMonster)