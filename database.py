import sqlite3
from classes.Users import Dispatcher, Client

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Client (
            client_id INTEGER PRIMARY KEY,
            c_pib TEXT,
            c_email TEXT,
            c_password TEXT,
            c_phone_number TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dispatcher (
            dispatcher_id INTEGER PRIMARY KEY,
            d_pib TEXT,
            d_email TEXT,
            d_password TEXT,
            d_phone_number TEXT
        )
    ''')
