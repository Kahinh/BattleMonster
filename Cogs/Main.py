import lib

class Main(lib.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.battle_monster.start()
        self.loop_remove = 1

    @lib.tasks.loop(minutes=1)
    async def battle_monster(self):
        #Gamemodes
        if self.bot.power:
            for gamemode in self.bot.rGamemodes:
                if gamemode["autospawn"]:
                    #random si ça doit spawn
                    if lib.random.choices(population=[True, False], weights=[float(gamemode["invoke_rate"]), 1-float(gamemode["invoke_rate"])], k=1)[0]:
                    #if True:
                        #On crée la class et on construit
                        Battle = lib.Battle(self.bot, gamemode)
                        await Battle.constructGamemode()
            
            if self.loop_remove >= 60:
                await self.bot.ActiveList.remove_inactive()
                self.loop_remove = 1
            
            self.loop_remove += 1

    @battle_monster.before_loop
    async def before_battle_monster(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Main(bot))
    print("BattleMonster : √")