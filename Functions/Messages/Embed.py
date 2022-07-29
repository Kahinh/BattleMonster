import lib

def create_embed_spawn(self, cMonster, rElement, rRarity):

    element_emote = rElement["display_emote"]
    rarity_color = rRarity["display_color"]
    rarity_text = rRarity["display_text"]

    embed=lib.discord.Embed(title=f"{cMonster.name} ({'{:,}'.format(cMonster.base_hp).replace(',', ' ')}/{'{:,}'.format(cMonster.total_hp).replace(',', ' ')} ❤️)",
    description= \
        f"**Monstre {rarity_text.capitalize()}**\n" \
        f"⚔️ Puissance : **{cMonster.damage}** {element_emote}\n" \
        f"🛡️ Armure : **{cMonster.armor}**\n" \
        f"🎲 Butin Disponible : **{cMonster.roll_dices}**\n\n" \
        f"{cMonster.description}", \
    color=int(rarity_color, 16)
    )
    embed.add_field(name="Statistiques Avancées", \
        value= \
            f"✊ Chance de blocage - Attaque Légère : **{cMonster.parry['parry_chance_L'] * 100}%**\n" \
            f"✊ Chance de blocage - Attaque Lourde : **{cMonster.parry['parry_chance_H'] * 100}%**\n" \
            f"🗡️ Létalité : **({cMonster.letality}, {cMonster.letality_per *100}%)**\n" \
            f"💠 Résistance Critique : **{cMonster.protect_crit}**\n", \
        inline=False)
    if cMonster.img_url_normal is not None:
        embed.set_thumbnail(url=f"{cMonster.img_url_normal}")
    if cMonster.bg_url is not None:
        embed.set_image(url=f"{cMonster.bg_url}")
    #embed.set_footer(text="")
    return embed

def create_embed_loot(self, loot, isAlready, rPrice, rRarity):

    rarity_color = rRarity["display_color"]

    #loot_price = Rarities[Items[loot].rarity]["price"]
    loot_description = loot["description"]
    loot_name = loot["name"]
    loot_img_url = loot["img_url"]

    Description = "Félicitations ! Vous avez obtenu un butin !" \
        f"\n{loot_description}"
    #Setup Description
    if isAlready:
        Description += f"\n\nMalheureusement, tu possèdes déjà cet objet. Il a donc été vendu pour **{rPrice}** 🪙."
    else:
        Description += f"\n\nQue souhaites-tu faire désormais ? L'équiper ? Le vendre pour {rPrice} 🪙? Le laisser dans ton inventaire ?"


    embed=lib.discord.Embed(title=f"{loot_name}",
    description= \
        f"{Description}",
    color=int(rarity_color, 16)
    )

    if loot_img_url is not None:
        embed.set_thumbnail(url=f"{loot_img_url}")
    #embed.set_footer(text="")
    return embed