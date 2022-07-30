import lib

class Main(lib.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.battle_monster.start()

    @lib.tasks.loop(minutes=1)
    async def battle_monster(self):

        #Gamemodes
        for Gamemode in self.bot.rGamemodes:
            if Gamemode["autospawn"]:
                await lib.Battle_Functions.spawn_handler(self, Gamemode)

    @battle_monster.before_loop
    async def before_battle_monster(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Main(bot))
    print("BattleMonster : √")