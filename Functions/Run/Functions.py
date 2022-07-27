import lib

async def checkifguildslayerexist(self, guild_id, slayer):
    if guild_id not in self.slayerlist:
        self.slayerlist[guild_id] = {}
    if slayer.id not in self.slayerlist[guild_id]:
        self.slayerlist[guild_id][slayer.id] = lib.Classes.Slayers.Slayers(name=slayer.name)

async def spawn_battle(self, guild_id, channel, monster_hp_scaling_based_on_active_players, gamemode, monster_to_spawn):
    #On calcule l'embed
    monster_class = lib.deepcopy(lib.PostgreSQL.Monsters_list[monster_to_spawn])
    monster_class.updateStats(monster_hp_scaling_based_on_active_players, lib.PostgreSQL.GameModes_list[gamemode]["scaling"], lib.PostgreSQL.GameModes_list[gamemode]["roll_dices"])

    message = await channel.send(embed=lib.Embed.create_embed_spawn(monster_class), view=lib.Buttons.Buttons_Battle(self))

    #On crée l'entrée du combat dans la table
    self.battleslist[guild_id][message.id] = lib.Classes.Battles.Battles(monster_class=monster_class, loots_slots= lib.PostgreSQL.LootsSlot_list[lib.PostgreSQL.GameModes_list[gamemode]["loots_slot"]], slayers_data={}, last_hits=[])

async def attack(self, interaction, hit):
    #Check Guild ID & User ID
    canAttack = False
    isDead = False

    await checkifguildslayerexist(self, interaction.guild_id, interaction.user)

    #On calcule les dégâts
    Damage, Stacks_Earned = self.slayerlist[interaction.guild.id][interaction.user.id].CalculateDamage(hit, self.battleslist[interaction.guild.id][interaction.message.id], interaction.user.id)

    #On documente la Class DamageDone
    if interaction.user.id not in self.battleslist[interaction.guild.id][interaction.message.id].slayers_data:
        self.battleslist[interaction.guild.id][interaction.message.id].slayers_data[interaction.user.id] = lib.Classes.DamageDone.DamageDone(eligible=True if Damage > 0 else False, total_damage=Damage if Damage > 0 else 0, timestamp_next_hit=lib.datetime.datetime.timestamp(lib.datetime.datetime.now()) + self.slayerlist[interaction.guild.id][interaction.user.id].calculateStats()['total_cooldown'])
        canAttack = True
    else:
        if self.battleslist[interaction.guild.id][interaction.message.id].slayers_data[interaction.user.id].timestamp_next_hit < lib.datetime.datetime.timestamp(lib.datetime.datetime.now()):
            canAttack = True
            self.battleslist[interaction.guild.id][interaction.message.id].slayers_data[interaction.user.id].updateClass(Damage = Damage, Cooldown = self.slayerlist[interaction.guild.id][interaction.user.id].calculateStats()['total_cooldown'])

    if Damage > 0 and canAttack:
        #On met à jour les PVs du monstre
        self.battleslist[interaction.guild.id][interaction.message.id].GetDamage(damage=Damage, hit=hit, slayer_class=self.slayerlist[interaction.guild.id][interaction.user.id])
        #On met à jour l'embed
        if self.battleslist[interaction.guild.id][interaction.message.id].monster_class.base_hp == 0:
            await interaction.message.edit(embed=lib.Embed.create_embed_spawn(self.battleslist[interaction.guild.id][interaction.message.id].monster_class), view=None)
            await calculate_loot(self, guild_id=interaction.guild.id, message_id=interaction.message.id)
            isDead = True
        else:
            await interaction.message.edit(embed=lib.Embed.create_embed_spawn(self.battleslist[interaction.guild.id][interaction.message.id].monster_class))

    ephemeral_message = lib.Ephemeral.get_ephemeral_message(Damage, hit, Stacks_Earned, self.slayerlist[interaction.guild.id][interaction.user.id], self.battleslist[interaction.guild.id][interaction.message.id], interaction.user.id, canAttack)
    await interaction.response.send_message(f'{ephemeral_message}', ephemeral=True)
    return isDead

async def calculate_loot(self, guild_id, message_id):

    channel = self.bot.get_channel(lib.Data.Global.Global_Variables.battle_channels[guild_id][lib.tokens.var_TestProd]["loots"])

    #On fait le tour de tous les slayers ayant attaqué
    for slayer in self.battleslist[guild_id][message_id].slayers_data:
        #On ne considère que les éligibles
        if self.battleslist[guild_id][message_id].slayers_data[slayer].eligible:
            
            #On calcule le loot obtenu
            loot = self.slayerlist[guild_id][slayer].GetLoot(element=self.battleslist[guild_id][message_id].monster_class.element, rarity=self.battleslist[guild_id][message_id].monster_class.rarity)
            isAlready = False
            view=None

            if loot is not None:
                if loot in self.slayerlist[guild_id][slayer].inventory_items:
                    isAlready = True
                    self.slayerlist[guild_id][slayer].money += lib.PostgreSQL.Rarities_list[lib.PostgreSQL.Items_list[loot]]["price"]
                else:
                    self.slayerlist[guild_id][slayer].inventory_items.append(loot)
                    view = lib.Buttons.Buttons_Loot(self)
                
                #On calcule l'embed à poster
                embed = lib.Embed.create_embed_loot(loot, isAlready)

                #On poste l'embed
                view.message = await channel.send(embed=embed, view=view)