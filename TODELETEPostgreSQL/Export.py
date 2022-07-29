import os
import sys
import inspect
import psycopg2

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir) 

from Classes.Monsters import Monster
from Classes.Items import Item
from Classes.Slayers import Slayer
import Functions.PostgreSQL.Tools as Tools

def extractBDDs():
    BDDs = {}
    conn, cur = Tools.getConn()



#Channels
def get_PostgreSQL_channels():
    conn, cur = Tools.getConn()
    Channels = {}
    for row in Tools.get_resSQL(cur, "Channels"):
        if row[1] not in Channels: Channels[row[1]] = {}
        Channels[row[1]].update({row[2] : row[3]})
    Tools.closeConn(conn, cur)
    
    return Channels

def get_PostgreSQL_Slayerslist(self):
    conn, cur = Tools.getConn()

    #On recup les listes d'items
    Inventory_Items = {}
    for row in Tools.get_resSQL(cur, "Slayers_Inventory_Items"):
        if row != []:
            if row[0] not in Inventory_Items:
                Inventory_Items[row[0]] = []
            Inventory_Items[row[0]].append(row[1])

    Inventory_Specializations = {}
    for row in Tools.get_resSQL(cur, "Slayers_Inventory_Specializations"):
        if row != []:
            if row[0] not in Inventory_Specializations:
                Inventory_Specializations[row[0]] = []
            Inventory_Specializations[row[0]].append(row[1])

    Slayers_Slots = {}
    for row in Tools.get_resSQL(cur, "Slayers_Slots"):
        if row != []:
            if row[0] not in Slayers_Slots:
                Slayers_Slots[row[0]] = {}
            Slayers_Slots[row[0]][row[1]] = row[2]
    
    Slayers = {}
    for row in Tools.get_resSQL(cur, "Slayers"):
        Slayers[row[0]] = Slayers(\
        Run=self,
        name=row[8],
        creation_date=row[7],
        xp=row[1],
        money=row[2],
        damage_taken=row[3],
        special_stacks=row[4],
        faction=row[5],
        specialization=row[6],
        inventory_items=[] if Inventory_Items == {} or row[0] not in Inventory_Items else Inventory_Items[row[0]],
        inventory_specializations=[] if Inventory_Specializations == {} or row[0] not in Inventory_Specializations else Inventory_Specializations[row[0]],
        slots={} if Slayers_Slots == {} or row[0] not in Slayers_Slots else Slayers_Slots[row[0]]
        )

    Tools.closeConn(conn, cur)    
    return Slayers
