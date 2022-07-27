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

def updateTables(Slayers_list):
    conn, cur = getConn()

    #1 on delete les tables
    deleteTable(conn, cur, "Slayers")
    deleteTable(conn, cur, "Slayers_Inventory_Items")
    deleteTable(conn, cur, "Slayers_Inventory_Specializations")
    deleteTable(conn, cur, "Slayers_Slots")

    #2 on import
        #1 Les SLAYERS
    records_to_insert = create_slayers_records(Slayers_list)
    postgres_insert_query = f"""INSERT INTO "Slayers" (slayer_id, xp, money, damage_taken, special_stacks, faction, specialization, creation_date, name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    ImportTable(conn, cur, postgres_insert_query, records_to_insert)
        #2 L'inventory Items
    records_to_insert = create_inventory_items_records(Slayers_list)
    postgres_insert_query = f'INSERT INTO "Slayers_Inventory_Items" (slayer_id, item_id) VALUES (%s,%s)'
    ImportTable(conn, cur, postgres_insert_query, records_to_insert)
        #3 L'inventory Specialization
    records_to_insert = create_inventory_specialization_records(Slayers_list)
    postgres_insert_query = f'INSERT INTO "Slayers_Inventory_Specializations" (slayer_id, specialization_id) VALUES (%s,%s)'
    ImportTable(conn, cur, postgres_insert_query, records_to_insert)
        #4 Les slots
    records_to_insert = create_slayers_slots_records(Slayers_list)
    postgres_insert_query = f'INSERT INTO "Slayers_Slots" (slayer_id, slot, item_id) VALUES (%s,%s,%s)'
    ImportTable(conn, cur, postgres_insert_query, records_to_insert)

    #3 On commit les changes & on close
    closeConn(conn, cur)


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

def create_slayers_records(Slayers_list):
    records_to_insert = []
    for slayer in Slayers_list:
        records_to_insert.append((slayer, Slayers_list[slayer].xp, Slayers_list[slayer].money, Slayers_list[slayer].damage_taken, Slayers_list[slayer].special_stacks, Slayers_list[slayer].faction, Slayers_list[slayer].specialization, Slayers_list[slayer].creation_date, Slayers_list[slayer].name))
    return records_to_insert

def create_inventory_items_records(Slayers_list):
    records_to_insert = []
    for slayer in Slayers_list:
        for item in Slayers_list[slayer].inventory_items:
            records_to_insert.append((slayer, item))
    return records_to_insert

def create_inventory_specialization_records(Slayers_list):
    records_to_insert = []
    for slayer in Slayers_list:
        for item in Slayers_list[slayer].inventory_specializations:
            records_to_insert.append((slayer, item))
    return records_to_insert

def create_slayers_slots_records(Slayers_list):
    records_to_insert = []
    for slayer in Slayers_list:
        for slot in Slayers_list[slayer].slots:
            if Slayers_list[slayer].slots[slot] is not None:
                records_to_insert.append((slayer, slot, Slayers_list[slayer].slots[slot]))
    return records_to_insert
    