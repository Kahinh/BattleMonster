import lib

def get_ephemeralAttack(Damage, Stacks_Earned, Hit, Buttons_Battle, Slayer, cMonster, user_id, canAttack):

    ephemeral_message = ""
    if Hit == "L":
        Hit = "Attaque Légère"
    elif Hit == "H":
        Hit = "Attaque Lourde"
    else: 
        Hit = "Spécial"
    if Slayer.dead:
        ephemeral_message += f"> Tu es mort ! Tu ne peux donc pas attaquer pour l'instant 💀"
    else:
        if canAttack == False:
            ephemeral_message += f"> Pas si vite ! Prends ton temps ! Prochaine attaque disponible dans **{int(cMonster.slayers_hits[user_id].timestamp_next_hit - lib.datetime.datetime.timestamp(lib.datetime.datetime.now()))}s**"
        else:
            if Damage == 0:
                #Esquive
                if Hit == "Spécial":
                    #on ne peut pas utiliser le sécial on n'a pas les stacks !
                    ephemeral_message += f"\n\n> ☄️ Tu ne possèdes pas le nombre de charges nécessaires - Charge total : **{Buttons_Battle.Main.bot.slayers_list[user_id].special_stacks}/{Slayer.stats['total_stacks']}**"
                else:
                    ephemeral_message += f"**> Le monstre a évité ton attaque !**"
            elif Damage < 0:
                #Les dégâts qu'on a subi
                ephemeral_message += f"**> Le monstre a bloqué ton attaque, et tu t'es fait attaquer en retour !**\n> ⚔️ Dégâts subis : {abs(Damage)} - Vie restante : {Slayer.stats['total_current_health'] - Slayer.damage_taken}/{Slayer.stats['total_max_health']} ❤️"
                if Slayer.dead:
                    ephemeral_message += f"**\n> Tu es mort 💀"
            else:
                #Dégâts infligés !
                ephemeral_message += f"**> Ton {Hit} a touché le monstre avec succès !**\n> ⚔️ Dégâts infligés : {Damage}"
                #Le monstre est il mort ?
                if cMonster.base_hp == 0:
                    ephemeral_message += f"\n> Le monstre est mort ! 💀"
                else:     
                    ephemeral_message += f"\n> Le monstre possède désormais {cMonster.base_hp}/{cMonster.total_hp} ❤️"
                #Si on a gagné des stacks
                if Stacks_Earned > 0:
                    ephemeral_message += f"\n\n> ☄️ Charge obtenue : {Stacks_Earned} - Charge total : **{Slayer.special_stacks}/{Slayer.stats['total_stacks']}**"
                if Stacks_Earned < 0:
                    ephemeral_message += f"\n\n> ☄️ Charge consommée : {abs(Stacks_Earned)} - Charge total : **{Slayer.special_stacks}/{Slayer.stats['total_stacks']}**"
            
            #If Battle = already dealed damage, on affiche le total !
            if cMonster.slayers_hits[user_id].total_damage > Damage and cMonster.slayers_hits[user_id].total_damage > 0:
                ephemeral_message += f"\n\n> 🔱 Dégâts infligés totaux : {cMonster.slayers_hits[user_id].total_damage}"

            #If Battle.eligible == False, on rajoute que le mec est pas éligible ! Sinon on affiche qu'il est éligible !
            if cMonster.slayers_hits[user_id].eligible:
                #En ayant infligé des dégâts au Monstre, tu es éligible !
                ephemeral_message += f"\n\n> ✨ **En ayant infligé des dégâts au Monstre, tu es éligible à l'obtention de butin !**"
            else:
                ephemeral_message += f"\n\n> 🛑 **Tu n'es, pour l'instant, pas éligible à l'obtention de butin !**"

            cooldown = Buttons_Battle.cMonster.slayers_hits[user_id].timestamp_next_hit - lib.datetime.datetime.timestamp(lib.datetime.datetime.now())

            #Puis, on rajoute la vivacité !
            if cooldown <= 1:
                ephemeral_message += f"\n\n> Tu peux **attaquer avec une Attaque Légère ou une Attaque Lourde !**"
            else:
                ephemeral_message += f"\n\n> Grâce à ta vivacité de {Slayer.stats['total_vivacity']}, tu pourras attaquer de nouveau dans **{cooldown}s**."

    return ephemeral_message

def get_ephemeralLootReaction(Buttons_Loot, interaction, isGoodSlayer, reaction, loot, rPrice, rRarity):
    ephemeral_message = ""
    ephemeral_message += "Tu as cliqué !"
    return ephemeral_message