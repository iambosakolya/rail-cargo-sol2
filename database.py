import sqlite3
from classes.Users import Dispatcher, Client
from classes.Contract import Contract
from classes.CargoType import CargoType

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Train (
            train_id INTEGER PRIMARY KEY,
            num_of_wagons INTEGER,
            condition TEXT,
            year_of_manufacture INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Itinerary (
            route_id INTEGER PRIMARY KEY,
            departure_station TEXT,
            arrival_station TEXT,
            route_length REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Payment (
            payment_id INTEGER PRIMARY KEY,
            payment_amount REAL,
            payment_datetime TEXT,
            contract_id INTEGER,
            FOREIGN KEY (contract_id) REFERENCES Contract(contract_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CargoType (
            cargo_type_id INTEGER PRIMARY KEY,
            name TEXT,
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
            dep_date TEXT,
            arr_date TEXT,
            client_id INTEGER,
            dispatcher_id INTEGER,
            train_id INTEGER,
            conclusion_date TEXT,
            cargo_id INTEGER,
            itinerary_id INTEGER,
            FOREIGN KEY (client_id) REFERENCES Client(client_id),
            FOREIGN KEY (dispatcher_id) REFERENCES Dispatcher(dispatcher_id),
            FOREIGN KEY (train_id) REFERENCES Train(train_id),
            FOREIGN KEY (cargo_id) REFERENCES Cargo(cargo_id),
            FOREIGN KEY (itinerary_id) REFERENCES Itinerary(route_id)
        )
    ''')

