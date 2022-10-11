import lib

class Details_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Détails", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        embed = lib.Embed.create_embed_item(self.view.bot, self.view.cItem, self.view.Slayer)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class Equip_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équiper", style=lib.discord.ButtonStyle.green)
        
    async def callback(self, interaction: lib.discord.Interaction):
        if self.view.Slayer.cSlayer.slayer_id == interaction.user.id:
            #On call la fonction
            Slayer = await self.view.bot.ActiveList.get_Slayer(interaction.user.id, "")
            isEquipped, List = await Slayer.equip_item(self.view.cItem)

            if isEquipped:
                #On update le Inventoryview ?
                await self.view.bot.ActiveList.update_interface(self.view.Slayer.cSlayer.slayer_id, "inventaire")
                await interaction.response.send_message(content="L'objet a été équipé !", ephemeral=True) 
            else:
                if len(List) == 0:
                    await interaction.response.send_message(content="Une erreur est survenue !", ephemeral=True)
                else:
                    viewMult = lib.MultEquipView(self.view.bot, self.view.Slayer, List, interaction, self.view.cItem)
                    await self.view.bot.ActiveList.add_interface(interaction.user.id, "mult_equip", viewMult)
                    await interaction.response.send_message(content="Tous les emplacements sont déjà utilisés, quel objet souhaitez-vous remplacer ?", view=viewMult, ephemeral=True)
        
        else:
            await interaction.response.send_message("Ce n'est pas ton butin !", ephemeral=True)

class Sell_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Vendre", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        if self.view.Slayer.cSlayer.slayer_id == interaction.user.id:

            #On call la fonction
            Slayer = await self.view.bot.ActiveList.get_Slayer(interaction.user.id, "")
            Sold = await Slayer.sell_item(self.view.cItem)
            await self.view.bot.ActiveList.update_interface(self.view.Slayer.cSlayer.slayer_id, "inventaire")

            if Sold:
                await interaction.response.send_message("L'objet a été vendu !", ephemeral=True)
            else:
                await interaction.response.send_message("Une erreur s'est produite !", ephemeral=True)
            
        else:
            await interaction.response.send_message("Ce n'est pas ton butin !", ephemeral=True)

class LootView(lib.discord.ui.View):
    def __init__(self, bot, Slayer, cItem, isLoot=False):
        super().__init__(timeout=600)
        self.bot = bot
        self.Slayer = Slayer
        self.cItem = cItem

        # Adds the dropdown to our view object.
        self.add_item(Details_Button())
        if isLoot:
            self.add_item(Equip_Button())
            self.add_item(Sell_Button())

    async def end_view(self):
        self.bot.ActiveList.remove_interface(self.Slayer.cSlayer.slayer_id, self.cItem.item_id)
        await self.message.edit(view=None)
        self.stop()

    async def close_view(self):
        #On désactive
        for item in self.children:
            if item.label=="Équiper" or item.label=="Vendre":
                item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        await self.end_view()