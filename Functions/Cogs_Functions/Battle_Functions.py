import lib

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
                        Slayer.Slayer_update()
                    else:
                        loots_list.append(loot["id"])
                        Slayer.inSlayerInventory_append(loot["id"])            
                    
                    #On calcule l'embed à poster
                    view = lib.Buttons.Buttons_Loot(Buttons_Battle, Slayer, loot, isAlready, rPrice, rRarity)
                    embed = lib.Embed.create_embed_loot(Buttons_Battle, loot, isAlready, rPrice, rRarity)
                    channel= Buttons_Battle.Main.bot.get_channel(rChannels["channel_id"])
                    view.message = await channel.send(content=f"<@{slayer_id}>", embed=embed, view=view)
        
            await Slayer.pushdB()  