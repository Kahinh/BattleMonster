import lib

class Gather_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Récolter", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if self.view.stock > 0:

            if interaction.user.id not in self.view.Slayer_user:

                #On enregistre que le joueur a joué pour pas qu'il puisse utiliser à nouveau
                self.view.Slayer_user.append(interaction.user.id)

                nbr = 1
                self.view.stock -= nbr
                embed = lib.Embed.create_embed_gatherables_gathered(self.view.cGather, nbr)
                await interaction.followup.send(embed=embed, ephemeral=True)

                Slayer = await self.view.bot.ActiveList.get_Slayer(interaction.user.id, "")
                await Slayer.update_inventory_gatherables(self.view.cGather.gatherable_id, nbr)

                if self.view.stock == 0:
                    await self.view.end_view()
            
            else:
                await interaction.followup.send("Tu as déjà récolté ici !", ephemeral=True)

        else:
            await interaction.followup.send("Récolte épuisée !", ephemeral=True)

class GatherView(lib.discord.ui.View):
    def __init__(self, Gather):
        super().__init__(timeout=600)
        self.bot = Gather.bot
        self.cGather = Gather
        self.Slayer_user = []
        self.stock = Gather.stock

        # Adds the dropdown to our view object.
        self.add_item(Gather_Button())

    async def end_view(self, poweroff=False):
        await self.message.edit(view=None)
        if not poweroff:
            #On remove le combat de la liste
            self.bot.ActiveList.remove_gather(self.message.id)
        self.stop()

    async def on_timeout(self) -> None:
        await self.end_view()