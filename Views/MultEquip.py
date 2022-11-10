import lib

class Equiped_Dropdown(lib.discord.ui.Select):
    def __init__(self, List):
        options = []
        for item in List:
            options.append(lib.discord.SelectOption(label=f"{item.rarity} {item.element} - {item.name}", value=item.item_id))
        super().__init__(placeholder='Objet à remplacer...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if not self.view.obsolete:
            try:
                self.view.Slayer.cSlayer.inventory_items[int(self.values[0])].unequip()
                self.view.cItem.equip()
                await self.view.Slayer.updateSlayer()
                await self.view.bot.dB.switch_item(self.view.Slayer.cSlayer, self.view.cItem, self.view.Slayer.cSlayer.inventory_items[int(self.values[0])])

                #On update le Inventoryview ?
                await self.view.bot.ActiveList.update_interface(self.view.Slayer.cSlayer.id, "inventaire")
                await self.view.bot.ActiveList.update_interface(self.view.Slayer.cSlayer.id, "LootReview")

                self.view.bot.ActiveList.remove_interface(self.view.Slayer.cSlayer.id, "mult_equip")
                message = await self.view.interaction.original_response()
                await message.edit(view=None)
                self.view.stop()
                
                self.view.Slayer.cSlayer.calculateStats(self.view.bot.rBaseBonuses)
                await self.view.bot.ActiveList.close_interface(self.view.Slayer.cSlayer.id, self.view.cItem.item_id)
                await interaction.followup.send(content="L'objet a été équipé !", ephemeral=True) 
            except:
                await interaction.followup.send("Une erreur s'est produite !", ephemeral=True)
        else:
            await interaction.followup.send(content="Cette interface est obsolete. Il te faut la redémarrer !")

class MultEquipView(lib.discord.ui.View):
    def __init__(self, bot, Slayer, List, interaction, cItem):
        super().__init__(timeout=60)
        self.bot = bot
        self.Slayer = Slayer
        self.interaction = interaction
        self.cItem = cItem
        self.List = []
        self.obsolete = False

        for item in List: 
            self.List.append(self.Slayer.cSlayer.inventory_items[item])

        self.add_item(Equiped_Dropdown(self.List))

    async def close_view(self):
        self.bot.ActiveList.remove_interface(self.Slayer.cSlayer.id, "mult_equip")
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
