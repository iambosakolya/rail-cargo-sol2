import sqlite3
import customtkinter
import customtkinter as ctk
from customtkinter import *
from classes.Map import Map
from classes.Contract import Contract
from classes.CargoType import CargoType
from CTkMessagebox import CTkMessagebox
from classes.Users import Dispatcher, Client

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

label_style = {
    "text_color": "#000000",
    "anchor": "w",
    "justify": "left",
    "font": ("Arial Rounded MT Bold", 15)
}

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


# 1.Вибір з декількох таблиць із сортуванням

# список контрактів, які були створені заданим диспетчером
def get_contracts_by_pib(dispatcher_pib):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        Contract.contract_id, Contract.conclusion_date,
        Client.c_pib, Client.c_phone_number, 
        Dispatcher.d_pib, Dispatcher.d_email, 
        Itinerary.departure_station, Itinerary.arrival_station, Itinerary.route_length,
        Itinerary.duration, Payment.payment_amount, Payment.payment_datetime, 
        CargoType.cargo_name, CargoType.description, CargoType.dimensions, 
        Cargo.quantity, Cargo.weight
    FROM Contract
    JOIN Dispatcher ON Contract.dispatcher_id = Dispatcher.dispatcher_id
    JOIN Client ON Contract.client_id = Client.client_id
    JOIN Cargo ON Contract.cargo_id = Cargo.cargo_id
    JOIN CargoType ON Cargo.cargo_type_id = CargoType.cargo_type_id
    JOIN Itinerary ON Contract.itinerary_id = Itinerary.itinerary_id
    JOIN Payment ON Contract.payment_id = Payment.payment_id
    WHERE Dispatcher.d_pib = ?
    ORDER BY Contract.conclusion_date;
    '''
    cursor.execute(query, (dispatcher_pib,))
    contracts = cursor.fetchall()
    conn.close()
    return contracts

def find1():
    root = ctk.CTkToplevel()
    root.title("Find contracts by dispatcher PIB")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    app_width = 300
    app_height = 150

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    root.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    root.resizable(0, 0)

    screen_frame = ctk.CTkFrame(master=root, width=300, height=150, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    label = ctk.CTkLabel(screen_frame, text="Enter Dispatcher PIB:")
    label.pack(pady=10)

    entry = ctk.CTkEntry(screen_frame)
    entry.pack(pady=10)

    def on_confirm():
        dispatcher_pib = entry.get()
        if dispatcher_pib:
            root.destroy()
            contracts = get_contracts_by_pib(dispatcher_pib)
            if not contracts:
                CTkMessagebox(message="No contracts found for the given dispatcher PIB!\nTry again!",
                              icon="cancel",
                              option_1="OK")
                return

            result_window = ctk.CTkToplevel()
            result_window.title("Contracts by dispatcher")
            result_window.geometry("450x350")

            screen_frame = ctk.CTkFrame(master=result_window, width=450, height=350, fg_color="#FFFFFF")
            screen_frame.pack_propagate(0)
            screen_frame.pack(expand=True, fill="both", padx=10, pady=10)

            label = ctk.CTkLabel(master=screen_frame, text="A list of contracts that were created"
                                                           "\n by the specified dispatcher", **label_style)
            label.pack(pady=10)

            text_box = ctk.CTkTextbox(master=screen_frame, height=200, wrap="none")
            text_box.pack(expand=True, fill="both", padx=10, pady=10)

            for contract in contracts:
                text_box.insert("end",
                                f"Contract ID: {contract[0]} \nConclusion date: {contract[1]}\n"
                                f"\nClient PIB: {contract[2]} \nPhone: {contract[3]}\n"
                                f"\nDispatcher PIB: {contract[4]} \nEmail: {contract[5]}\n"
                                f"\nFrom: {contract[6]} to {contract[7]}, "
                                f"\nRoute length: {contract[8]} \nDuration: {contract[9]}\n"
                                f"\nPayment amount: {contract[10]} \nPayment time: {contract[11]}\n"
                                f"\nCargo name: {contract[12]} \nDimensions: {contract[14]}\n"
                                f"\nQuantity: {contract[15]} \nWeight: {contract[16]}\n"
                                "---------------------------------\n")


    button = ctk.CTkButton(screen_frame, text="Submit", command=on_confirm, fg_color="#000000",
                           hover_color="#4F2346", text_color="#ffffff", font=("Arial Rounded MT Bold", 13))
    button.pack(pady=10)

    root.mainloop()


# 2. Завдання умови відбору з використанням предиката LIKE

# 3. Завдання умови відбору з використанням предиката BETWEEN

# 4. Агрегатна функція без угруповання
cursor.execute('''
    SELECT COUNT(*) AS contracts_last_month
    FROM Contract
    WHERE conclusion_date BETWEEN DATE('now', '-1 month') AND DATE('now');
''')
contracts_last_month = cursor.fetchone()[0]

# 5. Агрегатна функція з угрупованням
cursor.execute('''
    SELECT Dispatcher.dispatcher_id, Dispatcher.d_pib, COUNT(Contract.contract_id) AS contract_count
    FROM Contract
    JOIN Dispatcher ON Contract.dispatcher_id = Dispatcher.dispatcher_id
    GROUP BY Dispatcher.dispatcher_id;
''')
contracts_by_dispatcher = cursor.fetchall()

# 6. Використання предиката ALL або ANY
cursor.execute('''
    SELECT Dispatcher.dispatcher_id, Dispatcher.d_pib, COUNT(Contract.contract_id) AS contract_count
    FROM Contract
    JOIN Dispatcher ON Contract.dispatcher_id = Dispatcher.dispatcher_id
    GROUP BY Dispatcher.dispatcher_id
    HAVING COUNT(Contract.contract_id) = (
        SELECT MAX(contract_count)
        FROM (
            SELECT COUNT(contract_id) AS contract_count
            FROM Contract
            GROUP BY dispatcher_id
        )
    );
''')
top_dispatcher = cursor.fetchall()

