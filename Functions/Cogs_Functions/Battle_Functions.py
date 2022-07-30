import lib

async def spawn_handler(Main, Gamemode):

    async with Main.bot.db_pool.acquire() as conn:
        SlayerCount = await conn.fetchval(lib.qSlayers.COUNT)

        #On calcule le behemoth a faire spawn en prenant random dans la liste.
        async with Main.bot.db_pool.acquire() as conn:
            rarities = await conn.fetch(lib.qGameModes.SELECT_RARITY_POPULATION, Gamemode["name"])
            weights = await conn.fetch(lib.qGameModes.SELECT_RARITY_WEIGHT, Gamemode["name"])

        if len(rarities) == len(weights) and rarities != []:
            rarity_to_spawn = lib.random.choices(list(rarities), weights=[float(dict(element)['spawn_rate']) for element in weights], k=1)[0]
            embed, view, rChannels = await lib.Battle_Functions.create_battle(Main, Gamemode, next(rarity_to_spawn.values()))
            channel= Main.bot.get_channel(rChannels["channel_id"])
            message = await channel.send(embed=embed, view=view)

async def create_battle(Main, rGamemode, rarity_to_spawn):

    async with Main.bot.db_pool.acquire() as conn:
        rMonster = await conn.fetchrow(lib.qMonsters.SELECT_RANDOM, rarity_to_spawn)
        rChannels = await conn.fetchrow(lib.qChannels.SELECT_CHANNEL, lib.tokens.TestProd, rGamemode["name"])
        rElement = await conn.fetchrow(lib.qElements.SELECT_DISPLAY, rMonster["element"])
        rRarity = await conn.fetchrow(lib.qRarities.SELECT_DISPLAY, rMonster["rarity"])
        rHP_scaling = await conn.fetchval(lib.qSlayers.COUNT)

    #On calcule l'embed
    cMonster = lib.Monster(rMonster, rGamemode, max(rHP_scaling, 1))
    embed = lib.Embed.create_embed_spawn(Main, cMonster, rElement, rRarity)
    view = lib.Buttons.Buttons_Battle(Main, cMonster, rElement, rRarity)

    return embed, view, rChannels   

async def attack(Buttons_Battle, interaction, Hit):
    #Check Guild ID & User ID
    isDead = False
    bot = Buttons_Battle.Main.bot
    canAttack = False

    async with bot.db_pool.acquire() as conn:
        rRarities_Name = await conn.fetch(lib.qRaritiesLootRates.SELECT_RARITIES, Buttons_Battle.cMonster.rarity)
        rRarities_Weight = await conn.fetch(lib.qRaritiesLootRates.SELECT_WEIGHTS, Buttons_Battle.cMonster.rarity)

    #On init le Slayer
    Slayer = lib.MSlayer(Buttons_Battle.Main.bot, interaction)
    await Slayer.constructClass()

    if Slayer.cSlayer.dead == False:
        #On documente la Class DamageDone
        if interaction.user.id not in Buttons_Battle.cMonster.slayers_hits:
            Buttons_Battle.cMonster.slayers_hits[interaction.user.id] = lib.DamageDone(eligible=False, total_damage=0, timestamp_next_hit=lib.datetime.datetime.timestamp(lib.datetime.datetime.now()))
            canAttack = True
        elif Buttons_Battle.cMonster.slayers_hits[interaction.user.id].timestamp_next_hit < lib.datetime.datetime.timestamp(lib.datetime.datetime.now()):
            canAttack = True

        if (canAttack and Hit != "S") or (Hit == "S" and Slayer.cSlayer.canSpecial()):
            Damage, Stacks_Earned = Slayer.cSlayer.CalculateDamage(Hit, Buttons_Battle.cMonster)
            Buttons_Battle.cMonster.slayers_hits[interaction.user.id].updateClass(Damage, None if Hit == "S" else Slayer.cSlayer.stats["total_cooldown"])
        else:
            Damage, Stacks_Earned = 0, 0

        #On met à jour les PVs du monstre
        if Damage > 0: Buttons_Battle.cMonster.GetDamage(damage=Damage, hit=Hit, slayer_class=Slayer.cSlayer)
        ephemeral_message = lib.Ephemeral.get_ephemeralAttack(Damage, Stacks_Earned, Hit, Buttons_Battle, Slayer.cSlayer, Buttons_Battle.cMonster, interaction.user.id, canAttack)  
    else:
        ephemeral_message = lib.Ephemeral.get_ephemeralAttack(0, 0, Hit, Buttons_Battle, Slayer.cSlayer, Buttons_Battle.cMonster, interaction.user.id, canAttack)  
    
    await Slayer.Slayer_update()
    await Slayer.pushdB()
    await interaction.response.send_message(f'{ephemeral_message}', ephemeral=True)

    #On met à jour l'embed
    if Buttons_Battle.cMonster.base_hp == 0:
        await interaction.message.edit(embed=lib.Embed.create_embed_spawn(Buttons_Battle.Main, Buttons_Battle.cMonster, Buttons_Battle.rElement, Buttons_Battle.rRarity), view=None)
        await calculate_loot(Slayer, Buttons_Battle, rRarities_Name, rRarities_Weight)
        isDead = True
    else:
        await interaction.message.edit(embed=lib.Embed.create_embed_spawn(Buttons_Battle.Main, Buttons_Battle.cMonster, Buttons_Battle.rElement, Buttons_Battle.rRarity))
    
    return isDead

async def calculate_loot(Slayer, Buttons_Battle, rRarities_Name, rRarities_Weight):

    #On fait le tour de tous les slayers ayant attaqué
    for slayer_id in Buttons_Battle.cMonster.slayers_hits:
        #On ne considère que les éligibles
        if Buttons_Battle.cMonster.slayers_hits[slayer_id].eligible:
            loots_list = []

            #On prend en compte le roll_dice
            for i in range(Buttons_Battle.cMonster.roll_dices):
                
                #On calcule le loot obtenu
                rarity_loot, element = Slayer.cSlayer.GetLoot(element=Buttons_Battle.cMonster.element, rRarities_Name=rRarities_Name, rRarities_Weight=rRarities_Weight)

                if rarity_loot is not None:

                    isAlready, view = False, None
                    async with Buttons_Battle.Main.bot.db_pool.acquire() as conn:
                        loot = await conn.fetchrow(lib.qItems.SELECT_RANDOM, next(rarity_loot[0].values()), element)
                        rPrice = await conn.fetchval(lib.qRarities.SELECT_PRICE, next(rarity_loot[0].values()))
                        rChannels = await conn.fetchrow(lib.qChannels.SELECT_CHANNEL, lib.tokens.TestProd, "loots")
                        rRarity = await conn.fetchrow(lib.qRarities.SELECT_DISPLAY, next(rarity_loot[0].values()))

                    if loot["id"] in Slayer.cSlayer.inventory_items or loot["id"] in loots_list:
                        isAlready = True
                        Slayer.cSlayer.money += rPrice
                        await Slayer.Slayer_update()
                    else:
                        loots_list.append(loot["id"])
                        await Slayer.inSlayerInventory_append(loot["id"])            
                    
                    #On calcule l'embed à poster
                    view = lib.Buttons.Buttons_Loot(Buttons_Battle, Slayer, loot, isAlready, rPrice, rRarity)
                    embed = lib.Embed.create_embed_loot(Buttons_Battle, loot, isAlready, rPrice, rRarity)
                    channel= Buttons_Battle.Main.bot.get_channel(rChannels["channel_id"])
                    view.message = await channel.send(content=f"<@{slayer_id}>", embed=embed, view=view)
        
        await Slayer.pushdB()  