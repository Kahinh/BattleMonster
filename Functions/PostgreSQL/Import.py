import datetime

def ImportTable(conn, cur, postgres_insert_query, records_to_insert):
    
    try:
        result = cur.executemany(postgres_insert_query, records_to_insert)
        conn.commit()
        print(cur.rowcount, "Record inserted successfully into mobile table")
    except (Exception) as error:
        print("Failed inserting record into mobile table {}".format(error))

