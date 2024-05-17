import sqlite3
from classes.Map import Map
from classes.Contract import Contract
from classes.CargoType import CargoType
from classes.Users import Dispatcher, Client

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Client (
            client_id INTEGER PRIMARY KEY,
            c_pib TEXT,
            c_phone_number TEXT,
            c_email TEXT,
            c_password TEXT
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Itinerary (
            itinerary_id INTEGER PRIMARY KEY,
            departure_station TEXT,
            arrival_station TEXT,
            route_length REAL,
            duration REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Payment (
            payment_id INTEGER PRIMARY KEY,
            payment_amount REAL,
            payment_datetime TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CargoType (
            cargo_type_id INTEGER PRIMARY KEY,
            cargo_name TEXT,
            description TEXT,
            dimensions TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cargo (
            cargo_id INTEGER PRIMARY KEY,
            cargo_type_id INTEGER,
            quantity INTEGER,
            weight REAL,
            FOREIGN KEY (cargo_type_id) REFERENCES CargoType(cargo_type_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Contract (
            contract_id INTEGER PRIMARY KEY,
            conclusion_date TEXT,
            client_id INTEGER,
            dispatcher_id INTEGER,
            cargo_id INTEGER,
            payment_id INTEGER,
            itinerary_id INTEGER,
            FOREIGN KEY (client_id) REFERENCES Client(client_id),
            FOREIGN KEY (payment_id) REFERENCES Payment(payment_id),
            FOREIGN KEY (dispatcher_id) REFERENCES Dispatcher(dispatcher_id),
            FOREIGN KEY (cargo_id) REFERENCES Cargo(cargo_id),
            FOREIGN KEY (itinerary_id) REFERENCES Itinerary(itinerary_id)
        )
    ''')


