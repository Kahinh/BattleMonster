from pstats import Stats
import lib

class Loadout_Dropdown(lib.discord.ui.Select):
    def __init__(self, Loadouts):
        options = []
        for loadout_id in Loadouts:
            options.append(lib.discord.SelectOption(label=Loadouts[loadout_id].name, value=loadout_id))

        super().__init__(placeholder='Filtrer le loadout...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.cLoadout = self.view.cSlayer.loadouts[int(self.values[0])]
            await self.view.update_view(interaction) 
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Profil_Button_locked(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Profil :", style=lib.discord.ButtonStyle.grey)

class Profil_Button_global(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Global", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "Global"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Profil_Button_l(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="L", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "L"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Profil_Button_h(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="H", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "H"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Profil_Button_s(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="S", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "S"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Equipment_Button_locked(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équipement :", style=lib.discord.ButtonStyle.grey)

class Equipment_Button_weaponarmor(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Arme/Armure", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "Arme/Armure"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Equipment_Button_accessories(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Accessoires", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "Accessoires"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Equipment_Button_relics(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Reliques", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "Reliques"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Equipment_Button_pets(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Familiers", style=lib.discord.ButtonStyle.green)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "Familiers"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class LoadoutView(lib.discord.ui.View):
    def __init__(self, bot, cSlayer, interaction, avatar, interface_name="Loadout"):
        super().__init__(timeout=60)
        self.bot = bot
        self.interface_name=interface_name
        self.interaction = interaction
        self.cSlayer = cSlayer
        self.obsolete = False
        self.tab = "Global"
        self.avatar = avatar
        self.cLoadout = self.cSlayer.loadouts[list(self.cSlayer.loadouts.keys())[0]]

        self.add_items()

        self.enable_disable_buttons()


    def add_items(self):
        self.add_item(Profil_Button_locked())
        self.add_item(Profil_Button_global())
        self.add_item(Profil_Button_l())
        self.add_item(Profil_Button_h())
        self.add_item(Profil_Button_s())
        self.add_item(Equipment_Button_locked())
        self.add_item(Equipment_Button_weaponarmor())
        self.add_item(Equipment_Button_accessories())
        self.add_item(Equipment_Button_relics())
        self.add_item(Equipment_Button_pets())
        if len(self.cSlayer.loadouts) > 1:
            self.add_item(Loadout_Dropdown(self.cSlayer.loadouts))
    
    def select_embed(self):
        if self.tab == "Arme/Armure":
            embed = lib.Embed.create_embed_equipment(self.bot, self.cLoadout, self.avatar, "Arme/Armure")
        elif self.tab == "Accessoires":
            embed = lib.Embed.create_embed_equipment(self.bot, self.cLoadout, self.avatar, "Accessoires")
        elif self.tab == "Reliques":
            embed = lib.Embed.create_embed_equipment(self.bot, self.cLoadout, self.avatar, "Reliques")
        elif self.tab == "Familiers":
            embed = lib.Embed.create_embed_equipment(self.bot, self.cLoadout, self.avatar, "Familiers")
        elif self.tab == "Prouesses":
            embed = lib.Embed.create_embed_achievement(self.cLoadout, self.avatar)
        elif self.tab == "Ressources":
            embed = lib.Embed.create_embed_gatherables_profil(self.cLoadout, self.avatar, self.bot)
        elif self.tab == "L":
            embed = lib.Embed.create_embed_profil_attack(self.cLoadout, self.avatar, "l")
        elif self.tab == "H":
            embed = lib.Embed.create_embed_profil_attack(self.cLoadout, self.avatar, "h")
        elif self.tab == "S":
            embed = lib.Embed.create_embed_profil_attack(self.cLoadout, self.avatar, "s")
        else: #Profil
            embed = lib.Embed.create_embed_profil_global(self.cLoadout, self.avatar)
        return embed

    async def update_view(self, interaction=None):
        embed = self.select_embed()
        self.enable_disable_buttons()
        if interaction is None:
            message = await self.interaction.original_response()
            await message.edit(embed=embed) 
        else:
            await interaction.response.edit_message(embed=embed, view=self)
    
    def enable_disable_buttons(self):
        for item in self.children:
            if hasattr(item, "label"):
                if item.label==self.tab or item.label=="Profil :" or item.label =="Équipement :":
                    item.disabled = True
                elif item.label=="S" and (self.cLoadout.cSpe.id == 8 or self.cLoadout.cSpe.id == 5):
                    item.disabled = True
                else:
                    item.disabled = False

    async def close_view(self):
        if self.interface_name == "profil":
            self.bot.ActiveList.remove_interface(self.cLoadout.id, "profil")
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
