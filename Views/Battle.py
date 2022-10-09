import lib

class Light_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Attaque Légère", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        content = await self.view.Battle.getAttack(interaction, "L")
        #On répond au joueur
        await interaction.response.send_message(content=content, ephemeral=True)
        await self.view.updateBattle()

class Heavy_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Attaque Lourde", style=lib.discord.ButtonStyle.green)
        
    async def callback(self, interaction: lib.discord.Interaction):
        content = await self.view.Battle.getAttack(interaction, "H")
        #On répond au joueur
        await interaction.response.send_message(content=content, ephemeral=True)
        await self.view.updateBattle()


class Special_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Capacité Spéciale", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        content = await self.view.Battle.getAttack(interaction, "S")
        #On répond au joueur
        await interaction.response.send_message(content=content, ephemeral=True)
        await self.view.updateBattle()
        

class BattleView(lib.discord.ui.View):
    def __init__(self, Battle):
        super().__init__(timeout=600)
        self.Battle = Battle

        # Adds the dropdown to our view object.
        self.add_item(Light_Button())
        self.add_item(Heavy_Button())
        self.add_item(Special_Button())

    async def updateBattle(self, timeout=False):
        if hasattr(self, "interaction"): message = await self.interaction.original_response()
        if hasattr(self, "message"): message = self.message
        if self.Battle.end or timeout:
            if self.Battle.end:
                await self.Battle.calculateLoot()
            embed = lib.Embed.create_embed_end_battle(self.Battle, timeout)
            view = None
        else:
            embed = lib.Embed.create_embed_battle(self.Battle)
            view = self
        await message.edit(embed=embed, view=view)
        if self.Battle.end or timeout:
            self.stop()

    async def on_timeout(self) -> None:
        await self.updateBattle(True)
        self.stop()