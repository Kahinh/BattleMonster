import lib

def get_ephemeralAttack(self, Damage, Hit, Stacks_Earned, slayer_class, battle_class, user_id, canAttack):

    Bases_Bonuses_Slayers = self.BDD["Bases_Bonuses_Slayers"]
    Items_list = self.BDD["Items_list"]

    ephemeral_message = ""
    if Hit == "L":
        Hit = "Attaque Légère"
    elif Hit == "H":
        Hit = "Attaque Lourde"
    else: 
        Hit = "Spécial"
    
    if canAttack == False:
        ephemeral_message += f"> Pas si vite ! Prends ton temps ! Prochaine attaque disponible dans **{int(battle_class.slayers_data[user_id].timestamp_next_hit - lib.datetime.datetime.timestamp(lib.datetime.datetime.now()))}s**"
    else:
        if Damage == 0:
            #Esquive
            ephemeral_message += f"**> Le monstre a évité ton attaque !**"
        elif Damage < 0:
            #Les dégâts qu'on a subi
            ephemeral_message += f"**> Le monstre a bloqué ton attaque, et tu t'es fait attaquer en retour !**\n> ⚔️ Dégâts subis : {abs(Damage)} - Vie restante : {slayer_class.calculateStats()['total_current_health']}/{slayer_class.calculateStats()['total_max_health']} ❤️"
        else:
            #Dégâts infligés !
            ephemeral_message += f"**> Ton {Hit} a touché le monstre avec succès !**\n> ⚔️ Dégâts infligés : {Damage}"
            #Le monstre est il mort ?
            if battle_class.monster_class.base_hp == 0:
                ephemeral_message += f"\n> Le monstre est mort ! 💀"
            else:     
                ephemeral_message += f"\n> Le monstre possède désormais {battle_class.monster_class.base_hp}/{battle_class.monster_class.total_hp} ❤️"
            #Si on a gagné des stacks
            if Stacks_Earned > 0:
                ephemeral_message += f"\n\n> ☄️ Charge obtenue : {Stacks_Earned} - Charge total : **{slayer_class.special_stacks}/{slayer_class.calculateStats()['total_stacks']}**"
        
        #If Battle = already dealed damage, on affiche le total !
        if battle_class.slayers_data[user_id].total_damage > Damage and battle_class.slayers_data[user_id].total_damage > 0:
            ephemeral_message += f"\n\n> 🔱 Dégâts infligés totaux : {battle_class.slayers_data[user_id].total_damage}"

        #If Battle.eligible == False, on rajoute que le mec est pas éligible ! Sinon on affiche qu'il est éligible !
        if battle_class.slayers_data[user_id].eligible:
            #En ayant infligé des dégâts au Monstre, tu es éligible !
            ephemeral_message += f"\n\n> ✨ **En ayant infligé des dégâts au Monstre, tu es éligible à l'obtention de butin !**"
        else:
            ephemeral_message += f"\n\n> 🛑 **Tu n'es, pour l'instant, pas éligible à l'obtention de butin !**"

        #Puis, on rajoute la vivacité !
        ephemeral_message += f"\n\n> Grâce à ta vivacité de {slayer_class.calculateStats()['total_vivacity']}, tu pourras attaquer de nouveau dans **{slayer_class.calculateStats()['total_cooldown']}s**."

    return ephemeral_message

def get_ephemeralLootReaction(self, interaction, isGoodSlayer, reaction, loot):
    ephemeral_message = ""
    ephemeral_message += "Tu as cliqué !"
    return ephemeral_message