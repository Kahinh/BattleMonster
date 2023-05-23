import lib

class Light_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Attaque Légère", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        Slayer = await self.view.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
        content, damage, monster_killed = await self.view.Battle.handler_Attack(Slayer, "l")
        #On répond au joueur
        await interaction.followup.send(content=content, ephemeral=True)

        if self.view.Battle.stats["kills"] >= self.view.bot.Variables["battle_kills_before_escape"]:
            await self.view.updateBattle(timeout=True)
        elif damage != []:
            await self.view.updateBattle(monster_killed=monster_killed)

class Heavy_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Attaque Lourde", style=lib.discord.ButtonStyle.green)
        
    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        Slayer = await self.view.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
        content, damage, monster_killed = await self.view.Battle.handler_Attack(Slayer, "h")
        #On répond au joueur
        await interaction.followup.send(content=content, ephemeral=True)
        if self.view.Battle.stats["kills"] >= self.view.bot.Variables["battle_kills_before_escape"]:
            await self.view.updateBattle(timeout=True)
        elif damage != []:
            await self.view.updateBattle(monster_killed=monster_killed)

class Special_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Capacité Spéciale", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        Slayer = await self.view.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)
        content, damage, monster_killed = await self.view.Battle.handler_Attack(Slayer, "s")
        #On répond au joueur
        await interaction.followup.send(content=content, ephemeral=True)
        if self.view.Battle.stats["kills"] >= self.view.bot.Variables["battle_kills_before_escape"]:
            await self.view.updateBattle(timeout=True)
        elif damage != []:
            await self.view.updateBattle(monster_killed=monster_killed)
        

class BattleView(lib.discord.ui.View):
    def __init__(self, Battle):
        super().__init__(timeout=600)
        self.bot = Battle.bot
        self.Battle = Battle

        # Adds the dropdown to our view object.
        self.add_item(Light_Button())
        self.add_item(Heavy_Button())
        self.add_item(Special_Button())

    async def updateBattle(self, timeout=False, poweroff=False, monster_killed=False, auto_remove_battle=True):
        if self.Battle.endnotbeingpublished: #On contrôle qu'un joueur clic pas pendant qu'on calcule la mort du battle
            if hasattr(self, "message"): message = self.message
            #if hasattr(self, "interaction"): message = await self.interaction.original_response()
            if any([timeout, poweroff, self.Battle.end]):
                self.Battle.endnotbeingpublished = False #Si c'est fini alors on modifie direct le endnotbeingpublished
                if self.Battle.end or timeout:
                    if auto_remove_battle: self.Battle.bot.ActiveList.remove_battle(message.id)
                    if self.Battle.end and self.Battle.stats["attacks_received"] > 0: #On fait le loot que si le combat est vraiment fini, pas timeout
                        await self.Battle.handler_Loot()
                        await self.send_embed_end_battle(timeout)
                await self.clear_battle(message) #Whatever on clear
            else: #Si ce n'est pas fin, on update juste le embed
                await self.update_embed(message)

    async def clear_battle(self, message):
        await message.delete()
        self.stop()

    async def send_embed_end_battle(self, timeout):
        if self.Battle.type == "factionwar":
            embed = lib.Embed.create_embed_end_factionwar(self.Battle)
        else:
            embed = lib.Embed.create_embed_end_battle(self.Battle, timeout)
        if self.is_loot(): #Si on a du loot
            #Pas eu de loot
            view = lib.LootRecapView(self.Battle)
            content = self.get_content_looters()
        else:
            view = None
            content = ""
        channel = self.Battle.bot.get_channel(self.Battle.bot.rChannels["loots"])
        view.message = await channel.send(content=content, embed=embed, view=view)
        if view is not None:self.Battle.bot.ActiveList.add_recap(view.message.id, view)

    async def update_embed(self, message):
        embed = lib.Embed.create_embed_battle(self.Battle)
        view = self
        await message.edit(embed=embed, view=view)

    async def on_timeout(self) -> None:
        await self.updateBattle(True)
        self.stop()

    def is_loot(self):
        for items in [self.Battle.storage_loots[x]["items"] for x in self.Battle.storage_loots]:
            if items:
                return True
        for money in [self.Battle.storage_loots[x]["money"] for x in self.Battle.storage_loots]:
            if money:
                return True
        for mythic_stones in [self.Battle.storage_loots[x]["mythic_stones"] for x in self.Battle.storage_loots]:
            if mythic_stones:
                return True
        return False

    def get_content_looters(self):
        content = ""
        for id in self.Battle.storage_loots:
            if self.Battle.storage_loots[id]["items"]:
                content += f"<@{id}> "
        return content