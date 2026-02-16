import sqlite3

DB_NAME = 'abid_soreg.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    # Penting: Agar hasil query bisa diakses seperti dictionary (row['column'])
    conn.row_factory = sqlite3.Row 
    return conn