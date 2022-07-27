import lib

print("SpawnMonsters : √")

class Run(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.battleslist = {}
        self.slayerlist = {}

        self.BDD = lib.PostgreSQL.extractBDDs()
        self.battle_monster.start()

    @property
    def channels(self):
        return lib.Run_Self.get_Channels(self, lib.tokens.var_TestProd, lib.PostgreSQL.get_PostgreSQL_channels())

    @lib.tasks.loop(minutes=1)
    async def battle_monster(self):

        for gamemode in self.BDD["GameModes_list"]:

            #Doit on faire spawn un monster ?

            monster_hp_scaling_based_on_active_players = max(1, len(self.slayerlist.keys()))
            #On calcule le behemoth a faire spawn en prenant random dans la liste.
            rarity = lib.random.choices(list(self.BDD["GameModes_list"][gamemode]["spawn_rates"]), weights=list(self.BDD["GameModes_list"][gamemode]["spawn_rates"].values()), cum_weights=None, k=1)[0]
            monster_to_spawn = lib.random.choice([key for key, val in self.BDD["Monsters_list"].items() if val.rarity==rarity])

            await lib.Run_Functions.spawn_battle(self, monster_hp_scaling_based_on_active_players, gamemode, monster_to_spawn)

    @battle_monster.before_loop
    async def before_battle_monster(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Run(bot))