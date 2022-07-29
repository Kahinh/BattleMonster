import lib

async def spawn_handler(Main):

    async with Main.bot.db_pool.acquire() as conn:
        rGamemodes = await conn.fetch(lib.qGameModes.SELECT_ALL)
        SlayerCount = await conn.fetchval(lib.qSlayers.COUNT)

    for rGamemode in rGamemodes:
        #Doit on faire spawn un monster ?

        hp_scaling = max(1, SlayerCount)
        #On calcule le behemoth a faire spawn en prenant random dans la liste.
        async with Main.bot.db_pool.acquire() as conn:
            rarities = await conn.fetch(lib.qGameModes.SELECT_RARITY_POPULATION, rGamemode["name"])
            weights = await conn.fetch(lib.qGameModes.SELECT_RARITY_WEIGHT, rGamemode["name"])

        if len(rarities) == len(weights) and rarities != []:
            rarity_to_spawn = lib.random.choices(list(rarities), weights=[float(dict(element)['spawn_rate']) for element in weights], k=1)[0]
            embed, view, channel = await lib.Battle_Functions.create_battle(Main, hp_scaling, rGamemode, next(rarity_to_spawn.values()))
            message = await channel.send(embed=embed, view=view)

async def isExist_Slayer(Buttons_Battle, slayer):
    if slayer.id not in Buttons_Battle.Main.bot.slayers_list:
        Buttons_Battle.Main.bot.slayers_list[slayer.id] = lib.Slayer(Run=Buttons_Battle.Main, name=slayer.name)

async def create_battle(Main, hp_scaling, rGamemode, rarity_to_spawn):

    async with Main.bot.db_pool.acquire() as conn:
        rMonster = await conn.fetchrow(lib.qMonsters.SELECT_RANDOM, rarity_to_spawn)
        rChannels = await conn.fetchrow(lib.qChannels.SELECT_CHANNEL, lib.tokens.TestProd, rGamemode["name"])
        rElement = await conn.fetchrow(lib.qElements.SELECT_DISPLAY, rMonster["element"])
        rRarity = await conn.fetchrow(lib.qRarities.SELECT_DISPLAY, rMonster["rarity"])
    channel= Main.bot.get_channel(rChannels["channel_id"])

    #On calcule l'embed
    cMonster = lib.Monster(rMonster, rGamemode, hp_scaling)
    embed = lib.Embed.create_embed_spawn(Main, cMonster, rElement, rRarity)
    view = lib.Buttons.Buttons_Battle(Main, cMonster, rElement, rRarity)

    return embed, view, channel
    

async def attack(Buttons_Battle, interaction, hit):
    #Check Guild ID & User ID
    isDead = False
    bot = Buttons_Battle.Main.bot

    canAttack = False

    await isExist_Slayer(Buttons_Battle, interaction.user)

    async with bot.db_pool.acquire() as conn:
        rBaseBonuses = await conn.fetchrow(lib.qBaseBonuses.SELECT_BASE_BONUSES)
        rItemsSlayer = await conn.fetch(lib.qSlayers.SELECT_PLAYER_ITEMS, interaction.user.id)
        rRarities_Name = await conn.fetch(lib.qRaritiesLootRates.SELECT_RARITIES, Buttons_Battle.cMonster.rarity)
        rRarities_Weight = await conn.fetch(lib.qRaritiesLootRates.SELECT_WEIGHTS, Buttons_Battle.cMonster.rarity)

    #On documente la Class DamageDone
    if interaction.user.id not in Buttons_Battle.cMonster.slayers_hits:
        Buttons_Battle.cMonster.slayers_hits[interaction.user.id] = lib.DamageDone(eligible=False, total_damage=0, timestamp_next_hit=lib.datetime.datetime.timestamp(lib.datetime.datetime.now()))
        canAttack = True
    elif Buttons_Battle.cMonster.slayers_hits[interaction.user.id].timestamp_next_hit < lib.datetime.datetime.timestamp(lib.datetime.datetime.now()):
        canAttack = True

    if (canAttack and hit != "S") or (hit == "S" and bot.slayers_list[interaction.user.id].canSpecial(rBaseBonuses, rItemsSlayer)):
        #On calcule les dégâts
        Damage, Stacks_Earned, Stats = bot.slayers_list[interaction.user.id].CalculateDamage(hit, Buttons_Battle.cMonster, rBaseBonuses, rItemsSlayer)
        Buttons_Battle.cMonster.slayers_hits[interaction.user.id].updateClass(Damage, None if hit == "S" else Stats["total_cooldown"])
    else:
        Damage, Stacks_Earned, Stats = 0, 0, bot.slayers_list[interaction.user.id].calculateStats(rBaseBonuses, rItemsSlayer)

    if Damage > 0:
        #On met à jour les PVs du monstre
        Buttons_Battle.cMonster.GetDamage(damage=Damage, hit=hit, slayer_class=bot.slayers_list[interaction.user.id])

    ephemeral_message = lib.Ephemeral.get_ephemeralAttack(Buttons_Battle, Damage, hit, Stacks_Earned, Buttons_Battle.cMonster, interaction.user.id, canAttack, rBaseBonuses, rItemsSlayer, Stats, bot.slayers_list[interaction.user.id].canSpecial(rBaseBonuses, rItemsSlayer))
    await interaction.response.send_message(f'{ephemeral_message}', ephemeral=True)

    #On met à jour l'embed
    if Buttons_Battle.cMonster.base_hp == 0:
        await interaction.message.edit(embed=lib.Embed.create_embed_spawn(Buttons_Battle.Main, Buttons_Battle.cMonster, Buttons_Battle.rElement, Buttons_Battle.rRarity), view=None)
        await calculate_loot(Buttons_Battle, rBaseBonuses, rItemsSlayer, rRarities_Name, rRarities_Weight)
        isDead = True
    else:
        await interaction.message.edit(embed=lib.Embed.create_embed_spawn(Buttons_Battle.Main, Buttons_Battle.cMonster, Buttons_Battle.rElement, Buttons_Battle.rRarity))
    
    return isDead

async def calculate_loot(Buttons_Battle, rBaseBonuses, rItemsSlayer, rRarities_Name, rRarities_Weight):

    #On fait le tour de tous les slayers ayant attaqué
    for slayer_id in Buttons_Battle.cMonster.slayers_hits:
        #On ne considère que les éligibles
        if Buttons_Battle.cMonster.slayers_hits[slayer_id].eligible:

            #On prend en compte le roll_dice
            for i in range(Buttons_Battle.cMonster.roll_dices):
                
                #On calcule le loot obtenu
                rarity_loot, element = Buttons_Battle.Main.bot.slayers_list[slayer_id].GetLoot(element=Buttons_Battle.cMonster.element, rBaseBonuses=rBaseBonuses, rItemsSlayer=rItemsSlayer, rRarities_Name=rRarities_Name, rRarities_Weight=rRarities_Weight)

                if rarity_loot is not None:

                    isAlready, view = False, None
                    async with Buttons_Battle.Main.bot.db_pool.acquire() as conn:
                        loot = await conn.fetchrow(lib.qItems.SELECT_RANDOM, next(rarity_loot[0].values()), element)
                        rPrice = await conn.fetchval(lib.qRarities.SELECT_PRICE, next(rarity_loot[0].values()))
                        rChannels = await conn.fetchrow(lib.qChannels.SELECT_CHANNEL, lib.tokens.TestProd, "loots")
                        rRarity = await conn.fetchrow(lib.qRarities.SELECT_DISPLAY, next(rarity_loot[0].values()))

                    if loot["id"] in Buttons_Battle.Main.bot.slayers_list[slayer_id].inventory_items:
                        isAlready = True
                        Buttons_Battle.Main.bot.slayers_list[slayer_id].money += rPrice
                    else:
                        Buttons_Battle.Main.bot.slayers_list[slayer_id].inventory_items.append(loot["id"])
                    
                    #On calcule l'embed à poster
                    view = lib.Buttons.Buttons_Loot(Buttons_Battle, slayer_id, loot, isAlready, rPrice, rRarity)
                    embed = lib.Embed.create_embed_loot(Buttons_Battle, loot, isAlready, rPrice, rRarity)
                    channel= Buttons_Battle.Main.bot.get_channel(rChannels["channel_id"])
                    view.message = await channel.send(content=f"<@{slayer_id}>", embed=embed, view=view)