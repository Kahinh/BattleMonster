import lib

def create_embed_spawn(monster_class):
    embed=lib.discord.Embed(title=f"{monster_class.name} ({'{:,}'.format(monster_class.base_hp).replace(',', ' ')}/{'{:,}'.format(monster_class.total_hp).replace(',', ' ')} ❤️)",
    description= \
        f"**Monstre {lib.PostgreSQL.Rarities_list[monster_class.rarity]['display_text'].capitalize()}**\n" \
        f"⚔️ Puissance : **{monster_class.damage}** {lib.PostgreSQL.Elements_list[monster_class.element]['display_emote']}\n" \
        f"🛡️ Armure : **{monster_class.armor}**\n" \
        f"🎲 Butin Disponible : **{monster_class.roll_dices}**\n\n" \
        f"{monster_class.description}", \
    color=lib.PostgreSQL.Rarities_list[monster_class.rarity]['display_color']
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

def create_embed_loot(loot, isAlready):
    embed=lib.discord.Embed(title=f"{lib.PostgreSQL.Items_list[loot].name}",
    description= \
        f"{lib.PostgreSQL.Items_list[loot].description}",
    color=lib.PostgreSQL.Rarities_list[lib.PostgreSQL.Items_list[loot].rarity]['display_color']
    )
    if lib.PostgreSQL.Items_list[loot].img_url is not None:
        embed.set_thumbnail(url=f"{lib.PostgreSQL.Items_list[loot].img_url}")
    #embed.set_footer(text="")
    return embed