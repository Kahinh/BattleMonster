import lib

def create_embed_spawn(self, monster_class):

    Elements_list = self.BDD["Elements_list"]
    Rarities_list = self.BDD["Rarities_list"]

    embed=lib.discord.Embed(title=f"{monster_class.name} ({'{:,}'.format(monster_class.base_hp).replace(',', ' ')}/{'{:,}'.format(monster_class.total_hp).replace(',', ' ')} ❤️)",
    description= \
        f"**Monstre {Rarities_list[monster_class.rarity]['display_text'].capitalize()}**\n" \
        f"⚔️ Puissance : **{monster_class.damage}** {Elements_list[monster_class.element]['display_emote']}\n" \
        f"🛡️ Armure : **{monster_class.armor}**\n" \
        f"🎲 Butin Disponible : **{monster_class.roll_dices}**\n\n" \
        f"{monster_class.description}", \
    color=Rarities_list[monster_class.rarity]['display_color']
    )
    embed.add_field(name="Statistiques Avancées", \
        value= \
            f"✊ Chance de blocage - Attaque Légère : **{monster_class.parry['parry_chance_L'] * 100}%**\n" \
            f"✊ Chance de blocage - Attaque Lourde : **{monster_class.parry['parry_chance_H'] * 100}%**\n" \
            f"🗡️ Létalité : **({monster_class.letality}, {monster_class.letality_per *100}%)**\n" \
            f"💠 Résistance Critique : **{monster_class.protect_crit}**\n", \
        inline=False)
    if monster_class.img_url_normal is not None:
        embed.set_thumbnail(url=f"{monster_class.img_url_normal}")
    if monster_class.bg_url is not None:
        embed.set_image(url=f"{monster_class.bg_url}")
    #embed.set_footer(text="")
    return embed

def create_embed_loot(self, loot, isAlready):

    Items_list = self.BDD["Items_list"]
    Rarities_list = self.BDD["Rarities_list"]
    loot_price = Rarities_list[Items_list[loot].rarity]["price"]

    Description = "Félicitations ! Vous avez obtenu un butin !" \
        f"\n{Items_list[loot].description}"
    #Setup Description
    if isAlready:
        Description += f"\n\nMalheureusement, tu possèdes déjà cet objet. Il a donc été vendu pour **{loot_price}** 🪙."
    else:
        Description += "\n\nQue souhaites-tu faire désormais ? L'équiper ? Le vendre ? Le laisser dans ton inventaire ?"


    embed=lib.discord.Embed(title=f"{Items_list[loot].name}",
    description= \
        f"{Description}",
    color=Rarities_list[Items_list[loot].rarity]['display_color']
    )

    if Items_list[loot].img_url is not None:
        embed.set_thumbnail(url=f"{Items_list[loot].img_url}")
    #embed.set_footer(text="")
    return embed