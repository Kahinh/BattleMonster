import lib

def create_embed_battle(self):

    bot = self.bot

    description=f"🔰*Score requis* : **{self.Opponents[self.count].gearscore}**\n"
    description += f"\n**{self.Opponents[self.count].group_name} {self.bot.Rarities[self.Opponents[self.count].rarity].display_text.capitalize()}**"
    if self.Opponents[self.count].type != "banner":
        description += f"\n⚔️ Puissance : **{int(self.Opponents[self.count].damage)}** {self.bot.Elements[self.Opponents[self.count].element].display_emote}"
    if int(self.Opponents[self.count].armor) == int(self.Opponents[self.count].armor_cap):
        description += f"\n🛡️ Armure : **{int(self.Opponents[self.count].armor)}**"
    else:
        description += f"\n🛡️ Armure : **{int(self.Opponents[self.count].armor)}** *({int(self.Opponents[self.count].armor_cap)} min.)*"
    description += f"\n🎲 Butin Disponible : **{self.Opponents[self.count].roll_dices}**"
    description += f"\n\n{self.Opponents[self.count].description}"
    
    embed=lib.discord.Embed(
    title=
        f"{self.Opponents[self.count].name} ({'{:,}'.format(int(self.Opponents[self.count].base_hp)).replace(',', ' ')}/{'{:,}'.format(int(self.Opponents[self.count].total_hp)).replace(',', ' ')} ❤️) {'💩💩' if len(self.Opponents[self.count].loot_table) == 0 else ''}"
        if self.Opponents[self.count].type != "banner"
        else
        f"{self.Opponents[self.count].name} {'💩💩' if len(self.Opponents[self.count].loot_table) == 0 else ''}",
    description=description,
    color=int(self.bot.Rarities[self.Opponents[self.count].rarity].display_color, 16)
    )
    value = ""
    #Parry
    if self.Opponents[self.count].type != "banner":
        value += f"✊ Chance de blocage - Attaque Légère: **{int(self.Opponents[self.count].parry['parry_chance_l'] * 100)}%**\n" \
                f"✊ Chance de blocage - Attaque Lourde: **{int(self.Opponents[self.count].parry['parry_chance_h'] * 100)}%**\n" \
                f"🗡️ Létalité : **({int(self.Opponents[self.count].letality)}, {int(self.Opponents[self.count].letality_per *100)}%)**\n"
    #Létalité & Résistance Critique
    value += f"🧿 Résistance Critique : **{self.Opponents[self.count].protect_crit}**\n"

    #Statistiques avancées
    embed.add_field(name="Statistiques Avancées", \
        value= value,
        inline=False)
    if self.Opponents[self.count].img_url_normal is not None:
        embed.set_thumbnail(url=f"{self.Opponents[self.count].img_url_normal}")
    if self.Opponents[self.count].bg_url is not None:
        embed.set_image(url=f"{self.Opponents[self.count].bg_url}")
    if self.spawns_count > 1:   
        embed.set_footer(text=f"{self.Opponents[self.count].group_name} : {self.count+1}/{self.spawns_count}")
    
    #Banner
    if self.Opponents[self.count].type == "banner":
        listed_factions = sorted(self.Opponents[self.count].faction_best_damage.items(), key=lambda x:x[1], reverse=True)
        value = ""
        i = 0
        award_list = ["🥇","🥈","🥉","🏅"]
        for faction_best_damage_list in listed_factions:
            value += f"\n{award_list[i]} - {bot.Factions[faction_best_damage_list[0]].emote} {bot.Factions[faction_best_damage_list[0]].name}: **{faction_best_damage_list[1]}**"
            i += 1
        embed.add_field(name=f"Classement {bot.Variables['factionwar_nbr_hit_stack']} meilleures attaques :", value=value, inline=False)

    return embed

def create_embed_end_battle(Battle, timeout):
    #TITLE
    if timeout == False:
        title = f"**{Battle.name.capitalize()} achevé ✨ Tous les monstres ont été vaincus !**"
    else: 
        if Battle.stats["kills"] >= Battle.bot.Variables["battle_kills_before_escape"]:
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

    title = f"**{Battle.name.capitalize()} achevé : ✨ Félicitations Factions !**"
    
    description = "**Bilan du combat :**"
    description += f"\n\n⚔️ Attaques reçues : {Battle.stats['attacks_received']}"
    description += f"\n🎁 Butins récupérés : {Battle.stats['loots']}"
    description += f"\n🪙 Or distribué : {Battle.stats['money']}"
    if Battle.stats["mythic_stones"] != 0:
        description += f"\n💠 Pierres Mythiques : {Battle.stats['mythic_stones']}" 

    embed=lib.discord.Embed(title=title, description=description, color=0x2ecc71)

    #Banner
    if Battle.Opponents[0].type == "banner":
        listed_factions = sorted(Battle.Opponents[0].faction_best_damage.items(), key=lambda x:x[1], reverse=True)
        value = ""
        i = 0
        award_list = ["🥇","🥈","🥉","🏅"]
        for faction_best_damage_list in listed_factions:
            value += f"\n{award_list[i]} - {bot.Factions[faction_best_damage_list[0]].emote} {bot.Factions[faction_best_damage_list[0]].name}: **{faction_best_damage_list[1]}**"
            i += 1
        embed.add_field(name=f"Classement {bot.Variables['factionwar_nbr_hit_stack']} meilleures attaques :", value=value, inline=False)

    embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/K5FrBGB9d-8IbCg_bnZyheglS9Q61aXohV4hJSMiImA/%3Fcb%3D20200801054948/https/static.wikia.nocookie.net/dauntless_gamepedia_en/images/1/13/Hunt_Icon.png/revision/latest')
    return embed

def create_embed_new_loot(bot, Slayer, cItem):

    content = Slayer.equippedonSlot(cItem.slot)
    #Setup Description
    description = \
        f"*{bot.Elements[cItem.element].display_emote} {bot.rSlots[cItem.slot]['display_text']} {bot.Rarities[cItem.rarity].display_text}*" \
        f"\n\n{cItem.description}"

    if content != "":
        description += content

    description += \
        f"\n\n📑 Détails - Afficher les statistiques de l'équipement" \
        f"\n👚 Equiper - Equiper l'objet." \
        f"\n🪙 Vendre - Vendre l'objet pour obtenir **{bot.Rarities[cItem.rarity].price} 🪙**"

    embed=lib.discord.Embed(title=f"{cItem.name}",
    description= \
        f"{description}",
    color=int(bot.Rarities[cItem.rarity].display_color, 16)
    )

    embed.set_thumbnail(url=cItem.img_url)

    return embed

def create_embed_money_loot(bot, Slayer, cItem):

    content = Slayer.equippedonSlot(cItem.slot)

    #Setup Description
    description = \
        f"*{bot.Elements[cItem.element].display_emote} {bot.rSlots[cItem.slot]['display_text']} {bot.Rarities[cItem.rarity].display_text}*" \
        f"\n\n{cItem.description}"

    if content != "":
        description += content

    description += \
        f"\n\nVous possédez déjà ce {bot.rSlots[cItem.slot]['display_text']} ! Il a dont été vendu pour **{bot.Rarities[cItem.rarity].price} 🪙**" \
        f"\n\n📑 Détails - Afficher les statistiques de l'équipement"

    embed=lib.discord.Embed(title=f"{cItem.name}",
    description=description,
    color=int(bot.Rarities[cItem.rarity].display_color, 16)
    )

    embed.set_thumbnail(url=cItem.img_url)

    return embed

def create_embed_item(bot, cItem1, Slayer, cItem2=None):
    #cItem1 = Celui qu'on regarde
    #cItem2 = Celui qu'on possède
    if cItem1 == None:
        embed=lib.discord.Embed(title=f"No Item",
        description= \
            f"Aucun item ne correspond à la sélection.",
        color=0xe74c3c
        )        
    else:
        desc_stat = cItem1.getDisplayStats(cItem2)
        content = Slayer.equippedonSlot(cItem1.slot)

        description = f"__Description :__\n{cItem1.description}"

        if content != "":
            description += content

        description += f"\n\n__Statistiques :__{desc_stat}"
        
        embed=lib.discord.Embed(title=f"{bot.Elements[cItem1.element].display_emote} {'[' + str(cItem1.level) + ']' if cItem1.level > 0 else ''} {cItem1.name} ({cItem1.slot} / {bot.Rarities[cItem1.rarity].display_text})",
        description= \
            f"{description}",
        color=int(bot.Rarities[cItem1.rarity].display_color, 16)
        )

        embed.set_thumbnail(url=f"{cItem1.img_url}")
    return embed

def create_embed_profil(Slayer, avatar):

    description = \
    f"**{Slayer.cSlayer.Spe.emote} {Slayer.cSlayer.Spe.name}** {'*[ON : ' + str(Slayer.cSlayer.berserker_mode) + '/5]*' if Slayer.cSlayer.berserker_mode > 0 else ''}" \
    f"\n🪙 Coin : **{int(Slayer.cSlayer.money)}**" \
    "\n\n**__Statistiques__**" \
    f"\n{'💀' if Slayer.cSlayer.dead else '❤️'} Vie : **{int(Slayer.cSlayer.stats['total_max_health'] - Slayer.cSlayer.damage_taken)}/{Slayer.cSlayer.stats['total_max_health']}**" \
    f"\n🔰 Score : **{Slayer.cSlayer.gearscore}**" \
    f"\n🛡️ Armure : **{Slayer.cSlayer.stats['total_armor']}**" \
    f"\n🌪️ Vivacité : **{Slayer.cSlayer.stats['total_cooldown']}**s" \
    f"\n☄️ Charge : **{Slayer.cSlayer.special_stacks}/{Slayer.cSlayer.stats['total_stacks']}**" \
    f"\n🍀 Luck : **{Slayer.cSlayer.stats['total_luck'] * 100}**%"

    embed=lib.discord.Embed(title=f"Profil de {Slayer.cSlayer.name}",
    description=description,
    color=0x1abc9c)   

    for i in ("l", "h", "s"):
        if not (i == "s" and Slayer.cSlayer.Spe.id == 8):
            if i == "l":
                name = "__Attaque Légère__"
            elif i == "h":
                name = "__Attaque Lourde__"
            elif i == "s":
                name = "__Capacité Spéciale__"
            description = \
            f"\n⚔️ Puissance : **{Slayer.cSlayer.stats['total_damage_' + i]}**" \
            f"\n⚔️ Dégâts Finaux : **{int(Slayer.cSlayer.stats['total_final_damage_' + i]*100)}**%" \
            f"\n☄️ Gains Charge : **{Slayer.cSlayer.stats['total_special_charge_' + i]}**" \
            f"\n✨ Chance Critique : **{int(Slayer.cSlayer.stats['total_crit_chance_' + i]*100)}**%" \
            f"\n💢 Dégâts Critiques : **{int(Slayer.cSlayer.stats['total_crit_damage_' + i]*100)}**%" \
            f"\n🗡️ Létalité : **{Slayer.cSlayer.stats['total_letality_' + i]}**,  **{int(Slayer.cSlayer.stats['total_letality_per_' + i]*100)}**%"
            if int(Slayer.cSlayer.stats['total_parry_' + i]*100) != 0:
                description += f"\n✊ Blocage : **{int(Slayer.cSlayer.stats['total_parry_' + i]*100)}**%"
            embed.add_field(name=name, value=description, inline=False)

    embed.set_thumbnail(url=avatar)
    embed.set_footer(text=f'Chasse depuis le {lib.datetime.datetime.fromtimestamp(Slayer.cSlayer.creation_date).strftime("%d/%m/%Y")}')
    return embed

def create_embed_achievement(Slayer, avatar):

    description = \
    f"🎖️ Monstres tués : **{Slayer.cSlayer.achievements['monsters_killed']}**" \
    f"\n🏆 Meilleur attaque : **{Slayer.cSlayer.achievements['biggest_hit']}**"

    embed=lib.discord.Embed(title=f"Prouesses de {Slayer.cSlayer.name}",
    description=description,
    color=0x1abc9c)   

    embed.set_thumbnail(url=avatar)
    embed.set_footer(text=f'Chasse depuis le {lib.datetime.datetime.fromtimestamp(Slayer.cSlayer.creation_date).strftime("%d/%m/%Y")}')
    return embed

def create_embed_equipment(bot, Slayer, avatar):
    description = f"Score d'équipement : **{int(Slayer.cSlayer.gearscore)}**\n"
    for slot in Slayer.cSlayer.slots_count:
        if Slayer.cSlayer.slots_count[slot]['activated']:
            if Slayer.cSlayer.slots_count[slot]['count'] > 0:
                if slot in Slayer.cSlayer.slots: nbr = len(Slayer.cSlayer.slots[slot])
                else: nbr = 0
                description += f"\n**{Slayer.cSlayer.slots_count[slot]['display_emote']} {Slayer.cSlayer.slots_count[slot]['display_text']}** - ({nbr}/{Slayer.cSlayer.slots_count[slot]['count']})"
                if slot in Slayer.cSlayer.slots:
                    for item in Slayer.cSlayer.slots[slot]:
                        cItem = Slayer.cSlayer.inventory_items[item]
                        if cItem.level > 1:
                            description += f"\n- {bot.Elements[cItem.element].display_emote} [{cItem.level}] {cItem.name} - *{bot.Rarities[cItem.rarity].display_text}*"
                        else:
                            description += f"\n- {bot.Elements[cItem.element].display_emote} {cItem.name} - *{bot.Rarities[cItem.rarity].display_text}*"

    embed=lib.discord.Embed(title=f"Équipement de {Slayer.cSlayer.name}",
    description=description,
    color=0x1abc9c)   

    embed.set_thumbnail(url=avatar)
    embed.set_footer(text=f'Chasse depuis le {lib.datetime.datetime.fromtimestamp(Slayer.cSlayer.creation_date).strftime("%d/%m/%Y")}')
    return embed

def create_embed_spe(Slayer, cSpe):
    embed=lib.discord.Embed(title=f"{cSpe.emote} {cSpe.name}",
    description= \
        f"{cSpe.description}\n" \
        f"```ansi\n⚔️Dégâts: {cSpe.damage}```" \
        f"```ansi\n☄️Charges: {cSpe.stacks}```" \
        f"\n\n__Statistiques :__"
        f"{cSpe.getDisplayStats()}" \
        f"\n**Actuellement équipé :**" \
        f"\n{Slayer.cSlayer.Spe.emote} {Slayer.cSlayer.Spe.name}",
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
        for cItem in recap_loot['items']:
            description += f"\n- {bot.Elements[cItem.element].display_emote} {cItem.name} (*{bot.rSlots[cItem.slot]['display_text']} {bot.Rarities[cItem.rarity].display_text}*)"

    embed=lib.discord.Embed(title=f"Récapitulatif Butin :",
    description=description,
    color=0xe74c3c
    )        
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1000070083915304991/1034553474999922848/unknown.png?width=1022&height=1022")
    return embed        

def create_embed_new_pet(bot, Slayer, cPet):
    #Setup Description
    description = \
        f"*{bot.Elements[cPet.element].display_emote} {bot.rSlots[cPet.slot]['display_text']} {bot.Rarities[cPet.rarity].display_text}*" \
        f"\n\n{cPet.description}"

    description += \
        f"\n\nOH OH ! Que voilà ?"

    embed=lib.discord.Embed(title=f"{cPet.name}",
    description= \
        f"{description}",
    color=int(bot.Rarities[cPet.rarity].display_color, 16)
    )

    embed.set_thumbnail(url=cPet.img_url)

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

def create_embed_gatherables_profil(Slayer, avatar, bot):

    description = ""
    for gatherable_id in Slayer.cSlayer.inventory_gatherables:
        if int(Slayer.cSlayer.inventory_gatherables[gatherable_id]) > 0:
            description += f"\n- {bot.Gatherables[gatherable_id].display_emote} {bot.Gatherables[gatherable_id].name} : {Slayer.cSlayer.inventory_gatherables[gatherable_id]}"

    embed=lib.discord.Embed(title=f"Ressources de {Slayer.cSlayer.name}",
    description=description,
    color=0x1abc9c)   

    embed.set_thumbnail(url=avatar)
    embed.set_footer(text=f'Chasse depuis le {lib.datetime.datetime.fromtimestamp(Slayer.cSlayer.creation_date).strftime("%d/%m/%Y")}')
    return embed

def create_embed_enhancement_pet(Slayer, pet_list, index, bot):
    if pet_list == []:   
        embed=lib.discord.Embed(title=f"Pas d'améliorations",
        description="Vous ne possédez pas de familiers améliorables.",
        color=0x1abc9c)   
        #embed.set_thumbnail(url=avatar)
    else:
        description = pet_list[index].description
        description += "\n"
        description += pet_list[index].getDisplayStats()

        description += "\n\n**__Nourriture :__**"
        description += f"\n{bot.PetFood[pet_list[index].id].display_emote} {bot.PetFood[pet_list[index].id].name} - **{Slayer.cSlayer.inventory_gatherables[bot.PetFood[pet_list[index].id].id]}/{100-pet_list[index].level}** requis pour atteindre le nv. max."

        embed=lib.discord.Embed(title=f"{pet_list[index].name} - Niveau : {pet_list[index].level}",
        description=description,
        color=0x1abc9c)   

        embed.set_thumbnail(url=pet_list[index].img_url)
    return embed

def create_embed_enhancement_mythic(Slayer, mythic_list, index, bot):
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
        description += f"\n{bot.Gatherables[5].display_emote} {bot.Gatherables[5].name} - **{Slayer.cSlayer.inventory_gatherables[5]}** disponibles."

        embed=lib.discord.Embed(title=f"{mythic_list[index].name} - Niveau : {mythic_list[index].level}",
        description=description,
        color=0x1abc9c)   

        embed.set_thumbnail(url=mythic_list[index].img_url)
    return embed