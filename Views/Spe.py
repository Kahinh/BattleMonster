import lib

class Spe_Dropdown(lib.discord.ui.Select):
    def __init__(self, rSpes):
        options = []
        for spe in rSpes:
            options.append(lib.discord.SelectOption(label=spe["name"], value=spe["id"], emoji=spe["display_emote"]))
        super().__init__(placeholder="Filtrer la spécialité...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        self.view.current_spe_id = int(self.values[0])
        await self.view.update_view(interaction)

class Equip_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équiper", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        self.view.Slayer.cSlayer.special_stacks = 0
        self.view.Slayer.cSlayer.specialization = int(self.view.current_spe_id)
        self.view.Slayer.rSpe = lib.Toolbox.get_spe_row_by_id(self.view.bot.rSpe, self.view.current_spe_id)
        await self.view.bot.dB.push_slayer_data(self.view.Slayer.cSlayer)
        await self.view.Slayer.updateSlayer()

        await self.view.update_view()
        await interaction.response.send_message(content="La spécialité a bien été équipée !", ephemeral=True) 

class Buy_Button(lib.discord.ui.Button):
    def __init__(self, price):
        self.price = price
        super().__init__(label=f"{price} 🪙", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        self.view.Slayer.cSlayer.inventory_specializations.append(self.view.current_spe_id)
        self.view.Slayer.removeMoney(self.price)

        await self.view.bot.dB.push_slayer_data(self.view.Slayer.cSlayer)
        await self.view.bot.dB.push_spe_list(self.view.Slayer.cSlayer)
        await self.view.update_view()

        await interaction.response.send_message(content="La spécialité a bien été achetée !", ephemeral=True) 

class SpeView(lib.discord.ui.View):
    def __init__(self, bot, Slayer, interaction):
        super().__init__(timeout=120)
        self.bot = bot
        self.Slayer = Slayer
        self.interaction = interaction
        self.current_spe_id = 1

        self.add_item(Spe_Dropdown(list(self.bot.rSpe)))
        if 1 != self.Slayer.cSlayer.specialization:
            self.add_item(Equip_Button())

    async def update_view(self, interaction=None):
        spe_row = lib.Toolbox.get_spe_row_by_id(self.bot.rSpe, self.current_spe_id)
        embed = lib.Embed.create_embed_spe(self.Slayer, spe_row)
        await self.update_buttons(spe_row)
        view = self  
        if interaction is None:
            message = await self.interaction.original_response()
            await message.edit(embed=embed, view=view)
        else:
            await interaction.response.edit_message(embed=embed, view=view) 

    async def update_buttons(self, spe_row):
        self.clear_items()
        self.add_item(Spe_Dropdown(list(self.bot.rSpe)))
        if int(spe_row["id"]) not in self.Slayer.cSlayer.inventory_specializations:
            self.add_item(Buy_Button(spe_row["cost"]))
        else:
            if spe_row["id"] != self.Slayer.cSlayer.specialization:
                self.add_item(Equip_Button())


    async def close_view(self):
        self.bot.ActiveList.remove_interface(self.Slayer.cSlayer.slayer_id, "inventaire_spe")
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
