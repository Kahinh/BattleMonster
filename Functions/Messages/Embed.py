import lib

def create_embed_spawn(self):

    embed=lib.discord.Embed(title=f"{self.Monsters[self.count].name} ({'{:,}'.format(self.Monsters[self.count].base_hp).replace(',', ' ')}/{'{:,}'.format(self.Monsters[self.count].total_hp).replace(',', ' ')} ❤️)",
    description= \
        f"**Monstre {self.bot.rRarities[self.Monsters[self.count].rarity]['display_text'].capitalize()}**\n" \
        f"⚔️ Puissance : **{self.Monsters[self.count].damage}** {self.bot.rElements[self.Monsters[self.count].element]['display_emote']}\n" \
        f"🛡️ Armure : **{self.Monsters[self.count].armor}**\n" \
        f"🎲 Butin Disponible : **{self.Monsters[self.count].roll_dices}**\n\n" \
        f"{self.Monsters[self.count].description}", \
    color=int(self.bot.rRarities[self.Monsters[self.count].rarity]['display_color'], 16)
    )
    embed.add_field(name="Statistiques Avancées", \
        value= \
            f"✊ Chance de blocage - Attaque Légère : **{self.Monsters[self.count].parry['parry_chance_L'] * 100}%**\n" \
            f"✊ Chance de blocage - Attaque Lourde : **{self.Monsters[self.count].parry['parry_chance_H'] * 100}%**\n" \
            f"🗡️ Létalité : **({self.Monsters[self.count].letality}, {self.Monsters[self.count].letality_per *100}%)**\n" \
            f"💠 Résistance Critique : **{self.Monsters[self.count].protect_crit}**\n", \
        inline=False)
    if self.Monsters[self.count].img_url_normal is not None:
        embed.set_thumbnail(url=f"{self.Monsters[self.count].img_url_normal}")
    if self.Monsters[self.count].bg_url is not None:
        embed.set_image(url=f"{self.Monsters[self.count].bg_url}")
    embed.set_footer(text=f"Apparition : {self.count+1}/{self.spawns_count}")
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