from pstats import Stats
import lib
from copy import deepcopy
from hashids import Hashids
from Classes.Loadouts import Loadout
#DOTENV
import os
from dotenv import load_dotenv
load_dotenv()

class Loadout_Dropdown(lib.discord.ui.Select):
    def __init__(self, Loadouts, bot):
        options = []
        for loadout_id in Loadouts:
            options.append(lib.discord.SelectOption(label=f"{Loadouts[loadout_id].name}- (GS : {Loadouts[loadout_id].gearscore})", value=loadout_id, emoji=Loadouts[loadout_id].cSpe.emote))
        if len(options) < bot.Variables["loadout_maximum"]:
            options.append(lib.discord.SelectOption(label="Enregistrer l'équipement actuel", value=0, emoji='🆕'))

        super().__init__(placeholder='Filtrer le loadout...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            if int(self.values[0]) == 0:
                await interaction.response.send_modal(Loadout_Name(self.view.cSlayer))
            else:
                self.view.index = int(self.values[0])
                self.view.select_cLoadout()
                await self.view.update_view(interaction) 
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Loadout_Name(lib.discord.ui.Modal):
    def __init__(self, cSlayer, loadout_id=None):
        self.cSlayer = cSlayer
        self.loadout_id = loadout_id
        super().__init__(title=f"Enregistrement du Loadout")

        #Item
        self.loadout_name = lib.discord.ui.TextInput(label=f"Nom du Loadout",default="Mon loadout", style=lib.discord.TextStyle.short, min_length=1, max_length=20)
        self.add_item(self.loadout_name)

    async def on_submit(self, interaction: lib.discord.Interaction):
        if self.loadout_id is None:
            id = await self.cSlayer.bot.dB.push_creation_loadouts(self.cSlayer.id, self.loadout_name.value, self.cSlayer.current_loadout.get_loadout_list())
            self.cSlayer.loadouts[id] = await Loadout.get_Object_Class_from_cSlayer(self.cSlayer.bot, str(self.loadout_name.value), self.cSlayer, self.cSlayer.current_loadout.cSpe.id, self.cSlayer.current_loadout.items)
            await interaction.response.send_message(f"Le loadout a bien été ajouté !", ephemeral=True)
        else:
            await self.cSlayer.bot.dB.push_update_loadouts(self.loadout_id, self.cSlayer.id, self.loadout_name.value, self.cSlayer.current_loadout.get_loadout_list())
            self.cSlayer.loadouts[self.loadout_id] = await Loadout.get_Object_Class_from_cSlayer(self.cSlayer.bot, str(self.loadout_name.value), self.cSlayer, self.cSlayer.current_loadout.cSpe.id, self.cSlayer.current_loadout.items)
            await interaction.response.send_message(f"Le loadout a bien été remplacé !", ephemeral=True)
        await self.cSlayer.bot.ActiveList.update_interface(self.cSlayer.id, "Loadout")

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

class Action_Button_locked(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Action :", style=lib.discord.ButtonStyle.grey)

class Action_Button_export(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Export", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            hashids = Hashids(salt=os.getenv('HASH_ID_BM'), min_length=16)
            export_loadout_list = [int(os.getenv('EXPORT_VERSION')), self.view.cLoadout.cSpe.id]
            for cObject in self.view.cLoadout.items:
                export_loadout_list.append(cObject.id)
            export_loadout_list = hashids.encode(*export_loadout_list)
            await interaction.response.send_message(content=f"Loadout {self.view.cLoadout.name} compilé : {export_loadout_list}", ephemeral=True)
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Action_Button_replace(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Remplacer", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            await interaction.response.send_modal(Loadout_Name(self.view.cSlayer, self.view.index))
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Action_Button_import(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Importer", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            await interaction.response.send_modal(Loadout_Name_Import(self.view.cSlayer, self.view.index))
        else:
            await interaction.response.send_message(content="Cette interface est obsolete. Il te faut la redémarrer !", ephemeral=True)

class Loadout_Name_Import(lib.discord.ui.Modal):
    def __init__(self, cSlayer, loadout_id):
        self.cSlayer = cSlayer
        self.loadout_id = loadout_id
        super().__init__(title=f"Import de Loadout")

        #Item
        self.loadout_name = lib.discord.ui.TextInput(label=f"Nom du Loadout",default="Mon loadout", style=lib.discord.TextStyle.short, min_length=1, max_length=20)
        self.loadout_hash = lib.discord.ui.TextInput(label=f"Code du Loadout",default="code....", style=lib.discord.TextStyle.short, min_length=1, max_length=30)
        self.add_item(self.loadout_name)
        self.add_item(self.loadout_hash)

    async def on_submit(self, interaction: lib.discord.Interaction):
        hashids = Hashids(salt=os.getenv('HASH_ID_BM'), min_length=16)
        loadout_data = list(hashids.decode(self.loadout_hash.value))
        if loadout_data != []:
            if int(loadout_data[0]) == int(os.getenv('EXPORT_VERSION')):
                if len(self.cSlayer.loadouts) < self.cSlayer.bot.Variables["loadout_maximum"]:
                    id = await self.cSlayer.bot.dB.push_creation_loadouts(self.cSlayer.id, self.loadout_name.value, loadout_data[1:])
                    self.cSlayer.loadouts[id] = await Loadout.get_Object_Class_from_db(self.cSlayer.bot, str(self.loadout_name.value), self.cSlayer, loadout_data[1:][0], loadout_data[2:])
                    await interaction.response.send_message(f"Le loadout a bien été ajouté !", ephemeral=True)
                else:
                    await self.cSlayer.bot.dB.push_update_loadouts(self.loadout_id, self.cSlayer.id, self.loadout_name.value, loadout_data[1:])
                    self.cSlayer.loadouts[self.loadout_id] = await Loadout.get_Object_Class_from_db(self.cSlayer.bot, str(self.loadout_name.value), self.cSlayer, loadout_data[1:][0], loadout_data[2:])
                    await interaction.response.send_message(f"Le loadout a bien été remplacé !", ephemeral=True)
                await self.cSlayer.bot.ActiveList.update_interface(self.cSlayer.id, "Loadout")
            else:
                await interaction.response.send_message(content="Ce code provient d'une ancienne version de l'export !", ephemeral=True)
        else:
            await interaction.response.send_message(content="Ce code était erroné !", ephemeral=True)

class Action_Button_equip(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Équiper", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        if not self.view.obsolete:
            self.view.cSlayer.current_loadout = await Loadout.get_Object_Class_from_cSlayer(self.view.cSlayer.bot, self.view.cLoadout.name, self.view.cSlayer, self.view.cLoadout.cSpe.id, self.view.cLoadout.items, True)
            await interaction.response.send_message(content="Le loadout a été équipé !", ephemeral=True)
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
        self.index = list(self.cSlayer.loadouts.keys())[0] if len(self.cSlayer.loadouts) > 0 else 0
        self.select_cLoadout()
        self.add_items()
        self.enable_disable_buttons()


    def select_cLoadout(self):
        if len(self.cSlayer.loadouts) > 0 : self.cLoadout = self.cSlayer.loadouts[self.index]

    def add_items(self):
        self.clear_items()
        if len(self.cSlayer.loadouts) > 0: 
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
        self.add_item(Loadout_Dropdown(self.cSlayer.loadouts, self.bot))
        self.add_item(Action_Button_locked())
        if len(self.cSlayer.loadouts) > 0:
            self.add_item(Action_Button_replace())
            self.add_item(Action_Button_export())
        self.add_item(Action_Button_import())
        self.add_item(Action_Button_equip())

    
    def select_embed(self):
        if len(self.cSlayer.loadouts) == 0:
            embed=lib.discord.Embed(title=f"Liste des Loadouts :",
            description="Vous ne possédez pas encore de Loadouts",
            color=0x1abc9c)   
        else:
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
                embed = lib.Embed.create_embed_profil_attack(self.cLoadout, self.avatar, "l", self.cSlayer.current_loadout)
            elif self.tab == "H":
                embed = lib.Embed.create_embed_profil_attack(self.cLoadout, self.avatar, "h", self.cSlayer.current_loadout)
            elif self.tab == "S":
                embed = lib.Embed.create_embed_profil_attack(self.cLoadout, self.avatar, "s", self.cSlayer.current_loadout)
            else: #Profil
                embed = lib.Embed.create_embed_profil_global(self.cLoadout, self.avatar, self.cSlayer.current_loadout)
        return embed

    async def update_view(self, interaction=None):
        self.add_items()
        embed = self.select_embed()
        self.enable_disable_buttons()
        if interaction is None:
            message = await self.interaction.original_response()
            await message.edit(embed=embed, view=self) 
        else:
            await interaction.response.edit_message(embed=embed, view=self)
    
    def enable_disable_buttons(self):
        for item in self.children:
            if hasattr(item, "label"):
                if item.label==self.tab or item.label in ["Profil :", "Équipement :", "Action :"]:
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
