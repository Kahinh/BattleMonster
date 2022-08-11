import lib

class Equiped_Dropdown(lib.discord.ui.Select):
    def __init__(self, List):
        options = []
        for item in List:
            options.append(lib.discord.SelectOption(label=f"{item.rarity} {item.element} - {item.name}", value=item.item_id))
        super().__init__(placeholder='Objet à remplacer...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        pass

class MultEquipView(lib.discord.ui.View):
    def __init__(self, InventoryView, List):
        super().__init__()
        self.InventoryView = InventoryView
        self.List = List

        self.add_item(Equiped_Dropdown(List))