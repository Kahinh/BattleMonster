import lib

async def isExist_Slayer(self, slayer):
    if slayer.id not in self.slayerlist:
        self.slayerlist[slayer.id] = lib.Classes.Slayers.Slayers(Run=self, name=slayer.name)

async def spawn_battle(self, monster_hp_scaling_based_on_active_players, gamemode, monster_to_spawn):
    #On calcule l'embed
    monster_class = lib.deepcopy(self.BDD["Monsters_list"][monster_to_spawn])
    monster_class.updateStats(monster_hp_scaling_based_on_active_players, self.BDD["GameModes_list"][gamemode]["scaling"], self.BDD["GameModes_list"][gamemode]["roll_dices"])

    message = await self.channels[gamemode].send(embed=lib.Embed.create_embed_spawn(self, monster_class), view=lib.Buttons.Buttons_Battle(self))

    #On crée l'entrée du combat dans la table
    self.battleslist[message.id] = lib.Classes.Battles.Battles(monster_class=monster_class, gamemode=gamemode, loots_slots=self.BDD["LootsSlot_list"][self.BDD["GameModes_list"][gamemode]["loots_slot"]], slayers_data={}, last_hits=[])

async def attack(self, interaction, hit):
    #Check Guild ID & User ID
    canAttack = False
    isDead = False

    await isExist_Slayer(self, interaction.user)

    #On calcule les dégâts
    Damage, Stacks_Earned = self.slayerlist[interaction.user.id].CalculateDamage(hit, self.battleslist[interaction.message.id], interaction.user.id)

    #On documente la Class DamageDone
    if interaction.user.id not in self.battleslist[interaction.message.id].slayers_data:
        self.battleslist[interaction.message.id].slayers_data[interaction.user.id] = lib.Classes.DamageDone.DamageDone(eligible=True if Damage > 0 else False, total_damage=Damage if Damage > 0 else 0, timestamp_next_hit=lib.datetime.datetime.timestamp(lib.datetime.datetime.now()) + self.slayerlist[interaction.user.id].calculateStats()["total_cooldown"])
        canAttack = True
    else:
        if self.battleslist[interaction.message.id].slayers_data[interaction.user.id].timestamp_next_hit < lib.datetime.datetime.timestamp(lib.datetime.datetime.now()):
            canAttack = True
            self.battleslist[interaction.message.id].slayers_data[interaction.user.id].updateClass(Damage = Damage, Cooldown = self.slayerlist[interaction.user.id].calculateStats())

    if Damage > 0 and canAttack:
        #On met à jour les PVs du monstre
        self.battleslist[interaction.message.id].GetDamage(damage=Damage, hit=hit, slayer_class=self.slayerlist[interaction.user.id])

    ephemeral_message = lib.Ephemeral.get_ephemeralAttack(self, Damage, hit, Stacks_Earned, self.slayerlist[interaction.user.id], self.battleslist[interaction.message.id], interaction.user.id, canAttack)
    await interaction.response.send_message(f'{ephemeral_message}', ephemeral=True)

    #On met à jour l'embed
    if self.battleslist[interaction.message.id].monster_class.base_hp == 0:
        await interaction.message.edit(embed=lib.Embed.create_embed_spawn(self, self.battleslist[interaction.message.id].monster_class), view=None)
        await calculate_loot(self, message_id=interaction.message.id)
        del self.battleslist[interaction.message.id]
        isDead = True
    else:
        await interaction.message.edit(embed=lib.Embed.create_embed_spawn(self, self.battleslist[interaction.message.id].monster_class))
    
    return isDead

async def calculate_loot(self, message_id):

    #On fait le tour de tous les slayers ayant attaqué
    for slayer_id in self.battleslist[message_id].slayers_data:
        #On ne considère que les éligibles
        if self.battleslist[message_id].slayers_data[slayer_id].eligible:

            #On prend en compte le roll_dice
            for i in range(self.battleslist[message_id].monster_class.roll_dices):
                
                #On calcule le loot obtenu
                loot = self.slayerlist[slayer_id].GetLoot(element=self.battleslist[message_id].monster_class.element, rarity=self.battleslist[message_id].monster_class.rarity)
                isAlready, isDetailed, view = False, False, None

                if loot is not None:
                    if loot in self.slayerlist[slayer_id].inventory_items:
                        isAlready = True
                        self.slayerlist[slayer_id].money += self.BDD["Rarities_list"][self.BDD["Items_list"][loot].rarity]["price"]
                    else:
                        self.slayerlist[slayer_id].inventory_items.append(loot)
                    
                    #On calcule l'embed à poster
                    view = lib.Buttons.Buttons_Loot(self, slayer_id, loot, isAlready)
                    embed = lib.Embed.create_embed_loot(self, loot, isAlready)
                    view.message = await self.channels["loots"].send(content=f"<@{slayer_id}>", embed=embed, view=view)
    
    lib.PostgreSQL_Tools.updateTables(self.slayerlist)