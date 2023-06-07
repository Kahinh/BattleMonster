from pstats import Stats
import lib

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

class Achievements_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Prouesses", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "Prouesses"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Gatherables_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Ressources", style=lib.discord.ButtonStyle.grey)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.tab = "Ressources"
            await self.view.update_view(interaction)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class SlayerView(lib.discord.ui.View):
    def __init__(self, bot, cSlayer, interaction, avatar, interface_name="profil"):
        super().__init__(timeout=60)
        self.bot = bot
        self.interface_name=interface_name
        self.interaction = interaction
        self.cSlayer = cSlayer
        self.obsolete = False
        self.tab = "Profil"
        self.avatar = avatar

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
        self.add_item(Achievements_Button())
        self.add_item(Gatherables_Button())

        for item in self.children:
            if item.label=="Profil :" or item.label=="Global" or item.label =="Équipement :":
                item.disabled = True
            if item.label=="S" and (self.cSlayer.cSpe.id == 8 or self.cSlayer.cSpe.id == 5):
                item.disabled = True

    async def update_view(self, interaction=None):
        if self.tab == "Arme/Armure":
            embed = lib.Embed.create_embed_equipment(self.bot, self.cSlayer, self.avatar, "Arme/Armure")
        elif self.tab == "Accessoires":
            embed = lib.Embed.create_embed_equipment(self.bot, self.cSlayer, self.avatar, "Accessoires")
        elif self.tab == "Reliques":
            embed = lib.Embed.create_embed_equipment(self.bot, self.cSlayer, self.avatar, "Reliques")
        elif self.tab == "Familiers":
            embed = lib.Embed.create_embed_equipment(self.bot, self.cSlayer, self.avatar, "Familiers")
        elif self.tab == "Prouesses":
            embed = lib.Embed.create_embed_achievement(self.cSlayer, self.avatar)
        elif self.tab == "Ressources":
            embed = lib.Embed.create_embed_gatherables_profil(self.cSlayer, self.avatar, self.bot)
        elif self.tab == "L":
            embed = lib.Embed.create_embed_profil_l(self.cSlayer, self.avatar)
        elif self.tab == "H":
            embed = lib.Embed.create_embed_profil_h(self.cSlayer, self.avatar)
        elif self.tab == "S":
            embed = lib.Embed.create_embed_profil_s(self.cSlayer, self.avatar)
        else: #Profil
            embed = lib.Embed.create_embed_profil_global(self.cSlayer, self.avatar)

        for item in self.children:
            if item.label==self.tab or item.label=="Profil :" or item.label =="Équipement :":
                item.disabled = True
            elif item.label=="S" and (self.cSlayer.cSpe.id == 8 or self.cSlayer.cSpe.id == 5):
                item.disabled = True
            else:
                item.disabled = False
        if interaction is None:
            message = await self.interaction.original_response()
            await message.edit(embed=embed) 
        else:
            await interaction.response.edit_message(embed=embed, view=self)

    async def close_view(self):
        if self.interface_name == "profil":
            self.bot.ActiveList.remove_interface(self.cSlayer.id, "profil")
        message = await self.interaction.original_response()
        await message.edit(view=None)
        self.stop()

    async def on_timeout(self) -> None:
        await self.close_view()
