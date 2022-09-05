import lib

class Details_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Détails", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        embed = lib.Embed.create_embed_item(self.view.bot, self.view.cItem)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class Equip_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équiper", style=lib.discord.ButtonStyle.green)
        
    async def callback(self, interaction: lib.discord.Interaction):
        if self.view.request['slayer-id'] == interaction.user.id:
            #On call la fonction
            
            #On désactive
            for item in self.view.children:
                if item.label=="Équiper" or item.label=="Vendre":
                    item.disabled = True
            await interaction.response.edit_message(view=self.view)
        else:
            await interaction.response.send_message("Ce n'est pas ton butin !", ephemeral=True)

class Sell_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Vendre", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        if self.view.request['slayer-id'] == interaction.user.id:
            #On init le Slayer
            if interaction.user.id in self.bot.active_cSlayer:
                Slayer = self.bot.active_cSlayer[interaction.user.id]["class"]
            else:
                Slayer = lib.MSlayer(self.view.bot, interaction)
                await Slayer.constructClass()
            Sold = await Slayer.sell_item(lib.Item(self.view.request["loot"]))

            #On désactive
            for item in self.view.children:
                if item.label=="Équiper" or item.label=="Vendre":
                    item.disabled = True
            await interaction.response.edit_message(view=self.view)
            if Sold:
                await interaction.followup.send("L'objet a été vendu !", ephemeral=True)
            else:
                await interaction.followup.send("Une erreur s'est produite !", ephemeral=True)
        else:
            await interaction.response.send_message("Ce n'est pas ton butin !", ephemeral=True)

class LootView(lib.discord.ui.View):
    def __init__(self, bot, cItem):
        super().__init__(timeout=10)
        self.bot = bot
        self.cItem = cItem

        # Adds the dropdown to our view object.
        self.add_item(Details_Button())
        #if request['already'] == False:
            #self.add_item(Equip_Button())
            #self.add_item(Sell_Button())

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)
        self.stop()