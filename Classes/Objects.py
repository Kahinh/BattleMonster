class Object:
  def __init__(self, bot, rItem):
    self.bot = bot
    self.id = rItem["id"]
    self.level = 0
    self.name = rItem["name"]
    self.description = rItem["description"]
    self.slot = rItem["slot"]
    self.equipped = False if "equipped" not in rItem else rItem["equipped"]
    self.img_url = rItem["img_url"]
    self.element = rItem["element"]
    self.rarity = rItem["rarity"]
    self.gearscore = self.setGearscore()
    self.bonuses = {
      "armor" : rItem["armor"],
      "armor_per" : float(rItem["armor_per"]),
      "health" : rItem["health"],
      "health_per" : float(rItem["health_per"]),
      "parry_l" : float(rItem["parry_l"]),
      "parry_h" : float(rItem["parry_h"]),
      "parry_s" : float(rItem["parry_s"]),
      "damage_weapon" : rItem["damage_weapon"],
      "damage_l" : rItem["damage_l"],
      "damage_h" : rItem["damage_h"],
      "damage_s" : rItem["damage_s"],
      "final_damage_l" : float(rItem["final_damage_l"]),
      "final_damage_h" : float(rItem["final_damage_h"]),
      "final_damage_s" : float(rItem["final_damage_s"]),
      "damage_per_l" : float(rItem["damage_per_l"]),
      "damage_per_h" : float(rItem["damage_per_h"]),
      "damage_per_s" : float(rItem["damage_per_s"]),
      "letality_l" : rItem["letality_l"],
      "letality_h" : rItem["letality_h"],
      "letality_s" : rItem["letality_s"],
      "letality_per_l" : float(rItem["letality_per_l"]),
      "letality_per_h" : float(rItem["letality_per_h"]),
      "letality_per_s" : float(rItem["letality_per_s"]),
      "crit_chance_l" : float(rItem["crit_chance_l"]),
      "crit_chance_h" : float(rItem["crit_chance_h"]),
      "crit_chance_s" : float(rItem["crit_chance_s"]),
      "crit_damage_l" : float(rItem["crit_damage_l"]),
      "crit_damage_h" : float(rItem["crit_damage_h"]),
      "crit_damage_s" : float(rItem["crit_damage_s"]),
      "special_charge_l" : rItem["special_charge_l"],
      "special_charge_h" : rItem["special_charge_h"],
      "special_charge_s" : rItem["special_charge_s"],
      "stacks_reduction" : rItem["stacks_reduction"],
      "luck": float(rItem["luck"]),
      "vivacity": rItem["vivacity"]
    }

  def equip(self):
      #TODO Mettre un self.bot.db 
      self.equipped = True

  def unequip(self):
      #TODO Mettre un self.bot.db 
      self.equipped = False
  
  def getDisplayStats(self, cItem=None):
    desc_stat = ""
    #Bonuses Items 2
    if cItem is not None:
      bonuses_item2 = cItem.bonuses
    else:
      bonuses_item2 = {}

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

    def create_desc_stat_1_line(self, bonuses_item2, stat, name, emote):
      desc_stat = ""
      if self.bonuses[stat] != 0 or bonuses_item2.get(stat, 0) != 0:
        desc_stat += f"```ansi\n{emote}{name}: {ffin(self.bonuses[stat])} {sa(self.bonuses[stat], bonuses_item2.get(stat, 0)) + '[' + str(ffin(bonuses_item2.get(stat, 0))) + ']' if bonuses_item2 != {} else ''}```"    
      return desc_stat

    def create_desc_stat_2_lines(self, bonuses_item2, stat, name, emote, order=1):
      desc_stat = ""
      if (int(self.bonuses[f"{stat}_l"]) != 0 or int(self.bonuses[f"{stat}_h"]) != 0 or int(bonuses_item2.get(f"{stat}_l", 0)) != 0 or int(bonuses_item2.get(f"{stat}_h", 0)) != 0):
        #Le cas où l'un ou l'autre est différent
        if ((self.bonuses[f"{stat}_l"] != self.bonuses[f"{stat}_h"]) or (bonuses_item2.get(f"{stat}_l", 0) != bonuses_item2.get(f"{stat}_h", 0))):
          desc_stat += f"```ansi\n{emote}{name}:"
          #Parry L
          desc_stat += f"\n\u001b[0;0m  Légère: {ffin(self.bonuses[f'{stat}_l'])} {sa(self.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_l', 0))) + ']' if bonuses_item2 != {} else ''}"
          #Parry H
          desc_stat += f"\n\u001b[0;0m  Lourde: {ffin(self.bonuses[f'{stat}_h'])} {sa(self.bonuses[f'{stat}_h'], bonuses_item2.get(f'{stat}_h', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_h', 0))) + ']' if bonuses_item2 != {} else ''}```"
        #Le cas où les deux sont semblables
        else:
          if self.bonuses[f"{stat}_l"] != 0 or bonuses_item2.get(f"{stat}_l", 0) != 0:
            desc_stat += f"```ansi\n{emote}{name}: {ffin(self.bonuses[f'{stat}_l'])} {sa(self.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_l', 0))) + ']' if bonuses_item2 != {} else ''}```" 
      return desc_stat  

    def create_desc_stat_3_lines(self, bonuses_item2, stat, name, emote, order=1):
      desc_stat = ""
      if (int(self.bonuses[f"{stat}_l"]) != 0 or int(self.bonuses[f"{stat}_h"]) != 0 or int(self.bonuses[f"{stat}_s"]) != 0 or int(bonuses_item2.get(f"{stat}_l", 0)) != 0 or int(bonuses_item2.get(f"{stat}_h", 0)) != 0 or int(bonuses_item2.get(f"{stat}_s", 0)) != 0):
        #Le cas où l'un ou l'autre est différent
        if ((self.bonuses[f"{stat}_l"] != self.bonuses[f"{stat}_h"] != self.bonuses[f"{stat}_s"]) or (bonuses_item2.get(f"{stat}_l", 0) != bonuses_item2.get(f"{stat}_h", 0) != bonuses_item2.get(f"{stat}_s", 0))):
          desc_stat += f"```ansi\n{emote}{name}:"
          #Damage L
          desc_stat += f"\n\u001b[0;0m  Légère: {ffin(self.bonuses[f'{stat}_l'])} {sa(self.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_l', 0))) + ']' if bonuses_item2 != {} else ''}"
          #Damage H
          desc_stat += f"\n\u001b[0;0m  Lourde: {ffin(self.bonuses[f'{stat}_h'])} {sa(self.bonuses[f'{stat}_h'], bonuses_item2.get(f'{stat}_h', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_h', 0))) + ']' if bonuses_item2 != {} else ''}"
          #Damage s
          desc_stat += f"\n\u001b[0;0m  Spécial: {ffin(self.bonuses[f'{stat}_s'])} {sa(self.bonuses[f'{stat}_s'], bonuses_item2.get(f'{stat}_s', 0), order) + '[' + str(ffin(bonuses_item2.get(f'{stat}_s', 0))) + ']' if bonuses_item2 != {} else ''}"

          #on referme le ```
          desc_stat += "```"
        #Le cas où les deux sont semblables
        else:
          if self.bonuses[f"{stat}_l"] != 0 or bonuses_item2.get(f"{stat}_l", 0) != 0:
            desc_stat += f"```ansi\n{emote}{name}: {ffin(self.bonuses[f'{stat}_l'])} {sa(self.bonuses[f'{stat}_l'], bonuses_item2.get(f'{stat}_l', 0)) + '[' + str(ffin(bonuses_item2.get(f'{stat}_l', 0))) + ']' if bonuses_item2 != {} else ''}```"
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

    return desc_stat

  def setGearscore(self):
    return self.bot.Rarities[self.rarity].gearscore

class Item(Object):
  def __init__(self, bot, rItem):
    super().__init__(bot, rItem)

class Improvable_Object(Object):
  def __init__(self, bot, rItem):
    super().__init__(bot, rItem)
    self.level = 1 if "level" not in rItem else rItem["level"]
    self.gearscore = self.setGearscore()
    self.bases_bonuses = {
      "armor" : rItem["armor"],
      "armor_per" : float(rItem["armor_per"]),
      "health" : rItem["health"],
      "health_per" : float(rItem["health_per"]),
      "parry_l" : float(rItem["parry_l"]),
      "parry_h" : float(rItem["parry_h"]),
      "parry_s" : float(rItem["parry_s"]),
      "damage_weapon" : rItem["damage_weapon"],
      "damage_l" : rItem["damage_l"],
      "damage_h" : rItem["damage_h"],
      "damage_s" : rItem["damage_s"],
      "final_damage_l" : float(rItem["final_damage_l"]),
      "final_damage_h" : float(rItem["final_damage_h"]),
      "final_damage_s" : float(rItem["final_damage_s"]),
      "damage_per_l" : float(rItem["damage_per_l"]),
      "damage_per_h" : float(rItem["damage_per_h"]),
      "damage_per_s" : float(rItem["damage_per_s"]),
      "letality_l" : rItem["letality_l"],
      "letality_h" : rItem["letality_h"],
      "letality_s" : rItem["letality_s"],
      "letality_per_l" : float(rItem["letality_per_l"]),
      "letality_per_h" : float(rItem["letality_per_h"]),
      "letality_per_s" : float(rItem["letality_per_s"]),
      "crit_chance_l" : float(rItem["crit_chance_l"]),
      "crit_chance_h" : float(rItem["crit_chance_h"]),
      "crit_chance_s" : float(rItem["crit_chance_s"]),
      "crit_damage_l" : float(rItem["crit_damage_l"]),
      "crit_damage_h" : float(rItem["crit_damage_h"]),
      "crit_damage_s" : float(rItem["crit_damage_s"]),
      "special_charge_l" : rItem["special_charge_l"],
      "special_charge_h" : rItem["special_charge_h"],
      "special_charge_s" : rItem["special_charge_s"],
      "stacks_reduction" : rItem["stacks_reduction"],
      "luck": float(rItem["luck"]),
      "vivacity": rItem["vivacity"]
    }
    self.bonuses = self.calculate_bonuses()

  def calculate_bonuses(self):
    bonuses = {
      "armor" : int(self.base_bonuses["armor"] * self.level),
      "armor_per" : round(self.base_bonuses["armor_per"] * self.level,4),
      "health" : int(self.base_bonuses["health"] * self.level),
      "health_per" : round(self.base_bonuses["health_per"] * self.level,4),
      "parry_l" : round(self.base_bonuses["parry_l"] * self.level,4),
      "parry_h" : round(self.base_bonuses["parry_h"] * self.level,4),
      "parry_s" : round(self.base_bonuses["parry_s"] * self.level,4),
      "damage_weapon" : int(self.base_bonuses["damage_weapon"] * self.level),
      "damage_l" : int(self.base_bonuses["damage_l"] * self.level),
      "damage_h" : int(self.base_bonuses["damage_h"] * self.level),
      "damage_s" : int(self.base_bonuses["damage_s"] * self.level),
      "final_damage_l" : round(self.base_bonuses["final_damage_l"] * self.level,4),
      "final_damage_h" : round(self.base_bonuses["final_damage_h"] * self.level,4),
      "final_damage_s" : round(self.base_bonuses["final_damage_s"] * self.level,4),
      "damage_per_l" : round(self.base_bonuses["damage_per_l"] * self.level,4),
      "damage_per_h" : round(self.base_bonuses["damage_per_h"] * self.level,4),
      "damage_per_s" : round(self.base_bonuses["damage_per_s"] * self.level,4),
      "letality_l" : int(self.base_bonuses["letality_l"] * self.level),
      "letality_h" : int(self.base_bonuses["letality_h"] * self.level),
      "letality_s" : int(self.base_bonuses["letality_s"] * self.level),
      "letality_per_l" : round(self.base_bonuses["letality_per_l"] * self.level,4),
      "letality_per_h" : round(self.base_bonuses["letality_per_h"] * self.level,4),
      "letality_per_s" : round(self.base_bonuses["letality_per_s"] * self.level,4),
      "crit_chance_l" : round(self.base_bonuses["crit_chance_l"] * self.level,4),
      "crit_chance_h" : round(self.base_bonuses["crit_chance_h"] * self.level,4),
      "crit_chance_s" : round(self.base_bonuses["crit_chance_s"] * self.level,4),
      "crit_damage_l" : round(self.base_bonuses["crit_damage_l"] * self.level,4),
      "crit_damage_h" : round(self.base_bonuses["crit_damage_h"] * self.level,4),
      "crit_damage_s" : round(self.base_bonuses["crit_damage_s"] * self.level,4),
      "special_charge_l" : int(self.base_bonuses["special_charge_l"] * self.level),
      "special_charge_h" : int(self.base_bonuses["special_charge_h"] * self.level),
      "special_charge_s" : int(self.base_bonuses["special_charge_s"] * self.level),
      "stacks_reduction" : int(self.base_bonuses["stacks_reduction"] * self.level),
      "luck": round(self.base_bonuses["luck"] * self.level,4),
      "vivacity": int(self.base_bonuses["vivacity"] * self.level)
    }
    return bonuses

  async def update_item_level(self, level_upgrade, cSlayer):
      self.level += level_upgrade
      await self.bot.dB.push_update_item_level(cSlayer, self)
      self.bonuses = self.calculate_bonuses()

class Pet(Improvable_Object):
  def __init__(self, bot, rItem):
    super().__init__(bot, rItem)

  def update_item_level(self, level_upgrade, cSlayer):
    super().update_item_level(level_upgrade, cSlayer)
    self.setGearscore()

  def setGearscore(self):
    return int((self.bot.Rarities[self.rarity].gearscore/100) * self.level)

class Mythic(Improvable_Object):
  def __init__(self, bot, rItem):
    super().__init__(bot, rItem)

  def update_item_level(self, level_upgrade, cSlayer):
    super().update_item_level(level_upgrade, cSlayer)
    self.setGearscore()

  def setGearscore(self):
    return self.bot.Rarities[self.rarity].gearscore + self.level