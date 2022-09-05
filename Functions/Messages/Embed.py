import lib

def create_embed_battle(self):

    embed=lib.discord.Embed(title=f"{self.Monsters[self.count].name} ({'{:,}'.format(int(self.Monsters[self.count].base_hp)).replace(',', ' ')}/{'{:,}'.format(int(self.Monsters[self.count].total_hp)).replace(',', ' ')} ❤️)",
    description= \
        f"**Monstre {self.bot.rRarities[self.Monsters[self.count].rarity]['display_text'].capitalize()}**\n" \
        f"⚔️ Puissance : **{int(self.Monsters[self.count].damage)}** {self.bot.rElements[self.Monsters[self.count].element]['display_emote']}\n" \
        f"🛡️ Armure : **{int(self.Monsters[self.count].armor)}**\n" \
        f"🎲 Butin Disponible : **{self.Monsters[self.count].roll_dices}**\n\n" \
        f"{self.Monsters[self.count].description}", \
    color=int(self.bot.rRarities[self.Monsters[self.count].rarity]['display_color'], 16)
    )
    embed.add_field(name="Statistiques Avancées", \
        value= \
            f"✊ Chance de blocage - Attaque Légère : **{self.Monsters[self.count].parry['parry_chance_L'] * 100}%**\n" \
            f"✊ Chance de blocage - Attaque Lourde : **{self.Monsters[self.count].parry['parry_chance_H'] * 100}%**\n" \
            f"🗡️ Létalité : **({int(self.Monsters[self.count].letality)}, {self.Monsters[self.count].letality_per *100}%)**\n" \
            f"💠 Résistance Critique : **{self.Monsters[self.count].protect_crit}**\n", \
        inline=False)
    if self.Monsters[self.count].img_url_normal is not None:
        embed.set_thumbnail(url=f"{self.Monsters[self.count].img_url_normal}")
    if self.Monsters[self.count].bg_url is not None:
        embed.set_image(url=f"{self.Monsters[self.count].bg_url}")
    if self.spawns_count > 1:   
        embed.set_footer(text=f"Monstre : {self.count+1}/{self.spawns_count}")
    return embed

def create_embed_end_battle(Battle, End):
    #TITLE
    if End == True:
        title = "**Combat achevé ✨ Tous les monstres ont été vaincus !**"
    else: 
        title = "**Combat achevé : 🐉 Vous avez échoué et les monstres se sont enfuis.**"
    
    description = "**Bilan du combat :**"
    for i in Battle.Monsters:
        if int(Battle.Monsters[i].base_hp) == 0:
            description += f"\n- {i + 1} {Battle.bot.rElements[Battle.Monsters[i].element]['display_emote']} {Battle.Monsters[i].name} ({int(Battle.Monsters[i].base_hp)}/{int(Battle.Monsters[i].total_hp)} 💀)"
        else:
            description += f"\n- {i + 1} {Battle.bot.rElements[Battle.Monsters[i].element]['display_emote']} {Battle.Monsters[i].name} ({int(Battle.Monsters[i].base_hp)}/{int(Battle.Monsters[i].total_hp)} ❤️)"
    
    description += f"\n\n⚔️ Attaques infligées : {Battle.stats['attacks']}"
    description += f"\n🩸 Dégâts reçus : {Battle.stats['damage']}"
    description += f"\n💀 Slayers morts : {Battle.stats['kills']}"
    description += f"\n🎁 Butins récupérés : {Battle.stats['loots']}"
    embed=lib.discord.Embed(title=title, description=description, color=0x2ecc71 if End else 0xe74c3c)
    embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/K5FrBGB9d-8IbCg_bnZyheglS9Q61aXohV4hJSMiImA/%3Fcb%3D20200801054948/https/static.wikia.nocookie.net/dauntless_gamepedia_en/images/1/13/Hunt_Icon.png/revision/latest')
    return embed

def create_embed_new_loot():

    Description = "Félicitations ! Vous avez obtenu un butin !"
    #Setup Description
    Description += f"\n\nQue souhaites-tu faire désormais ? L'équiper ? Le vendre pour 10 🪙? Le laisser dans ton inventaire ?"


    embed=lib.discord.Embed(title=f"NEW LOOT",
    description= \
        f"{Description}",
    #color=int(rarity_color, 16)
    )

    #embed.set_footer(text="")
    return embed

def create_embed_money_loot(bot, Slayer, cItem, Price):

    #Setup Description
    description = \
        f"*{bot.rElements[cItem.element]['display_emote']} {bot.rSlots[cItem.slot]['display_text']} {bot.rRarities[cItem.rarity]['display_text']}*" \
        f"\n\n{cItem.description}" \
        f"\n\nVous possédez déjà ce casque ! Il a dont été vendu pour **10 🪙**"

    embed=lib.discord.Embed(title=f"{cItem.name}",
    description=description,
    color=int(bot.rRarities[cItem.rarity]["display_color"], 16)
    )

    embed.set_thumbnail(url=cItem.img_url)

    return embed

def create_embed_item(bot, cItem1, cItem2=None):
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

        description = f"__Description :__\n{cItem1.description}"

        if cItem2 is not None:
            description += f"\n\n__Objet équipé à cet emplacement :__\n{bot.rElements[cItem2.element]['display_emote']} {cItem2.name} ({cItem2.slot} / {bot.rRarities[cItem2.rarity]['display_text']})"

        description += f"\n\n__Statistiques :__{desc_stat}"
        
        embed=lib.discord.Embed(title=f"{bot.rElements[cItem1.element]['display_emote']} {cItem1.name} ({cItem1.slot} / {bot.rRarities[cItem1.rarity]['display_text']})",
        description= \
            f"{description}",
        color=int(bot.rRarities[cItem1.rarity]['display_color'], 16)
        )

        embed.set_thumbnail(url=f"{cItem1.img_url}")
    return embed

def create_embed_profil(Slayer, avatar):

    description = \
    f"**📯 {Slayer.cSlayer.Spe.name}**" \
    "\n\n**__Statistiques__**" \
    f"\n❤️ Vie : **{Slayer.cSlayer.stats['total_max_health'] - Slayer.cSlayer.damage_taken}/{Slayer.cSlayer.stats['total_max_health']}**" \
    f"\n🛡️ Armure : **{Slayer.cSlayer.stats['total_armor']}**" \
    f"\n🌪️ Vivacité : **{Slayer.cSlayer.stats['total_cooldown']}s**" \
    f"\n☄️ Charge : **{Slayer.cSlayer.special_stacks}/{Slayer.cSlayer.stats['total_stacks']}**" \
    f"\n🍀 Luck : **{Slayer.cSlayer.stats['total_luck'] * 100}**%"

    embed=lib.discord.Embed(title=f"Profil de {Slayer.cSlayer.name}",
    description=description,
    color=0x1abc9c)   

    for i in ("L", "H", "S"):
        if i == "L":
            name = "__Attaque Légère__"
        elif i == "H":
            name = "__Attaque Lourde__"
        elif i == "S":
            name = "__Capacité Spéciale__"
        description = \
        f"\n⚔️ Puissance : **{Slayer.cSlayer.stats['total_damage_' + i]}**" \
        f"\n⚔️ Dégâts Finaux : **{Slayer.cSlayer.stats['total_final_damage_' + i]*100}**" \
        f"\n☄️ Gains Charge : **{Slayer.cSlayer.stats['total_special_charge_' + i]}**" \
        f"\n✨ Chance Critique : **{Slayer.cSlayer.stats['total_crit_chance_' + i]*100}**%" \
        f"\n💢 Dégâts Critiques : **{Slayer.cSlayer.stats['total_crit_damage_' + i]*100}**%" \
        f"\n🗡️ Létalité : **{Slayer.cSlayer.stats['total_letality_' + i]}**,  **{Slayer.cSlayer.stats['total_letality_per_' + i]*100}**%" \
        f"\n🎯 Echec : **{Slayer.cSlayer.stats['total_fail_' + i]*100}**%" \
        f"\n✊ Blocage : **{Slayer.cSlayer.stats['total_parry_' + i]*100}**"
        embed.add_field(name=name, value=description, inline=False)

    embed.set_thumbnail(url=avatar)
    embed.set_footer(text=f'Chasse depuis le {Slayer.cSlayer.creation_date}')
    return embed

def create_embed_equipment(bot, Slayer, avatar):
    description = f"Score d'équipement : **{Slayer.cSlayer.gearscore}**\n"
    for slot in Slayer.cSlayer.slots_count:
        if slot in Slayer.cSlayer.slots: nbr = len(Slayer.cSlayer.slots[slot])
        else: nbr = 0
        description += f"\n**{Slayer.cSlayer.slots_count[slot]['display_emote']} {Slayer.cSlayer.slots_count[slot]['display_text']}** - ({nbr}/{Slayer.cSlayer.slots_count[slot]['count']})"
        if slot in Slayer.cSlayer.slots:
            for item in Slayer.cSlayer.slots[slot]:
                cItem = Slayer.cSlayer.inventory_items[item]
                if cItem.level > 1:
                    description += f"\n- {bot.rElements[cItem.element]['display_emote']} [{cItem.level}] {cItem.name} - *{bot.rRarities[cItem.rarity]['display_text']}*"
                else:
                    description += f"\n- {bot.rElements[cItem.element]['display_emote']} {cItem.name} - *{bot.rRarities[cItem.rarity]['display_text']}*"

    embed=lib.discord.Embed(title=f"Équipement de {Slayer.cSlayer.name}",
    description=description,
    color=0x1abc9c)   

    embed.set_thumbnail(url=avatar)
    embed.set_footer(text=f'Chasse depuis le {Slayer.cSlayer.creation_date}')
    return embed