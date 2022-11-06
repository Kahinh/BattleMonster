import lib

class Light_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Attaque Légère", style=lib.discord.ButtonStyle.blurple)

    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        content, damage = await self.view.Battle.getAttack(interaction, "L")
        #On répond au joueur
        await interaction.followup.send(content=content, ephemeral=True)
        if damage != []:
            await self.view.updateBattle()

class Heavy_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Attaque Lourde", style=lib.discord.ButtonStyle.green)
        
    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        content, damage = await self.view.Battle.getAttack(interaction, "H")
        #On répond au joueur
        await interaction.followup.send(content=content, ephemeral=True)
        if damage != []:
            await self.view.updateBattle()


class Special_Button(lib.discord.ui.Button):
    def __init__(self):
        super().__init__(label="Capacité Spéciale", style=lib.discord.ButtonStyle.red)

    async def callback(self, interaction: lib.discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        content, damage = await self.view.Battle.getAttack(interaction, "S")
        #On répond au joueur
        await interaction.followup.send(content=content, ephemeral=True)
        if damage != []:
            await self.view.updateBattle()
        

class BattleView(lib.discord.ui.View):
    def __init__(self, Battle):
        super().__init__(timeout=600)
        self.Battle = Battle

        # Adds the dropdown to our view object.
        self.add_item(Light_Button())
        self.add_item(Heavy_Button())
        self.add_item(Special_Button())

    async def updateBattle(self, timeout=False, poweroff=False):
        if self.Battle.EndNotPublished:
            if hasattr(self, "interaction"): message = await self.interaction.original_response()
            if hasattr(self, "message"): message = self.message
            if self.Battle.end or timeout:

                self.Battle.EndNotPublished = False

                if self.Battle.end:
                    await self.Battle.calculateLoot()

                if self.Battle.stats['attacks_received'] > 0 and poweroff==False:
                    content = lib.Toolbox.get_content_looters(self.Battle)
                    embed = lib.Embed.create_embed_end_battle(self.Battle, timeout)
                    if self.Battle.loots != {}:
                        view = lib.LootRecapView(self.Battle)
                    else:
                        view = None

                    channel = self.Battle.bot.get_channel(self.Battle.bot.rChannels["loots"])
                    if view is None:
                        await channel.send(embed=embed, view=view)
                    else:
                        view.message = await channel.send(content=content, embed=embed, view=view)
                        self.Battle.bot.ActiveList.add_recap(view.message.id, view)
                
                await message.delete()

                if not poweroff:
                    #On remove le combat de la liste
                    self.Battle.bot.ActiveList.remove_battle(message.id)

                self.stop()
            else:
                embed = lib.Embed.create_embed_battle(self.Battle)
                view = self
                await message.edit(embed=embed, view=view)

    async def on_timeout(self) -> None:
        await self.updateBattle(True)
        self.stop()