def get_display_stats(cStatOwner1, cStatOwner2):
    desc_stat = ""
    #Bonuses Items 2
    if cStatOwner2 is not None:
        bonuses_item2 = cStatOwner2.bonuses
        gearscore2 = cStatOwner2.gearscore
    else:
        bonuses_item2 = {}
        gearscore2 = 0

    def create_desc_stat_1_line(bonuses_item2, stat, name, emote):
        desc_stat = ""
        if (cStatOwner1.bonuses[stat]*100) != 0 or (bonuses_item2.get(stat, 0)*100) != 0:
            desc_stat += f"```ansi\n{emote}{name}: {ffin(cStatOwner1.bonuses[stat])} {sa(cStatOwner1.bonuses[stat], bonuses_item2.get(stat, 0)) + '[' + str(ffin(bonuses_item2.get(stat, 0))) + ']' if bonuses_item2 != {} else ''}```"    
        return desc_stat

    def create_desc_stat_2_lines(bonuses_item2, stat, name, emote, order=1):
        desc_stat = ""
        if (int(cStatOwner1.bonuses[f"{stat}_l"]*100) != 0 or int(cStatOwner1.bonuses[f"{stat}_h"]*100) != 0 or int(bonuses_item2.get(f"{stat}_l", 0)*100) != 0 or int(bonuses_item2.get(f"{stat}_h", 0)*100) != 0):
            #Le cas où l'un ou l'autre est différent
            if ((cStatOwner1.bonuses[f"{stat}_l"] != cStatOwner1.bonuses[f"{stat}_h"]) or (bonuses_item2.get(f"{stat}_l", 0) != bonuses_item2.get(f"{stat}_h", 0))):
                desc_stat += f"```ansi\n{emote}{name}:"
                #Parry L
                if int(cStatOwner1.bonuses[f'{stat}_l']) != 0 or int(bonuses_item2.get(f'{stat}_l', 0)) != 0:
                    desc_stat += f"\n\u001b[0;0m   Légère: {ffin(cStatOwner1.bonuses[f'{stat}_l'])} {sa(cStatOwner1.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_l', 0))) + ']' if bonuses_item2 != {} else ''}"
                #Parry H
                if int(cStatOwner1.bonuses[f'{stat}_h']) != 0 or int(bonuses_item2.get(f'{stat}_h', 0)) != 0:
                    desc_stat += f"\n\u001b[0;0m   Lourde: {ffin(cStatOwner1.bonuses[f'{stat}_h'])} {sa(cStatOwner1.bonuses[f'{stat}_h'], bonuses_item2.get(f'{stat}_h', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_h', 0))) + ']' if bonuses_item2 != {} else ''}"
            
                #on referme le ```
                desc_stat += "```"            

            #Le cas où les deux sont semblables
            else:
                if cStatOwner1.bonuses[f"{stat}_l"] != 0 or bonuses_item2.get(f"{stat}_l", 0) != 0:
                    desc_stat += f"```ansi\n{emote}{name}: {ffin(cStatOwner1.bonuses[f'{stat}_l'])} {sa(cStatOwner1.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_l', 0))) + ']' if bonuses_item2 != {} else ''}```" 
        return desc_stat  

    def create_desc_stat_3_lines(bonuses_item2, stat, name, emote, order=1):
        desc_stat = ""
        if (int(cStatOwner1.bonuses[f"{stat}_l"]*100) != 0 or int(cStatOwner1.bonuses[f"{stat}_h"]*100) != 0 or int(cStatOwner1.bonuses[f"{stat}_s"]*100) != 0 or int(bonuses_item2.get(f"{stat}_l", 0)*100) != 0 or int(bonuses_item2.get(f"{stat}_h", 0)*100) != 0 or int(bonuses_item2.get(f"{stat}_s", 0)*100) != 0):
            #Le cas où l'un ou l'autre est différent
            if ((cStatOwner1.bonuses[f"{stat}_l"] != cStatOwner1.bonuses[f"{stat}_h"] != cStatOwner1.bonuses[f"{stat}_s"]) or (bonuses_item2.get(f"{stat}_l", 0) != bonuses_item2.get(f"{stat}_h", 0) != bonuses_item2.get(f"{stat}_s", 0))):
                desc_stat += f"```ansi\n{emote}{name}:"
                #Damage L
                if int(cStatOwner1.bonuses[f'{stat}_l']) != 0 or int(bonuses_item2.get(f'{stat}_l', 0)) != 0:
                    desc_stat += f"\n\u001b[0;0m   Légère: {ffin(cStatOwner1.bonuses[f'{stat}_l'])} {sa(cStatOwner1.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_l', 0))) + ']' if bonuses_item2 != {} else ''}"
                #Damage H
                if int(cStatOwner1.bonuses[f'{stat}_h']) != 0 or int(bonuses_item2.get(f'{stat}_h', 0)) != 0:
                    desc_stat += f"\n\u001b[0;0m   Lourde: {ffin(cStatOwner1.bonuses[f'{stat}_h'])} {sa(cStatOwner1.bonuses[f'{stat}_h'], bonuses_item2.get(f'{stat}_h', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_h', 0))) + ']' if bonuses_item2 != {} else ''}"
                #Damage s
                if int(cStatOwner1.bonuses[f'{stat}_s']) != 0 or int(bonuses_item2.get(f'{stat}_s', 0)) != 0:
                    desc_stat += f"\n\u001b[0;0m   Spécial: {ffin(cStatOwner1.bonuses[f'{stat}_s'])} {sa(cStatOwner1.bonuses[f'{stat}_s'], bonuses_item2.get(f'{stat}_s', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_s', 0))) + ']' if bonuses_item2 != {} else ''}"

                #on referme le ```
                desc_stat += "```"
            #Le cas où les deux sont semblables
            else:
                if cStatOwner1.bonuses[f"{stat}_l"] != 0 or bonuses_item2.get(f"{stat}_l", 0) != 0:
                    desc_stat += f"```ansi\n{emote}{name}: {ffin(cStatOwner1.bonuses[f'{stat}_l'])} {sa(cStatOwner1.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0)) + '[' + str(ffin(bonuses_item2.get(f'{stat}_l', 0))) + ']' if bonuses_item2 != {} else ''}```"
        return desc_stat

    def ffin(number):
    #format float int numbers
        if isinstance(number, float):
            return f"{int(round(number*100,0))}%"
        else:
            return f"{number}"

    def sa(equippednumber, secondnumber, order=1):
    #select ANSI
        #Basique : \u001b[0;0m
        #Rouge : \u001b[1;31m
        #Vert : \u001b[1;32m
        #Jaune : \u001b[1;33m
        if equippednumber == secondnumber:
            return "\u001b[1;33m"
        else:
            if order == 0:
                if equippednumber > secondnumber:
                    return "\u001b[1;31m"
                else:
                    return "\u001b[1;32m"
            else:
                if equippednumber > secondnumber:
                    return "\u001b[1;32m"
                else:
                    return "\u001b[1;31m"

    #Score
    if hasattr(cStatOwner1, "gearscore"):
        desc_stat += f"```ansi\n🔰Score: {ffin(cStatOwner1.gearscore)} {sa(cStatOwner1.gearscore, gearscore2) + '[' + str(ffin(gearscore2)) + ']' if cStatOwner2 != None else ''}```" 
    #Armor
    desc_stat += create_desc_stat_1_line(bonuses_item2, "armor", "Armure", "🛡️")
    #Armor_Per
    desc_stat += create_desc_stat_1_line(bonuses_item2, "armor_per", "Bonus Armure", "🛡️")
    #Health
    desc_stat += create_desc_stat_1_line(bonuses_item2, "health", "Vie", "❤️")
    #Health_Per
    desc_stat += create_desc_stat_1_line(bonuses_item2, "health_per", "Bonus Vie", "💖")
    #Parry
    desc_stat += create_desc_stat_2_lines(bonuses_item2, "parry", "Parade", "↪️", 0)
    #Damage_Weapon
    desc_stat += create_desc_stat_1_line(bonuses_item2, "damage_weapon", "Puissance Arme", "⚔️")
    #Damage
    desc_stat += create_desc_stat_3_lines(bonuses_item2, "damage", "Puissance", "🔥")
    #Damage_Per
    desc_stat += create_desc_stat_3_lines(bonuses_item2, "damage_per", "Bonus Puissance", "🔥")
    #Final_Damage
    desc_stat += create_desc_stat_3_lines(bonuses_item2, "final_damage", "Dégâts Finaux", "💯")
    #Letality
    desc_stat += create_desc_stat_3_lines(bonuses_item2, "letality", "Pénétration", "🗡️")
    #Letality_Per
    desc_stat += create_desc_stat_3_lines(bonuses_item2, "letality_per", "Bonus Pénétration", "🗡️")
    #Crit_Chance
    desc_stat += create_desc_stat_3_lines(bonuses_item2, "crit_chance", "Chance Critique", "✨")
    #Crit_Damage
    desc_stat += create_desc_stat_3_lines(bonuses_item2, "crit_damage", "Dégâts Critiques", "💢")
    #Special Charge 
    desc_stat += create_desc_stat_3_lines(bonuses_item2, "special_charge", "Gain Charge", "⏫")
    #Stacks Reduction
    desc_stat += create_desc_stat_1_line(bonuses_item2, "stacks_reduction", "Réduction Charge", "☄️")
    #Luck
    desc_stat += create_desc_stat_1_line(bonuses_item2, "luck", "Prospérité", "🍀")
    #Vivacity   
    desc_stat += create_desc_stat_1_line(bonuses_item2, "vivacity", "Vivacité", "🌪️")

    return desc_stat