import os
import sys
import inspect
import psycopg2
import datetime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir) 
from Functions.PostgreSQL.Import import ImportTable
from gitignore import postgresql

def get_resSQL(cur, table):
    cur.execute(f'select * from "{table}"')
    return cur.fetchall()

def updateTables(Slayers):
    conn, cur = getConn()

    logs = ""

    #1 on delete les tables
    deleteTable(conn, cur, "Slayers")
    deleteTable(conn, cur, "Slayers_Inventory_Items")
    deleteTable(conn, cur, "Slayers_Inventory_Specializations")
    deleteTable(conn, cur, "Slayers_Slots")

    #2 on import
        #1 Les SLAYERS
    records_to_insert = create_slayers_records(Slayers)
    postgres_insert_query = f"""INSERT INTO "Slayers" (slayer_id, xp, money, damage_taken, special_stacks, faction, specialization, creation_date, name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    logs += ImportTable(conn, cur, postgres_insert_query, records_to_insert, "Slayers")
        #2 L'inventory Items
    records_to_insert = create_inventory_items_records(Slayers)
    postgres_insert_query = f'INSERT INTO "Slayers_Inventory_Items" (slayer_id, item_id) VALUES (%s,%s)'
    logs += ImportTable(conn, cur, postgres_insert_query, records_to_insert, "Slayers_Inventory_Items")
        #3 L'inventory Specialization
    records_to_insert = create_inventory_specialization_records(Slayers)
    postgres_insert_query = f'INSERT INTO "Slayers_Inventory_Specializations" (slayer_id, specialization_id) VALUES (%s,%s)'
    logs += ImportTable(conn, cur, postgres_insert_query, records_to_insert, "Slayers_Inventory_Specializations")
        #4 Les slots
    records_to_insert = create_slayers_slots_records(Slayers)
    postgres_insert_query = f'INSERT INTO "Slayers_Slots" (slayer_id, slot, item_id) VALUES (%s,%s,%s)'
    logs += ImportTable(conn, cur, postgres_insert_query, records_to_insert, "Slayers_Slots")

    #3 On commit les changes & on close
    closeConn(conn, cur)

    return logs


def getConn():
    #Si on est en local (Donc en prod)
    #conn = psycopg2.connect('dbname')
    conn = psycopg2.connect(f'host={postgresql.host} user={postgresql.user} password={postgresql.password} dbname={postgresql.dbname}')
    cur = conn.cursor()
    return conn, cur

def closeConn(conn, cur):
    #Commit changes
    conn.commit()
    # Close communication with the PostgreSQL database
    cur.close()

def deleteTable(conn, cur, tablename):
    cur.execute(f'TRUNCATE "{tablename}"; DELETE FROM "{tablename}";')

def create_slayers_records(Slayers):
    records_to_insert = []
    for slayer in Slayers:
        records_to_insert.append((slayer, Slayers[slayer].xp, Slayers[slayer].money, Slayers[slayer].damage_taken, Slayers[slayer].special_stacks, Slayers[slayer].faction, Slayers[slayer].specialization, Slayers[slayer].creation_date, Slayers[slayer].name))
    return records_to_insert

def create_inventory_items_records(Slayers):
    records_to_insert = []
    for slayer in Slayers:
        for item in Slayers[slayer].inventory_items:
            records_to_insert.append((slayer, item))
    return records_to_insert

def create_inventory_specialization_records(Slayers):
    records_to_insert = []
    for slayer in Slayers:
        for item in Slayers[slayer].inventory_specializations:
            records_to_insert.append((slayer, item))
    return records_to_insert

def create_slayers_slots_records(Slayers):
    records_to_insert = []
    for slayer in Slayers:
        for slot in Slayers[slayer].slots:
            if Slayers[slayer].slots[slot] is not None:
                records_to_insert.append((slayer, slot, Slayers[slayer].slots[slot]))
    return records_to_insert
    