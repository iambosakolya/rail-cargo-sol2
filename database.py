import sqlite3
from classes.Map import Map
from classes.Contract import Contract
from classes.CargoType import CargoType
from classes.Users import Dispatcher, Client

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# # Insert example data into Client table
# cursor.execute('''
#     INSERT INTO Client (c_pib, c_phone_number, c_email, c_password)
#     VALUES (?, ?, ?, ?)
# ''', ("Kwe", "0952163862", "we@gmail.com", "password123"))
#
# # Insert example data into Dispatcher table
# cursor.execute('''
#     INSERT INTO Dispatcher (d_pib, d_email, d_password, d_phone_number)
#     VALUES (?, ?, ?, ?)
# ''', ("Dispatcher Name", "dispatcher@example.com", "password123", "0123456789"))
#
# # Insert example data into Itinerary table
# cursor.execute('''
#     INSERT INTO Itinerary (departure_station, arrival_station, route_length, duration)
#     VALUES (?, ?, ?, ?)
# ''', ("Station A", "Station B", 120.5, 3.5))
#
# # Insert example data into Payment table
# cursor.execute('''
#     INSERT INTO Payment (payment_amount, payment_datetime)
#     VALUES (?, ?)
# ''', (1556.0, "2024-05-18 16:47:08"))
#
# # Insert example data into CargoType table
# cursor.execute('''
#     INSERT INTO CargoType (cargo_name, description, dimensions)
#     VALUES (?, ?, ?)
# ''', ("Type A", "Description A", "10x10x10"))
#
# # Insert example data into Cargo table
# cursor.execute('''
#     INSERT INTO Cargo (cargo_type_id, quantity, weight)
#     VALUES (?, ?, ?)
# ''', (1, 100, 200.5))
#
# # Insert example data into Contract table
# cursor.execute('''
#     INSERT INTO Contract (conclusion_date, client_id, dispatcher_id, cargo_id, payment_id, itinerary_id)
#     VALUES (?, ?, ?, ?, ?, ?)
# ''', ("2024-05-18 19:09:48", 1, 1, 1, 1, 1))

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Client (
#         client_id INTEGER PRIMARY KEY,
#         c_pib TEXT,
#         c_phone_number TEXT,
#         c_email TEXT,
#         c_password TEXT
#     )
# ''')
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Dispatcher (
#         dispatcher_id INTEGER PRIMARY KEY,
#         d_pib TEXT,
#         d_email TEXT,
#         d_password TEXT,
#         d_phone_number TEXT
#     )
# ''')
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Itinerary (
#         itinerary_id INTEGER PRIMARY KEY,
#         departure_station TEXT,
#         arrival_station TEXT,
#         route_length REAL,
#         duration REAL
#     )
# ''')
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Payment (
#         payment_id INTEGER PRIMARY KEY,
#         payment_amount REAL,
#         payment_datetime TEXT
#     )
# ''')
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS CargoType (
#         cargo_type_id INTEGER PRIMARY KEY,
#         cargo_name TEXT,
#         description TEXT,
#         dimensions TEXT
#     )
# ''')
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Cargo (
#         cargo_id INTEGER PRIMARY KEY,
#         cargo_type_id INTEGER,
#         quantity INTEGER,
#         weight REAL,
#         FOREIGN KEY (cargo_type_id) REFERENCES CargoType(cargo_type_id)
#     )
# ''')
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Contract (
#         contract_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         conclusion_date TEXT,
#         client_id INTEGER,
#         dispatcher_id INTEGER,
#         cargo_id INTEGER,
#         payment_id INTEGER,
#         itinerary_id INTEGER,
#         FOREIGN KEY (client_id) REFERENCES Client(client_id),
#         FOREIGN KEY (payment_id) REFERENCES Payment(payment_id),
#         FOREIGN KEY (dispatcher_id) REFERENCES Dispatcher(dispatcher_id),
#         FOREIGN KEY (cargo_id) REFERENCES Cargo(cargo_id),
#         FOREIGN KEY (itinerary_id) REFERENCES Itinerary(itinerary_id)
#         )
#     ''')
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Contracts (
#         contract_id TEXT PRIMARY KEY
#     )
# ''')

conn.commit()
def get_db_connection(db_path='data.db'):
    conn = sqlite3.connect(db_path)
    return conn

# def clear_tables(cursor):
#     try:
#         #Очистка таблиць
#         # cursor.execute("DELETE FROM Client")
#         # cursor.execute("DELETE FROM Dispatcher")
#         cursor.execute("DELETE FROM Itinerary")
#         cursor.execute("DELETE FROM Payment")
#         cursor.execute("DELETE FROM CargoType")
#         cursor.execute("DELETE FROM Contracts")
#         cursor.execute("DELETE FROM Cargo")
#         cursor.execute("DELETE FROM Contract")
#         conn.commit()
#         print("All tables cleared successfully.")
#     except sqlite3.Error as e:
#         print("An error occurred:", e)
#
# #Виклик функції для очистки таблиць
# clear_tables(cursor)

# cursor.execute('DROP TABLE IF EXISTS Contract')
# cursor.execute('DROP TABLE IF EXISTS Cargo')
# cursor.execute('DROP TABLE IF EXISTS CargoType')
# cursor.execute('DROP TABLE IF EXISTS Payment')
# cursor.execute('DROP TABLE IF EXISTS Itinerary')
# cursor.execute('DROP TABLE IF EXISTS Dispatcher')
# cursor.execute('DROP TABLE IF EXISTS Client')