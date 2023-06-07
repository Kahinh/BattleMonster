def get_display_stats(cStatOwner1, cStatOwner2):

    bot = cStatOwner1.bot

    desc_stat = ""

    #Bonuses Items 2
    if cStatOwner2 is not None:
        if cStatOwner2.name == cStatOwner1.name:
            bonuses_item2 = {}
            gearscore2 = 0       
        else:
            bonuses_item2 = cStatOwner2.bonuses
            gearscore2 = cStatOwner2.gearscore
    else:
        bonuses_item2 = {}
        gearscore2 = 0

    def create_desc_stat_1_line(bonuses_item2, stat, name, emote):
        desc_stat = ""
        if (cn(cStatOwner1.bonuses[stat])) != 0 or cn((bonuses_item2.get(stat, 0))) != 0:
            desc_stat += f"```ansi\n{emote}{name}: {_ffin(cStatOwner1.bonuses[stat], stat)} {sa(cStatOwner1.bonuses[stat], bonuses_item2.get(stat, 0)) + '[' + str(_ffin(bonuses_item2.get(stat, 0), stat)) + ']' if bonuses_item2 != {} else ''}```"    
        return desc_stat

    def create_desc_stat_2_lines(bonuses_item2, stat, name, emote, order=1):
        desc_stat = ""
        if cn(cStatOwner1.bonuses[f"{stat}_l"]) != 0 or cn(cStatOwner1.bonuses[f"{stat}_h"]) != 0 or cn(bonuses_item2.get(f"{stat}_l", 0)) != 0 or cn(bonuses_item2.get(f"{stat}_h", 0)) != 0:
            #Le cas où l'un ou l'autre est différent
            if ((cn(cStatOwner1.bonuses[f"{stat}_l"]) != cn(cStatOwner1.bonuses[f"{stat}_h"])) or (cn(bonuses_item2.get(f"{stat}_l", 0)) != cn(bonuses_item2.get(f"{stat}_h", 0)))):
                desc_stat += f"```ansi\n{emote}{name}:"
                #Parry L
                if cn(cStatOwner1.bonuses[f'{stat}_l']) != 0 or cn(bonuses_item2.get(f'{stat}_l', 0)) != 0:
                    desc_stat += f"\n\u001b[0;0m   Légère: {_ffin(cStatOwner1.bonuses[f'{stat}_l'], stat)} {sa(cStatOwner1.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0), order) + '[' + str(_ffin(bonuses_item2.get(f'{stat}_l', 0), stat)) + ']' if bonuses_item2 != {} else ''}"
                #Parry H
                if cn(cStatOwner1.bonuses[f'{stat}_h']) != 0 or cn(bonuses_item2.get(f'{stat}_h', 0)) != 0:
                    desc_stat += f"\n\u001b[0;0m   Lourde: {_ffin(cStatOwner1.bonuses[f'{stat}_h'], stat)} {sa(cStatOwner1.bonuses[f'{stat}_h'], bonuses_item2.get(f'{stat}_h', 0), order) + '[' + str(_ffin(bonuses_item2.get(f'{stat}_h', 0), stat)) + ']' if bonuses_item2 != {} else ''}"
            
                #on referme le ```
                desc_stat += "```"            

            #Le cas où les deux sont semblables
            else:
                if cn(cStatOwner1.bonuses[f"{stat}_l"]) != 0 or cn(bonuses_item2.get(f"{stat}_l", 0)) != 0:
                    desc_stat += f"```ansi\n{emote}{name}: {_ffin(cStatOwner1.bonuses[f'{stat}_l'], stat)} {sa(cStatOwner1.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0), order) + '[' + str(_ffin(bonuses_item2.get(f'{stat}_l', 0), stat)) + ']' if bonuses_item2 != {} else ''}```" 
        return desc_stat  

    def create_desc_stat_3_lines(bonuses_item2, stat, name, emote, order=1):
        desc_stat = ""
        if cn(cStatOwner1.bonuses[f"{stat}_l"]) != 0 or cn(cStatOwner1.bonuses[f"{stat}_h"]) != 0 or cn(cStatOwner1.bonuses[f"{stat}_s"]) != 0 or cn(bonuses_item2.get(f"{stat}_l", 0)) != 0 or cn(bonuses_item2.get(f"{stat}_h", 0)) != 0 or cn(bonuses_item2.get(f"{stat}_s", 0)) != 0:
            #Le cas où l'un ou l'autre est différent
            if ((cn(cStatOwner1.bonuses[f"{stat}_l"]) != cn(cStatOwner1.bonuses[f"{stat}_h"]) or cn(cStatOwner1.bonuses[f"{stat}_h"]) != cn(cStatOwner1.bonuses[f"{stat}_s"])) or (cn(bonuses_item2.get(f"{stat}_l", 0)) != cn(bonuses_item2.get(f"{stat}_h", 0)) or cn(bonuses_item2.get(f"{stat}_h", 0)) != cn(bonuses_item2.get(f"{stat}_s", 0)))):
                desc_stat += f"```ansi\n{emote}{name}:"
                #Damage L
                if cn(cStatOwner1.bonuses[f'{stat}_l']) != 0 or cn(bonuses_item2.get(f'{stat}_l', 0)) != 0:
                    desc_stat += f"\n\u001b[0;0m   Légère: {_ffin(cStatOwner1.bonuses[f'{stat}_l'], stat)} {sa(cStatOwner1.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0), order) + '[' + str(_ffin(bonuses_item2.get(f'{stat}_l', 0), stat)) + ']' if bonuses_item2 != {} else ''}"
                #Damage H
                if cn(cStatOwner1.bonuses[f'{stat}_h']) != 0 or cn(bonuses_item2.get(f'{stat}_h', 0)) != 0:
                    desc_stat += f"\n\u001b[0;0m   Lourde: {_ffin(cStatOwner1.bonuses[f'{stat}_h'], stat)} {sa(cStatOwner1.bonuses[f'{stat}_h'], bonuses_item2.get(f'{stat}_h', 0), order) + '[' + str(_ffin(bonuses_item2.get(f'{stat}_h', 0), stat)) + ']' if bonuses_item2 != {} else ''}"
                #Damage s
                if cn(cStatOwner1.bonuses[f'{stat}_s']) != 0 or cn(bonuses_item2.get(f'{stat}_s', 0)) != 0:
                    desc_stat += f"\n\u001b[0;0m   Spécial: {_ffin(cStatOwner1.bonuses[f'{stat}_s'], stat)} {sa(cStatOwner1.bonuses[f'{stat}_s'], bonuses_item2.get(f'{stat}_s', 0), order) + '[' + str(_ffin(bonuses_item2.get(f'{stat}_s', 0), stat)) + ']' if bonuses_item2 != {} else ''}"

                #on referme le ```
                desc_stat += "```"
            #Le cas où les deux sont semblables
            else:
                if cn(cStatOwner1.bonuses[f"{stat}_l"]) != 0 or cn(bonuses_item2.get(f"{stat}_l", 0)) != 0:
                    desc_stat += f"```ansi\n{emote}{name}: {_ffin(cStatOwner1.bonuses[f'{stat}_l'], stat)} {sa(cStatOwner1.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0)) + '[' + str(_ffin(bonuses_item2.get(f'{stat}_l', 0), stat)) + ']' if bonuses_item2 != {} else ''}```"
        return desc_stat

    def _ffin(number, stat=None):
        if stat is None:
            return f"{int(number)}"
        if bot.Statistics[stat].percentage:
            return f"{int(round(number*100,0))}%"
        else:
            return f"{int(number)}"
    
    def cn(number):
    #checking numbers
        return int(number * 10000)

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
        desc_stat += f"```ansi\n🔰Score: {_ffin(cStatOwner1.gearscore)} {sa(cStatOwner1.gearscore, gearscore2) + '[' + str(_ffin(gearscore2)) + ']' if bonuses_item2 != {} else ''}```" 
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