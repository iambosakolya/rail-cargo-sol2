import re
import sqlite3
import database.database_setup
from datetime import datetime
import customtkinter
import customtkinter as ctk
from customtkinter import *
from database.database_setup import cursor, conn

label_style = {
    "text_color": "#000000",
    "anchor": "w",
    "justify": "left",
    "font": ("Arial Rounded MT Bold", 15)}

btn_style = {
    "fg_color": "#000000",
    "hover_color": "#4F2346",
    "text_color": "#ffffff",
    "font": ("Arial Rounded MT Bold", 13)}

entry_style = {
    "fg_color": "#EEEEEE",
    "border_color": "#601E88",
    "border_width": 1,
    "text_color": "#000000"}

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

tables = [
    'Client', 'Dispatcher', 'Itinerary', 'Payment',
    'CargoType', 'Cargo', 'Contract', 'Archive']
current_table_index = 0

def display_tables(table_name, text_box):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    text_box.configure(state='normal')
    text_box.delete(1.0, END)
    text_box.insert(END, f"Table: {table_name}\n")
    text_box.insert(END, " | ".join(columns) + "\n")
    text_box.insert(END, "-" * 100 + "\n")
    for row in rows:
        text_box.insert(END, " | ".join(map(str, row)) + "\n")
    text_box.configure(state='disabled')

def next_table(text_box):
    global current_table_index
    current_table_index = (current_table_index + 1) % len(tables)
    display_tables(tables[current_table_index], text_box)

def previous_table(text_box):
    global current_table_index
    current_table_index = (current_table_index - 1) % len(tables)
    display_tables(tables[current_table_index], text_box)


def contracts_window():
    contracts_window = ctk.CTk()
    contracts_window.title("Contracts")

    screen_width = contracts_window.winfo_screenwidth()
    screen_height = contracts_window.winfo_screenheight()

    app_width = 500
    app_height = 400

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    contracts_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    contracts_window.resizable(0, 0)

    screen_frame = ctk.CTkFrame(master=contracts_window, width=850,
                                height=750, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    text_box = ctk.CTkTextbox(master=screen_frame, wrap="none")
    text_box.pack(expand=True, fill="both")

    button_frame = ctk.CTkFrame(master=screen_frame, fg_color="#FFFFFF")
    button_frame.pack(pady=10)

    prev_button = ctk.CTkButton(master=button_frame, text="Previous", height=40,
                                command=lambda: previous_table(text_box),
                                fg_color="#FFFFFF", hover_color="#897E9B",
                                text_color="#000000", font=("Arial Rounded MT Bold", 13))
    prev_button.pack(side="left", padx=10)

    next_button = ctk.CTkButton(master=button_frame, text="Next", height=40,
                                command=lambda: next_table(text_box),
                                fg_color="#FFFFFF",
                                hover_color="#897E9B", text_color="#000000",
                                font=("Arial Rounded MT Bold", 13))
    next_button.pack(side="left", padx=10)

    display_tables(tables[current_table_index], text_box)
    contracts_window.mainloop()


def show_contracts(user_id, result_textbox):
    query = '''
    SELECT 
        Contract.contract_id, Contract.conclusion_date,
        Client.c_email, Client.c_phone_number, Client.c_pib,
        Dispatcher.d_pib, CargoType.cargo_name, CargoType.description,
        CargoType.dimensions, Cargo.quantity, Cargo.weight,
        Itinerary.departure_station, Itinerary.arrival_station,
        Itinerary.route_length, Itinerary.duration,
        Payment.payment_amount, Payment.payment_datetime
        
    FROM Contract JOIN Client ON Contract.client_id = Client.client_id
    JOIN Dispatcher ON Contract.dispatcher_id = Dispatcher.dispatcher_id
    JOIN Cargo ON Contract.cargo_id = Cargo.cargo_id
    JOIN CargoType ON Cargo.cargo_type_id = CargoType.cargo_type_id
    JOIN Itinerary ON Contract.itinerary_id = Itinerary.itinerary_id
    JOIN Payment ON Contract.payment_id = Payment.payment_id
    WHERE Contract.client_id = ?
    '''

    cursor.execute(query, (user_id,))
    contracts = cursor.fetchall()

    result_textbox.delete("1.0", "end")
    if contracts:
        for contract in contracts:
            contract_data = {
                'contract_id': contract[0], 'conclusion_date': contract[1],
                'client_email': contract[2], 'client_phone': contract[3],
                'client_pib': contract[4], 'dispatcher_pib': contract[5],
                'cargo_name': contract[6], 'cargo_description': contract[7],
                'cargo_dimensions': contract[8], 'cargo_quantity': contract[9],
                'cargo_weight': contract[10], 'departure_station': contract[11],
                'arrival_station': contract[12], 'route_length': contract[13],
                'duration': contract[14], 'payment_amount': contract[15],
                'payment_datetime': contract[16]
            }

            contract_info = f'''
            
Contract ID: {contract_data['contract_id']}
Conclusion date: {contract_data['conclusion_date']}

Client email: {contract_data['client_email']}
Client phone: {contract_data['client_phone']}
Client PIB: {contract_data['client_pib']}

Dispatcher PIB: {contract_data['dispatcher_pib']}

Name: {contract_data['cargo_name']}
Description: {contract_data['cargo_description']}
Dimensions: {contract_data['cargo_dimensions']}
Quantity: {contract_data['cargo_quantity']}
Weight: {contract_data['cargo_weight']}

Departure station: {contract_data['departure_station']}
Arrival station: {contract_data['arrival_station']}
Route length: {contract_data['route_length']}
Duration: {contract_data['duration']}

Payment amount: {contract_data['payment_amount']}
Payment date: {contract_data['payment_datetime']}
'''
            result_textbox.insert("end", contract_info + "\n\n")
    else:
        result_textbox.insert("1.0", "No contracts found")
