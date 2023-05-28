import lib

class Gather_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Récolter", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if self.view.stock > 0:

            if interaction.user.id not in self.view.Slayer_user:

                Slayer = await self.view.bot.ActiveList.get_Slayer(interaction.user.id, "")
                if Slayer.cSlayer.dead:
                    await interaction.followup.send("Tu es mort, tu ne peux pas récolter", ephemeral=True)
                else:
                    #On enregistre que le joueur a joué pour pas qu'il puisse utiliser à nouveau
                    self.view.Slayer_user.append(interaction.user.id)
                    nbr = int(self.view.bot.Variables["bonus_gatherables_default"])

                    #Si le pet équipé se nourrit de la bouffe, on fait +1
                    if "pet" in Slayer.cSlayer.slots:
                        if Slayer.cSlayer.slots["pet"] != []:
                            if int(self.view.bot.PetFood[Slayer.cSlayer.slots["pet"][0]].id) == int(self.view.cGather.gatherable_id):
                                nbr += int(self.view.bot.Variables["bonus_gatherables_in_pets"])

                    #Si on a la faction qui a l'affinité
                    if int(Slayer.cSlayer.faction) != 0:
                        if self.view.bot.Factions[int(Slayer.cSlayer.faction)].gatherable_affinity == self.view.cGather.type:
                            nbr += int(self.view.bot.Variables["bonus_gatherables_in_faction"])
                    
                    #On remove du stock, et on envoie les gatherables dans l'inventaire du slayer. 
                    self.view.stock -= nbr
                    embed = lib.Embed.create_embed_gatherables_gathered(self.view.cGather, nbr)
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    await Slayer.update_inventory_gatherables(self.view.cGather.gatherable_id, nbr)

                    #end view si le stock est fini
                    if self.view.stock == 0:
                        await self.view.end_view()
            
            else:
                await interaction.followup.send("Tu as déjà récolté ici !", ephemeral=True)

        else:
            await interaction.followup.send("Récolte épuisée !", ephemeral=True)

class GatherView(lib.discord.ui.View):
    def __init__(self, Gather):
        super().__init__(timeout=200)
        self.bot = Gather.bot
        self.cGather = Gather
        self.Slayer_user = []
        self.stock = Gather.stock

        # Adds the dropdown to our view object.
        self.add_item(Gather_Button())

    async def end_view(self, poweroff=False):
        await self.message.delete()
        if not poweroff:
            #On remove le combat de la liste
            self.bot.ActiveList.remove_gather(self.message.id)
        self.stop()

    async def on_timeout(self) -> None:
        await self.end_view()