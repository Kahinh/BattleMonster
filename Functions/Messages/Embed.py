import lib

def create_embed_battle(self):

    bot = self.bot
    cOpponent = self.Opponents[self.count]

    description=f"🔰*Score requis* : **{cOpponent.gearscore}**\n"
    description += f"\n**{cOpponent.group_name} {self.bot.Rarities[cOpponent.rarity].display_text.capitalize()}**"
    if cOpponent.type != "banner":
        description += f"\n⚔️ Puissance : **{int(cOpponent.damage)}** {self.bot.Elements[cOpponent.element].display_emote}"
    if int(cOpponent.armor) == int(cOpponent.armor_cap):
        description += f"\n🛡️ Armure : **{int(cOpponent.armor)}**"
    else:
        description += f"\n🛡️ Armure : **{int(cOpponent.armor)}** *({int(cOpponent.armor_cap)} min.)*"
    description += f"\n🎲 Butin Disponible : **{cOpponent.roll_dices}**"
    description += f"\n\n{cOpponent.description}"
    
    embed=lib.discord.Embed(
    title=
        f"{cOpponent.name} ({'{:,}'.format(int(cOpponent.base_hp)).replace(',', ' ')}/{'{:,}'.format(int(cOpponent.total_hp)).replace(',', ' ')} ❤️) {'💩💩' if len(cOpponent.loot_table) == 0 else ''}"
        if cOpponent.type != "banner"
        else
        f"{cOpponent.name} {'💩💩' if len(cOpponent.loot_table) == 0 else ''}",
    description=description,
    color=int(self.bot.Rarities[cOpponent.rarity].display_color, 16)
    )
    value = ""
    #Parry
    if cOpponent.type != "banner":
        value += f"✊ Chance de blocage - Attaque Légère: **{int(cOpponent.parry['parry_chance_l'] * 100)}%**\n" \
                f"✊ Chance de blocage - Attaque Lourde: **{int(cOpponent.parry['parry_chance_h'] * 100)}%**\n" \
                f"🗡️ Létalité : **({int(cOpponent.letality)}, {int(cOpponent.letality_per *100)}%)**\n"
    #Létalité & Résistance Critique
    value += f"🧿 Résistance Critique : **{cOpponent.protect_crit}**\n"

    #Statistiques avancées
    embed.add_field(name="Statistiques Avancées", \
        value= value,
        inline=False)
    if cOpponent.img_url_normal is not None:
        embed.set_thumbnail(url=f"{cOpponent.img_url_normal}")
    if cOpponent.bg_url is not None:
        embed.set_image(url=f"{cOpponent.bg_url}")
    if self.spawns_count > 1:   
        embed.set_footer(text=f"{cOpponent.group_name} : {self.count+1}/{self.spawns_count}")

    #Buffs
    if len(cOpponent.buffs) > 0:
        embed.add_field(name="Altérations d'état", value=cOpponent.get_display_buffs(), inline=False)

    #Banner
    if cOpponent.type == "banner":
        listed_factions = sorted(cOpponent.faction_best_damage.items(), key=lambda x:x[1], reverse=True)
        value = ""
        i = 0
        award_list = ["🥇","🥈","🥉","🏅"]
        for faction_best_damage_list in listed_factions:
            value += f"\n{award_list[i]} - {bot.Factions[faction_best_damage_list[0]].emote} {bot.Factions[faction_best_damage_list[0]].name}: **{faction_best_damage_list[1]}**"
            i += 1
        embed.add_field(name=f"Classement meilleur combo de {cOpponent.nbr_hit_stack} coups:", value=value, inline=False)

    if cOpponent.type == "banner":
        embed.set_footer(text=f"Fin de combat : {lib.datetime.datetime.fromtimestamp(self.timer_start + int(self.bot.Variables['factionwar_timing_before_end_seconds'])).strftime('%H:%M:%S')}")

    return embed

def create_embed_end_battle(Battle, timeout):
    #TITLE
    if timeout == False:
        title = f"**{Battle.name.capitalize()} achevé ✨ Tous les monstres ont été vaincus !**"
    else: 
        if Battle.stats["kills"] >= int(Battle.bot.Variables["battle_kills_before_escape"]):
            title = f"**{Battle.name.capitalize()} achevé : 🐉 Vous avez échoué, trop de Slayers sont morts.**"
        else:
            title = f"**{Battle.name.capitalize()} achevé : 🐉 Vous avez échoué et les monstres se sont enfuis.**"
    
    description = "**Bilan du combat :**"
    for cOpponent in Battle.Opponents:
        if int(cOpponent.base_hp) == 0:
            description += f"\n- {Battle.bot.Elements[cOpponent.element].display_emote} {cOpponent.name} ({int(cOpponent.base_hp)}/{int(cOpponent.total_hp)} 💀)"
        else:
            description += f"\n- {Battle.bot.Elements[cOpponent.element].display_emote} {cOpponent.name} ({int(cOpponent.base_hp)}/{int(cOpponent.total_hp)} ❤️)"
    
    description += f"\n\n⚔️ Attaques reçues : {Battle.stats['attacks_received']}"
    description += f"\n🩸 Dégâts infligés : {Battle.stats['attacks_done']}"
    description += f"\n💀 Slayers morts : {Battle.stats['kills']}"
    description += f"\n🎁 Butins récupérés : {Battle.stats['loots']}"
    description += f"\n🪙 Or distribué : {Battle.stats['money']}"
    if Battle.stats["mythic_stones"] != 0:
        description += f"\n💠 Pierres Mythiques : {Battle.stats['mythic_stones']}" 
    embed=lib.discord.Embed(title=title, description=description, color=0xe74c3c if timeout else 0x2ecc71)
    embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/K5FrBGB9d-8IbCg_bnZyheglS9Q61aXohV4hJSMiImA/%3Fcb%3D20200801054948/https/static.wikia.nocookie.net/dauntless_gamepedia_en/images/1/13/Hunt_Icon.png/revision/latest')
    return embed

def create_embed_end_factionwar(Battle):
    #TITLE
    bot = Battle.bot
    cOpponent = Battle.Opponents[0]

    title = f"**{Battle.name.capitalize()} achevé : ✨ Félicitations Factions !**"
    
    description = "**Bilan du combat :**"
    description += f"\n\n⚔️ Attaques reçues : {Battle.stats['attacks_received']}"
    description += f"\n🎁 Butins récupérés : {Battle.stats['loots']}"
    description += f"\n🪙 Or distribué : {Battle.stats['money']}"
    if Battle.stats["mythic_stones"] != 0:
        description += f"\n💠 Pierres Mythiques : {Battle.stats['mythic_stones']}" 

    embed=lib.discord.Embed(title=title, description=description, color=0x2ecc71)

    #Banner
    if cOpponent.type == "banner":
        listed_factions = sorted(cOpponent.faction_best_damage.items(), key=lambda x:x[1], reverse=True)
        value = ""
        i = 0
        award_list = ["🥇","🥈","🥉","🏅"]
        for faction_best_damage_list in listed_factions:
            value += f"\n{award_list[i]} - {bot.Factions[faction_best_damage_list[0]].emote} {bot.Factions[faction_best_damage_list[0]].name}: **{faction_best_damage_list[1]}**"
            i += 1
        embed.add_field(name=f"Classement meilleur combo de {cOpponent.nbr_hit_stack} coups:", value=value, inline=False)

    embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/K5FrBGB9d-8IbCg_bnZyheglS9Q61aXohV4hJSMiImA/%3Fcb%3D20200801054948/https/static.wikia.nocookie.net/dauntless_gamepedia_en/images/1/13/Hunt_Icon.png/revision/latest')
    return embed

def create_embed_new_loot(bot, cSlayer, cObject):

    content = cSlayer.equippedonSlot(cObject.slot)
    #Setup Description
    description = \
        f"*{bot.Elements[cObject.element].display_emote} {bot.Slots[cObject.slot].display_text} {bot.Rarities[cObject.rarity].display_text}*" \
        f"\n\n{cObject.description}"

    if content != "":
        description += content

    description += \
        f"\n\n📑 Détails - Afficher les statistiques de l'équipement" \
        f"\n👚 Equiper - Equiper l'objet." \
        f"\n🪙 Vendre - Vendre l'objet pour obtenir **{bot.Rarities[cObject.rarity].price} 🪙**"

    embed=lib.discord.Embed(title=f"{cObject.name}",
    description= \
        f"{description}",
    color=int(bot.Rarities[cObject.rarity].display_color, 16)
    )

    embed.set_thumbnail(url=cObject.img_url)

    return embed

def create_embed_money_loot(bot, cSlayer, cObject):

    content = cSlayer.equippedonSlot(cObject.slot)

    #Setup Description
    description = \
        f"*{bot.Elements[cObject.element].display_emote} {bot.Slots[cObject.slot].display_text} {bot.Rarities[cObject.rarity].display_text}*" \
        f"\n\n{cObject.description}"

    if content != "":
        description += content

    description += \
        f"\n\nVous possédez déjà ce {bot.Slots[cObject.slot].display_text} ! Il a dont été vendu pour **{bot.Rarities[cObject.rarity].price} 🪙**" \
        f"\n\n📑 Détails - Afficher les statistiques de l'équipement"

    embed=lib.discord.Embed(title=f"{cObject.name}",
    description=description,
    color=int(bot.Rarities[cObject.rarity].display_color, 16)
    )

    embed.set_thumbnail(url=cObject.img_url)

    return embed

def create_embed_item(bot, cSlayer, cObject1, cObject2=None):
    #cObject1 = Celui qu'on regarde
    #cObject2 = Celui qu'on possède
    if cObject1 == None:
        embed=lib.discord.Embed(title=f"No Item",
        description= \
            f"Aucun item ne correspond à la sélection.",
        color=0xe74c3c
        )        
    else:
        desc_stat = cObject1.getDisplayStats(cObject2)
        slots_items_equipped = cSlayer.slot_items_equipped(bot.Slots[cObject1.slot])

        description = f"__Description :__\n{cObject1.description}"

        if slots_items_equipped != []:
            description += f"\n\n__Objet(s) actuellement équipés à cet emplacement :__"
            for cObject in slots_items_equipped:
                description += f"\n- {bot.Elements[cObject.element].display_emote} {'[' + str(cObject.level) + ']' if cObject.level > 0 else ''} {cObject.name} ({cObject.slot} / {bot.Rarities[cObject.rarity].display_text})"


        description += f"\n\n__Statistiques :__{desc_stat}"
        
        embed=lib.discord.Embed(title=f"{bot.Elements[cObject1.element].display_emote} {'[Nv. ' + str(cObject1.level) + ']' if cObject1.level > 0 else ''} {cObject1.name} ({cObject1.slot} / {bot.Rarities[cObject1.rarity].display_text})",
        description= \
            f"{description}",
        color=int(bot.Rarities[cObject1.rarity].display_color, 16)
        )

        embed.set_thumbnail(url=f"{cObject1.img_url}")
        embed.set_footer(text=f"ID: {cObject1.id}")
    return embed

def create_embed_achievement(cSlayer, avatar):

    description = \
    f"🎖️ Monstres tués : **{cSlayer.achievements['monsters_killed']}**" \
    f"\n🏆 Meilleur attaque : **{cSlayer.achievements['biggest_hit']}**"

    embed=lib.discord.Embed(title=f"Prouesses de {cSlayer.name}",
    description=description,
    color=0x1abc9c)   

    embed.set_thumbnail(url=avatar)
    embed.set_footer(text=f'Chasse depuis le {lib.datetime.datetime.fromtimestamp(cSlayer.creation_date).strftime("%d/%m/%Y")}')
    return embed

def create_embed_equipment(bot, cLoadout_or_cSlayer, avatar, group):
    description = f"Score d'équipement : **{int(cLoadout_or_cSlayer.gearscore)}**\n"
    for _, cSlot in bot.Slots.items():
        if cSlot.activated and cSlot.group == group:
            if (nbr := cLoadout_or_cSlayer.slot_nbr_max_items(cSlot)) > 0:
                description += f"\n**{cSlot.display_emote} {cSlot.display_text}** - ({str(nbr)})"
                for cObject in cLoadout_or_cSlayer.slot_items_equipped(cSlot):
                    if cObject.level > 1:
                        description += f"\n- {bot.Elements[cObject.element].display_emote} [{cObject.level}] {cObject.name} - *{bot.Rarities[cObject.rarity].display_text}*"
                    else:
                        description += f"\n- {bot.Elements[cObject.element].display_emote} {cObject.name} - *{bot.Rarities[cObject.rarity].display_text}*"


    embed=lib.discord.Embed(title=f"Équipement de {cLoadout_or_cSlayer.name}",
    description=description,
    color=0x1abc9c)   

    embed.set_thumbnail(url=avatar)
    if hasattr(cLoadout_or_cSlayer, "creation_date"):
        embed.set_footer(text=f'Chasse depuis le {lib.datetime.datetime.fromtimestamp(cLoadout_or_cSlayer.creation_date).strftime("%d/%m/%Y")}')
    return embed

def create_embed_spe(cSlayer, cSpe):
    embed=lib.discord.Embed(title=f"{cSpe.emote} {cSpe.name}",
    description= \
        f"{cSpe.description}\n\n[**{cSpe.ability_name}**] : {cSpe.description_special}\n" \
        f"```ansi\n☄️Charges: {cSpe.stacks}```" \
        f"\n\n__Statistiques :__"
        f"{cSpe.getDisplayStats()}" \
        f"\n**Actuellement équipé :**" \
        f"\n{cSlayer.cSpe.emote} {cSlayer.cSpe.name}",
    color=0xe74c3c
    )        
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1000070083915304991/1033518782544613417/unknown.png")
    return embed 

def create_embed_recap_loot(bot, recap_loot):

    description = ""
    if recap_loot.get('money', 0) != 0:
        description = f"🪙 récupérés : {recap_loot['money']}"
    if recap_loot.get('mythic_stones', 0) != 0:
        description = f"💠 récupérées : {recap_loot['mythic_stones']}"
    if recap_loot.get('items', []) != []:
        description += f"\n\n__Item(s) récupéré(s) :__"
        for cObject in recap_loot['items']:
            description += f"\n- {bot.Elements[cObject.element].display_emote} {cObject.name} (*{bot.Slots[cObject.slot].display_text} {bot.Rarities[cObject.rarity].display_text}*)"

    embed=lib.discord.Embed(title=f"Récapitulatif Butin :",
    description=description,
    color=0xe74c3c
    )        
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1000070083915304991/1034553474999922848/unknown.png?width=1022&height=1022")
    return embed        

def create_embed_new_pet(bot, cSlayer, cObject):
    #Setup Description
    description = \
        f"*{bot.Elements[cObject.element].display_emote} {bot.Slots[cObject.slot].display_text} {bot.Rarities[cObject.rarity].display_text}*" \
        f"\n\n{cObject.description}"

    description += \
        f"\n\nOH OH ! Que voilà ?"

    embed=lib.discord.Embed(title=f"{cObject.name}",
    description= \
        f"{description}",
    color=int(bot.Rarities[cObject.rarity].display_color, 16)
    )

    embed.set_thumbnail(url=cObject.img_url)

    return embed

def create_embed_gatherables(Gather):
    #Setup Description
    description = \
        f"*Ressource - {Gather.type} {Gather.bot.Rarities[Gather.rarity].display_text}*" \
        f"\n\n{Gather.description}" \
        "\n\n Dépêchez-vous de récolter cette ressource avant qu'elle ne disparaisse !"

    embed=lib.discord.Embed(title=f"{Gather.name}",
    description= \
        f"{description}",
    color=int(Gather.bot.Rarities[Gather.rarity].display_color, 16)
    )

    embed.set_thumbnail(url=Gather.img_url)

    return embed    

def create_embed_gatherables_gathered(Gather, nbr=1):
    #Setup Description
    description = \
        f"Vous avez récolté : {nbr} {Gather.name}"

    embed=lib.discord.Embed(title=f"Récolte",
    description= \
        f"{description}",
    color=int(Gather.bot.Rarities[Gather.rarity].display_color, 16)
    )
    embed.set_thumbnail(url=Gather.img_url)

    return embed   

def create_embed_gatherables_profil(cSlayer, avatar, bot):

    description = ""
    for gatherable_id in cSlayer.inventories["gatherables"]:
        if int(cSlayer.inventories["gatherables"][gatherable_id]) > 0:
            description += f"\n- {bot.Gatherables[gatherable_id].display_emote} {bot.Gatherables[gatherable_id].name} : {cSlayer.inventories['gatherables'][gatherable_id]}"

    embed=lib.discord.Embed(title=f"Ressources de {cSlayer.name}",
    description=description,
    color=0x1abc9c)   

    embed.set_thumbnail(url=avatar)
    embed.set_footer(text=f'Chasse depuis le {lib.datetime.datetime.fromtimestamp(cSlayer.creation_date).strftime("%d/%m/%Y")}')
    return embed

def create_embed_enhancement_pet(cSlayer, pet_list, index, bot):
    if pet_list == []:   
        embed=lib.discord.Embed(title=f"Pas d'améliorations",
        description="Vous ne possédez pas de familiers améliorables.",
        color=0x1abc9c)   
        #embed.set_thumbnail(url=avatar)
    else:
        cObject = pet_list[index]
        description = pet_list[index].description
        description += "\n"
        description += pet_list[index].getDisplayStats()

        description += "\n\n**__Nourriture :__**"
        description += f"\n{cObject.get_food().display_emote} {cObject.get_food().name} - **{cSlayer.inventories['gatherables'][cObject.get_food().id]}/{100-pet_list[index].level}** requis pour atteindre le nv. max."

        embed=lib.discord.Embed(title=f"{pet_list[index].name} - Niveau : {pet_list[index].level}",
        description=description,
        color=0x1abc9c)   

        embed.set_thumbnail(url=pet_list[index].img_url)
    return embed

def create_embed_enhancement_mythic(cSlayer, mythic_list, index, bot):
    if mythic_list == []:   
        embed=lib.discord.Embed(title=f"Pas d'améliorations disponibles",
        description="Vous ne possédez pas de mythiques améliorables.",
        color=0x1abc9c)   
        #embed.set_thumbnail(url=avatar)
    else:
        description = mythic_list[index].description
        description += "\n"
        description += mythic_list[index].getDisplayStats()

        description += "\n\n**__Améliorations :__**"
        description += f"\n{bot.Gatherables[5].display_emote} {bot.Gatherables[5].name} - **{cSlayer.inventories['gatherables'][5]}** disponibles."

        embed=lib.discord.Embed(title=f"{bot.Elements[mythic_list[index].element].display_emote} {mythic_list[index].name} - Niveau : {mythic_list[index].level}",
        description=description,
        color=0x1abc9c)   

        embed.set_thumbnail(url=mythic_list[index].img_url)
    return embed

def create_embed_profil_global(cLoadout_or_cSlayer, avatar, cLoadout2=None):

    duplicated = False
    if cLoadout2 is None: 
        cLoadout2 = cLoadout_or_cSlayer
        duplicated = True

    def btb():
    #back to basic
        return "\u001b[0;0m"

    def sa(equippednumber, secondnumber, order=1):
    #select ANSI
        #Basique : \u001b[0;0m
        #Rouge : \u001b[1;31m
        #Vert : \u001b[1;32m
        #Jaune : \u001b[1;33m
        equippednumber = int(equippednumber*100)
        secondnumber = int(secondnumber*100)
        if duplicated:
            return "\u001b[0;0m"
        if equippednumber == secondnumber:
            return "\u001b[1;33m"
        else:
            if order == 0:
                if equippednumber > secondnumber:
                    return "\u001b[1;31m"
                else:
                    return "\u001b[1;32m"
            else:
                if equippednumber > secondnumber:
                    return "\u001b[1;32m"
                else:
                    return "\u001b[1;31m"

    description = f"**{cLoadout_or_cSlayer.cSpe.emote} {cLoadout_or_cSlayer.cSpe.name}**"
    if hasattr(cLoadout_or_cSlayer, "money"):
        description += f"```- 🪙 Coin : {int(cLoadout_or_cSlayer.money)}```"
    description += "\n**__Statistiques__**"
    if hasattr(cLoadout_or_cSlayer, "money"):
        description += f"```- {'💀' if cLoadout_or_cSlayer.dead else '❤️'} Vie : {int(cLoadout_or_cSlayer.current_health)}/{int(cLoadout_or_cSlayer.health)}```"
    else:
        description += f"```ansi\n- ❤️ Vie : {sa(cLoadout2.stats('health'), cLoadout_or_cSlayer.stats('health'), 0)} {cLoadout_or_cSlayer.stats('health')} {btb() + '(' + str(cLoadout2.stats('health')) + ')' if not duplicated else ''}```"
    description += f"```ansi\n- 🔰 Score : {sa(cLoadout2.gearscore, cLoadout_or_cSlayer.gearscore, 0)} {cLoadout_or_cSlayer.gearscore} {btb() + '(' + str(cLoadout2.gearscore) + ')' if not duplicated else ''}```"
    description += f"```ansi\n- 🛡️ Armure : {sa(cLoadout2.stats('armor'), cLoadout_or_cSlayer.stats('armor'), 0)} {int(cLoadout_or_cSlayer.stats('armor'))} {btb() + '(' + str(int(cLoadout2.stats('armor'))) + ')' if not duplicated else ''}```"
    description += f"```ansi\n- 🌪️ Vivacité : {sa(cLoadout2.stats('cooldown'), cLoadout_or_cSlayer.stats('cooldown'), 1)} {cLoadout_or_cSlayer.stats('cooldown')}s {btb() + '(' + str(cLoadout2.stats('cooldown')) + 's)' if not duplicated else ''}```"
    if hasattr(cLoadout_or_cSlayer, "money"):
        description += f"```- ☄️ Charge : {cLoadout_or_cSlayer.special_stacks}/{int(cLoadout_or_cSlayer.stats('stacks'))}```"
    else:
        description += f"```ansi\n- ☄️ Charge : {sa(cLoadout2.stats('stacks'), cLoadout_or_cSlayer.stats('stacks'), 1)} {cLoadout_or_cSlayer.stats('stacks')} {btb() + '(' + str(cLoadout2.stats('stacks')) + ')' if not duplicated else ''}```"
    description += f"```ansi\n- 🍀 Luck : {sa(cLoadout2.stats('luck'), cLoadout_or_cSlayer.stats('luck'), 0)} {int(cLoadout_or_cSlayer.stats('luck') * 100)}% {btb() + '(' + str(int(cLoadout2.stats('luck')*100)) + '%)' if not duplicated else ''}```"

    embed=lib.discord.Embed(title=f"Profil de {cLoadout_or_cSlayer.name}",
    description=description,
    color=0x1abc9c)   

    if hasattr(cLoadout_or_cSlayer, "creation_date"):
        embed.set_thumbnail(url=avatar)
    else:
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1000070083915304991/1116618600158068826/150.png")
    if hasattr(cLoadout_or_cSlayer, "creation_date"):
        embed.set_footer(text=f'Chasse depuis le {lib.datetime.datetime.fromtimestamp(cLoadout_or_cSlayer.creation_date).strftime("%d/%m/%Y")}')
    return embed

def create_embed_profil_attack(cLoadout_or_cSlayer, avatar, hit, cLoadout2=None):
    bot = cLoadout_or_cSlayer.bot
    duplicated = False
    if cLoadout2 is None: 
        cLoadout2 = cLoadout_or_cSlayer
        duplicated = True

    def sa(equippednumber, secondnumber, order=1):
    #select ANSI
        #Basique : \u001b[0;0m
        #Rouge : \u001b[1;31m
        #Vert : \u001b[1;32m
        #Jaune : \u001b[1;33m
        equippednumber = int(equippednumber*100)
        secondnumber = int(secondnumber*100)
        if duplicated:
            return "\u001b[0;0m"
        if equippednumber == secondnumber:
            return "\u001b[1;33m"
        else:
            if order == 0:
                if equippednumber > secondnumber:
                    return "\u001b[1;31m"
                else:
                    return "\u001b[1;32m"
            else:
                if equippednumber > secondnumber:
                    return "\u001b[1;32m"
                else:
                    return "\u001b[1;31m"

    def btb():
    #back to basic
        return "\u001b[0;0m"

    def _ffin(number, stat=None):
        if stat is None:
            return f"{int(number)}"
        if bot.Statistics[stat].percentage:
            if (number*100)%1 == 0.0:
                return f"{int(number*100)}%"
            else:
                return f"{round(number*100,2)}%"
        else:
            return f"{int(number)}"

    description = "**__Statistiques__**"
    for stat, cStatistic in bot.Statistics.items():
        for subdivisions in cStatistic.sub_division():
            if f"_{hit}" in subdivisions:
                description += \
                    f"```ansi\n- {cStatistic.display_emote} {cStatistic.display_name}: " \
                    f"{'🔒' if cLoadout_or_cSlayer.cSpe.adapt_min(cStatistic.cap_min, cStatistic.name, cLoadout_or_cSlayer.stats) == cLoadout_or_cSlayer.stats(subdivisions) or cLoadout_or_cSlayer.cSpe.adapt_max(cStatistic.cap_max, cStatistic.name, cLoadout_or_cSlayer.stats) == cLoadout_or_cSlayer.stats(subdivisions) else ''}" \
                    f"{sa(cLoadout2.stats(subdivisions), cLoadout_or_cSlayer.stats(subdivisions), cStatistic.reverse)}" \
                    f"{_ffin(cLoadout_or_cSlayer.stats(subdivisions) + (cLoadout_or_cSlayer.cSpe.spe_damage if hit == 's' and subdivisions == 'damage_s' else 0), stat)}" \
                    f"{btb() + ' (' + _ffin(cLoadout2.stats(subdivisions), stat) + ')' if not duplicated else ''}```"
    embed=lib.discord.Embed(title=f"{hit} {cLoadout_or_cSlayer.name}",
    description=description,
    color=0x1abc9c)  
    if hasattr(cLoadout_or_cSlayer, "creation_date"):
        embed.set_thumbnail(url=avatar)
    else:
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1000070083915304991/1116618600158068826/150.png")
    if hasattr(cLoadout_or_cSlayer, "creation_date"):
        embed.set_footer(text=f'Chasse depuis le {lib.datetime.datetime.fromtimestamp(cLoadout_or_cSlayer.creation_date).strftime("%d/%m/%Y")}')
    return embed 