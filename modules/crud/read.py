import re
import sqlite3
import database.database_setup
from datetime import datetime
import customtkinter
import customtkinter as ctk
from customtkinter import *
from CTkTable import *
from database.database_setup import cursor, conn


class CTkScrollableTable(ctk.CTkScrollableFrame):
    def __init__(self, parent, cell_width=100, cell_height=30, **kwargs):
        super().__init__(parent, **kwargs)
        self.cells = []
        self.cell_width = cell_width
        self.cell_height = cell_height

    def update_table_data(self, data):
        for row in self.cells:
            for cell in row:
                cell.destroy()
        self.cells = []

        for r, row_data in enumerate(data):
            cell_row = []
            for c, cell_data in enumerate(row_data):
                cell = ctk.CTkButton(self, text=str(cell_data), border_width=1, fg_color="#1B1C1C",
                                     hover_color="#1B1C1C", text_color="white", width=self.cell_width, height=self.cell_height)
                cell.grid(row=r, column=c, sticky="nsew")
                cell_row.append(cell)
            self.cells.append(cell_row)

        for i in range(len(data)):
            self.grid_rowconfigure(i, weight=1)
        for j in range(len(data[0])):
            self.grid_columnconfigure(j, weight=1)

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

tables = [
    'Client', 'Dispatcher', 'Itinerary', 'Payment',
    'CargoType', 'Cargo', 'Contract', 'Archive']
current_table_index = 0

def display_tables(table_name, table_widget):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    data = [columns] + rows
    table_widget.update_table_data(data)

def next_table(table_widget):
    global current_table_index
    current_table_index = (current_table_index + 1) % len(tables)
    display_tables(tables[current_table_index], table_widget)

def previous_table(table_widget):
    global current_table_index
    current_table_index = (current_table_index - 1) % len(tables)
    display_tables(tables[current_table_index], table_widget)

def contracts_window():
    app = ctk.CTk()
    app.title("Database table viewer")

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    app_width = 750
    app_height = 650

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    app.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    app.resizable(True, True)

    table_widget = CTkScrollableTable(app, width=app_width-20, height=app_height-100, corner_radius=0, fg_color="transparent")
    table_widget.pack(expand=True, fill='both')

    btn_frame = ctk.CTkFrame(app)
    btn_frame.pack(fill='x', pady=5)

    btn_style = {'fg_color': "#3A3B3C", 'hover_color': "#3A3B3C", 'text_color': "white"}

    prev_btn = ctk.CTkButton(btn_frame, text="Previous table", **btn_style,
                             command=lambda: previous_table(table_widget))
    prev_btn.pack(side='left', padx=5)

    next_btn = ctk.CTkButton(btn_frame, text="Next table", **btn_style,
                             command=lambda: next_table(table_widget))
    next_btn.pack(side='right', padx=5)

    display_tables(tables[current_table_index], table_widget)

    app.mainloop()


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
