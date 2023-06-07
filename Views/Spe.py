import lib

class Spe_Dropdown(lib.discord.ui.Select):
    def __init__(self, Specializations):
        options = []
        for cSpe in list(Specializations.values()):
            options.append(lib.discord.SelectOption(label=cSpe.name, value=cSpe.id, emoji=cSpe.emote))
        super().__init__(placeholder="Filtrer la spécialité...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.current_spe_id = int(self.values[0])
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Equip_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équiper", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            # self.view.cSlayer.mult_damage = 0
            # self.view.cSlayer.berserker_mode = 0
            await self.view.cSlayer.set_specialization(self.view.current_spe_id)
            await self.view.update_view(interaction)
            await interaction.followup.send(content="La spécialité a bien été équipée !", ephemeral=True) 
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Buy_Button(lib.discord.ui.Button):
    def __init__(self, price):
        self.price = price
        super().__init__(label=f"{price} 🪙", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            if is_moneyspent := await self.view.cSlayer.add_remove_money(self.price):
                await self.view.cSlayer.set_inventory_specializations(int(self.view.current_spe_id))
                await self.view.update_view(interaction)
                await interaction.followup.send(content="La spécialité a bien été achetée !", ephemeral=True) 
            else:
                await interaction.response.send_message(content="Malheureusement, tu ne possèdes pas suffisament de 🪙 !", ephemeral=True)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class SpeView(lib.discord.ui.View):
    def __init__(self, bot, cSlayer, interaction):
        super().__init__(timeout=120)
        self.bot = bot
        self.cSlayer = cSlayer
        self.interaction = interaction
        self.current_spe_id = 1
        self.obsolete = False

        self.add_item(Spe_Dropdown(self.bot.Specializations))
        if 1 != self.cSlayer.cSpe.id:
            self.add_item(Equip_Button())

    async def update_view(self, interaction=None):
        cSpe = self.bot.Specializations[self.current_spe_id]
        embed = lib.Embed.create_embed_spe(self.cSlayer, cSpe)
        await self.update_buttons(cSpe)
        view = self  
        if interaction is None:
            message = await self.interaction.original_response()
            await message.edit(embed=embed, view=view)
        else:
            await interaction.response.edit_message(embed=embed, view=view) 

    async def update_buttons(self, cSpe):
        self.clear_items()
        self.add_item(Spe_Dropdown(self.bot.Specializations))
        if int(cSpe.id) not in self.cSlayer.inventories["specializations"]:
            self.add_item(Buy_Button(cSpe.cost))
        else:
            if cSpe.id != self.cSlayer.cSpe.id:
                self.add_item(Equip_Button())

    async def close_view(self):
        self.bot.ActiveList.remove_interface(self.cSlayer.id, "inventaire_spe")
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
