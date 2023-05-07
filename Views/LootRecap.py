import lib

class Details_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Détails", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if interaction.user.id in self.view.Battle.loots:
            embed = lib.Embed.create_embed_recap_loot(self.view.bot, self.view.Battle.loots[interaction.user.id])
            Slayer = await self.view.bot.ActiveList.get_Slayer(interaction.user.id, interaction.user.name)

            if self.view.Battle.loots[interaction.user.id].get("items", []) != []:
                view=lib.LootReviewView(self.view.bot, self.view.Battle.loots[interaction.user.id], Slayer, interaction)
                await self.view.bot.ActiveList.add_interface(interaction.user.id, "LootReview", view)
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            else:    
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(content="Vous n'avez malheureusement rien reçu lors de ce combat.", ephemeral=True)

class LootRecapView(lib.discord.ui.View):
    def __init__(self, Battle):
        super().__init__(timeout=600)
        self.bot = Battle.bot
        self.Battle = Battle

        # Adds the dropdown to our view object.
        self.add_item(Details_Button())

    async def end_view(self, poweroff=False):
        await self.message.edit(view=None)
        if not poweroff:
            #On remove le combat de la liste
            self.bot.ActiveList.remove_recap(self.message.id)
        self.stop()

    async def on_timeout(self) -> None:
        await self.end_view()