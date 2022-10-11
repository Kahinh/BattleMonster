import lib

class Main(lib.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cd_regen = 1
        self.cd_rez = 1
        self.battle_monster.start()

    @lib.tasks.loop(minutes=1)
    async def battle_monster(self):
        #Gamemodes
        if self.cd_regen >= self.bot.rBaseBonuses["cd_regen"]:
            async with self.bot.db_pool.acquire() as conn:
                await conn.execute(f'UPDATE "Slayers" SET damage_taken = GREATEST(damage_taken - {self.bot.rBaseBonuses["regen"]}, 0) WHERE dead = false AND damage_taken > 0')
            self.bot.ActiveList.regen_health_all()
            channel = self.bot.get_channel(self.bot.rChannels["logs"])
            await channel.send("Régen effectuée")
            self.cd_regen = 1
        if self.cd_rez >= self.bot.rBaseBonuses["cd_rez"]:
            async with self.bot.db_pool.acquire() as conn:
                await conn.execute(f'UPDATE "Slayers" SET damage_taken = GREATEST(damage_taken - {self.bot.rBaseBonuses["regen"]}, 0), dead = false WHERE dead = true AND damage_taken > 0')            
            self.bot.ActiveList.rez_all()
            channel = self.bot.get_channel(self.bot.rChannels["logs"])
            await channel.send("Résurrection effectuée")            
            self.cd_rez = 1

        for gamemode in self.bot.rGamemodes:
            if gamemode["autospawn"]:
                #random si ça doit spawn
                if lib.random.choices(population=[True, False], weights=[float(gamemode["invoke_rate"]), 1-float(gamemode["invoke_rate"])], k=1)[0]:
                #if True:
                    #On crée la class et on construit
                    Battle = lib.Battle(self.bot, gamemode)
                    await Battle.constructGamemode()
        
        self.cd_regen += 1
        self.cd_rez += 1

    @battle_monster.before_loop
    async def before_battle_monster(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Main(bot))
    print("BattleMonster : √")