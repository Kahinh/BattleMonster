import datetime

def ImportTable(conn, cur, postgres_insert_query, records_to_insert, table):
    
    try:
        result = cur.executemany(postgres_insert_query, records_to_insert)
        conn.commit()
        return f"\n{cur.rowcount} records into {table}"
    except (Exception) as error:
        return f'\nFailed inserting record into mobile table {table}'

