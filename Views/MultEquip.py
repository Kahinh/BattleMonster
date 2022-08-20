import lib

class Equiped_Dropdown(lib.discord.ui.Select):
    def __init__(self, List):
        options = []
        for item in List:
            options.append(lib.discord.SelectOption(label=f"{item.rarity} {item.element} - {item.name}", value=item.item_id))
        super().__init__(placeholder='Objet à remplacer...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        self.view.Slayer.removefromSlots(self.view.Slayer.cSlayer.inventory_items[int(self.values[0])])
        self.view.Slayer.addtoSlots(self.view.cItem)

        await self.view.bot.dB.switch_item(self.view.Slayer.cSlayer, self.view.cItem, self.view.Slayer.cSlayer.inventory_items[int(self.values[0])])

        #On update le Inventoryview ?
        lib.Toolbox.disable_enable_InventoryView(self.view.InventoryView.children, self.view.InventoryView.items_list_filtered, self.view.InventoryView.index)
        view = self.view.InventoryView
        await self.view.message.edit(view=view)

        self.view.bot.ActiveList.close_interface(self.view.Slayer.cSlayer.slayer_id, "mult_equip")
        message = await self.view.interaction.original_message()
        await message.edit(view=None)
        self.view.stop()
        
        self.view.Slayer.cSlayer.calculateStats(self.view.bot.rBaseBonuses)
        await interaction.response.send_message(content="L'objet a été équipé !", ephemeral=True) 

class MultEquipView(lib.discord.ui.View):
    def __init__(self, InventoryView, List, interaction, cItem, message):
        super().__init__(timeout=60)
        self.InventoryView = InventoryView
        self.bot = InventoryView.bot
        self.Slayer = InventoryView.Slayer
        self.interaction = interaction
        self.message = message
        self.cItem = cItem
        self.Slayer = InventoryView.Slayer
        self.List = []

        for item in List: 
            self.List.append(self.Slayer.cSlayer.inventory_items[item])

        self.add_item(Equiped_Dropdown(self.List))

    async def on_timeout(self) -> None:
        self.bot.ActiveList.close_interface(self.Slayer.cSlayer.slayer_id, "mult_equip")
        message = await self.interaction.original_message()
        await message.edit(view=None)
        self.stop()