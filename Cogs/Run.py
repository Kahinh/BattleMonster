import lib

print("SpawnMonsters : √")

class Run(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.battleslist = {}
        self.slayerlist = {}
        self.PostgreSQL = {
            #"Bases_Bonuses_Slayers" : lib.PostgreSQL.Bases_Bonuses_Slayers
        }
        self.battle_monster.start()

    @lib.tasks.loop(minutes=1)
    async def battle_monster(self):

        for guild_id in lib.Data.Global.Global_Variables.battle_channels:
            if guild_id not in self.slayerlist: self.slayerlist[guild_id] = {}
            if guild_id not in self.battleslist: self.battleslist[guild_id] = {}
            for gamemode in lib.PostgreSQL.GameModes_list:

                #Doit on faire spawn un monster ?

                monster_hp_scaling_based_on_active_players = max(1, len(self.slayerlist[guild_id].keys()))
                channel = self.bot.get_channel(lib.Data.Global.Global_Variables.battle_channels[guild_id][lib.tokens.var_TestProd][gamemode])

                #On calcule le behemoth a faire spawn en prenant random dans la liste.
                rarity = lib.random.choices(list(lib.PostgreSQL.GameModes_list[gamemode]["spawn_rates"]), weights=list(lib.PostgreSQL.GameModes_list[gamemode]["spawn_rates"].values()), cum_weights=None, k=1)[0]
                monster_to_spawn = lib.random.choice([key for key, val in lib.PostgreSQL.Monsters_list.items() if val.rarity==rarity])

                await lib.Functions.Run.Functions.spawn_battle(self, guild_id, channel, monster_hp_scaling_based_on_active_players, gamemode, monster_to_spawn)

    @battle_monster.before_loop
    async def before_battle_monster(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Run(bot))