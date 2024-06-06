import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

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
#     )
# ''')
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Archive (
#         contract_id INTEGER PRIMARY KEY,
#         conclusion_date TEXT,
#         archive_date TEXT
#     )
# ''')


# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Admin (
#         admin_id INTEGER PRIMARY KEY,
#         admin_pib TEXT NOT NULL,
#         admin_email TEXT NOT NULL UNIQUE,
#         admin_password TEXT NOT NULL
#     )
# ''')


conn.commit()


# def clear_tables(cursor):
#     try:
#         cursor.execute("DELETE FROM Archive")
#         # cursor.execute("DELETE FROM Dispatcher")
#         # cursor.execute("DELETE FROM Payment")
#         # cursor.execute("DELETE FROM Client")
#         # cursor.execute("DELETE FROM Itinerary")
#         # cursor.execute("DELETE FROM Payment")
#         # cursor.execute("DELETE FROM CargoType")
#         # cursor.execute("DELETE FROM Cargo")
#         # cursor.execute("DELETE FROM Contract")
#         conn.commit()
#         print("All tables cleared successfully.")
#     except sqlite3.Error as e:
#         print("An error occurred:", e)
#
#
# clear_tables(cursor)


# cursor.execute('DROP TABLE IF EXISTS Contract')
# cursor.execute('DROP TABLE IF EXISTS Cargo')
# cursor.execute('DROP TABLE IF EXISTS CargoType')
# cursor.execute('DROP TABLE IF EXISTS Payment')
# cursor.execute('DROP TABLE IF EXISTS Itinerary')
# cursor.execute('DROP TABLE IF EXISTS Dispatcher')
# cursor.execute('DROP TABLE IF EXISTS Client')
# cursor.execute('DROP TABLE IF EXISTS Archive')

