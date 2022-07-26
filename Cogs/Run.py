import lib

print("SpawnMonsters : √")

#Global Data
global_battleslist = {}
global_slayerlist = {}

class Buttons_Battle(lib.discord.ui.View):
    def __init__(self):
        super().__init__()
        self.guild = None
        self.message = None

    @lib.discord.ui.button(label='Attaque Légère', style=lib.discord.ButtonStyle.green)
    async def light(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        isDead = await Run.attack(interaction, "L")
        if isDead:
            for item in self.children:
                item.disabled = True
            self.stop()

    @lib.discord.ui.button(label='Attaque Lourde', style=lib.discord.ButtonStyle.blurple)
    async def heavy(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        isDead = await Run.attack(interaction, "H")
        if isDead:
            for item in self.children:
                item.disabled = True
            self.stop()

    #@lib.discord.ui.button(label='Spécial', style=lib.discord.ButtonStyle.red)
    #async def special(self, interaction: lib.discord.Interaction, button: lib.discord.ui.Button):
        ##Check Guild ID & User ID
        #global global_slayerlist
        #global global_battleslist
        #global_slayerlist = await lib.Functions.Global.Tools.checkifguildslayerexist(global_slayerlist, interaction.guild_id, interaction.user)

    #    await interaction.response.send_message('Special', ephemeral=True)

class Run(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.battle_monster.start()

    @lib.tasks.loop(minutes=1)
    async def battle_monster(self):
        global global_battleslist
        global global_slayerlist

        for guild_id in lib.Data.Global.Global_Variables.battle_channels:
            if guild_id not in global_slayerlist: global_slayerlist[guild_id] = {}
            if guild_id not in global_battleslist: global_battleslist[guild_id] = {}
            for gamemode in lib.PostgreSQL.GameModes_list:

                #Doit on faire spawn un monster ?

                monster_hp_scaling_based_on_active_players = max(1, len(global_slayerlist[guild_id].keys()))
                channel = self.bot.get_channel(lib.Data.Global.Global_Variables.battle_channels[guild_id][lib.tokens.var_TestProd][gamemode])

                #On calcule le behemoth a faire spawn en prenant random dans la liste.
                rarity = lib.random.choices(list(lib.PostgreSQL.GameModes_list[gamemode]["spawn_rates"]), weights=list(lib.PostgreSQL.GameModes_list[gamemode]["spawn_rates"].values()), cum_weights=None, k=1)[0]
                monster_to_spawn = lib.random.choice([key for key, val in lib.PostgreSQL.Monsters_list.items() if val.rarity==rarity])

                await self.spawn_battle(guild_id, channel, monster_hp_scaling_based_on_active_players, lib.PostgreSQL.GameModes_list[gamemode]["scaling"], monster_to_spawn, lib.PostgreSQL.Monsters_list, lib.PostgreSQL.GameModes_list[gamemode]["roll_dices"], lib.PostgreSQL.LootsSlot_list[lib.PostgreSQL.GameModes_list[gamemode]["loots_slot"]])
                
    async def spawn_battle(self, guild_id, channel, monster_hp_scaling_based_on_active_players, monster_difficulty_scaling, monster_to_spawn, Monsters_list, roll_dices, loots_slots):
        global global_slayerlist
        global global_battleslist
        #On calcule l'embed
        monster_class = lib.deepcopy(Monsters_list[monster_to_spawn])
        monster_class.updateStats(monster_hp_scaling_based_on_active_players, monster_difficulty_scaling, roll_dices)
        embed = lib.Functions.Combat.Embed.create_embed_spawn(monster_class)

        view = Buttons_Battle()
        message = await channel.send(embed=embed, view=view)
        #On crée l'entrée du combat dans la table
        global_battleslist[guild_id][message.id] = lib.Classes.Battles.Battles(monster_class=monster_class, loots_slots= loots_slots, slayers_data={}, last_hits=[])

    async def attack(interaction, hit):
        #Check Guild ID & User ID
        global global_slayerlist
        global global_battleslist

        canAttack = False
        isDead = False

        global_slayerlist = await lib.Functions.Global.Tools.checkifguildslayerexist(global_slayerlist, interaction.guild_id, interaction.user)

        #On calcule les dégâts
        Damage, Stacks_Earned = global_slayerlist[interaction.guild.id][interaction.user.id].CalculateDamage(hit, global_battleslist[interaction.guild.id][interaction.message.id], interaction.user.id)

        #On documente la Class DamageDone
        if interaction.user.id not in global_battleslist[interaction.guild.id][interaction.message.id].slayers_data:
            global_battleslist[interaction.guild.id][interaction.message.id].slayers_data[interaction.user.id] = lib.Classes.DamageDone.DamageDone(eligible=True if Damage > 0 else False, total_damage=Damage if Damage > 0 else 0, timestamp_next_hit=lib.datetime.datetime.timestamp(lib.datetime.datetime.now()) + global_slayerlist[interaction.guild.id][interaction.user.id].calculateStats()['total_cooldown'])
            canAttack = True
        else:
            if global_battleslist[interaction.guild.id][interaction.message.id].slayers_data[interaction.user.id].timestamp_next_hit < lib.datetime.datetime.timestamp(lib.datetime.datetime.now()):
                canAttack = True
                global_battleslist[interaction.guild.id][interaction.message.id].slayers_data[interaction.user.id].updateClass(Damage = Damage, Cooldown = global_slayerlist[interaction.guild.id][interaction.user.id].calculateStats()['total_cooldown'])

        if Damage > 0 and canAttack:
            #On met à jour les PVs du monstre
            global_battleslist[interaction.guild.id][interaction.message.id].GetDamage(damage=Damage, hit=hit, slayer_class=global_slayerlist[interaction.guild.id][interaction.user.id])
            embed = lib.Functions.Combat.Embed.create_embed_spawn(global_battleslist[interaction.guild.id][interaction.message.id].monster_class)
            #On met à jour l'embed
            if global_battleslist[interaction.guild.id][interaction.message.id].monster_class.base_hp == 0:
                await interaction.message.edit(embed=embed, view=None)
                await Run.calculate_loot(Run, guild_id=interaction.guild.id, message_id=interaction.message.id)
                isDead = True
            else:
                await interaction.message.edit(embed=embed)

        ephemeral_message = lib.Functions.Combat.Functions.get_ephemeral_message(Damage, hit, Stacks_Earned, global_slayerlist[interaction.guild.id][interaction.user.id], global_battleslist[interaction.guild.id][interaction.message.id], interaction.user.id, canAttack)
        await interaction.response.send_message(f'{ephemeral_message}', ephemeral=True)
        return isDead

    async def calculate_loot(self, guild_id, message_id):
        pass

    @battle_monster.before_loop
    async def before_battle_monster(self):
        await self.bot.wait_until_ready()
            
async def setup(bot):
    await bot.add_cog(Run(bot))