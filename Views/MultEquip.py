import lib

class Equiped_Dropdown(lib.discord.ui.Select):
    def __init__(self, List):
        options = []
        for item in List:
            options.append(lib.discord.SelectOption(label=f"{item.rarity} {item.element} - {item.name}", value=item.id))
        super().__init__(placeholder='Objet à remplacer...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if not self.view.obsolete:
            await self.view.cSlayer.equip_item(self.view.cObject)
            await self.view.cSlayer.unequip_item(self.view.cSlayer.inventories["items"][int(self.values[0])])

            #On update le Inventoryview ?
            await self.view.bot.ActiveList.update_interface(self.view.cSlayer.id, "inventaire")

            self.view.bot.ActiveList.remove_interface(self.view.cSlayer.id, "mult_equip")
            message = await self.view.interaction.original_response()
            await message.edit(view=None)
            self.view.stop()
            
            await interaction.followup.send(content="L'objet a été équipé !", ephemeral=True) 
        else:
            await interaction.followup.send(content="Cette interface est obsolete. Il te faut la redémarrer !")

class MultEquipView(lib.discord.ui.View):
    def __init__(self, bot, cSlayer, List, interaction, cObject):
        super().__init__(timeout=60)
        self.bot = bot
        self.cSlayer = cSlayer
        self.interaction = interaction
        self.cObject = cObject
        self.List = []
        self.obsolete = False

        self.List = List

        self.add_item(Equiped_Dropdown(self.List))

    async def close_view(self):
        self.bot.ActiveList.remove_interface(self.cSlayer.id, "mult_equip")
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
