import re
import sqlite3
import win32ui
import win32con
import win32print
import database
import customtkinter
import customtkinter as ctk
from CTkToolTip import *
from customtkinter import *
from classes.Map import Map
from datetime import datetime
from classes.Calc import Calc
from database import cursor, conn
from classes.Tariff import Tariff
from classes.Register import Register
from classes.Contract import Contract
from database import find1
from classes.ContractInfo import ContractInfo
from classes.ContractInfo import ContractList
from classes.RailCargoSol import RailCargoSol
from classes.CargoType import CargoType
from CTkMessagebox import CTkMessagebox
from classes.Users import Dispatcher,Client

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
    'CargoType', 'Cargo', 'Contract', 'Contracts'
]
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

    screen_frame = ctk.CTkFrame(master=contracts_window, width=850, height=750, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    text_box = ctk.CTkTextbox(master=screen_frame, wrap="none")
    text_box.pack(expand=True, fill="both")

    button_frame = ctk.CTkFrame(master=screen_frame)
    button_frame.pack(pady=10)

    prev_button = ctk.CTkButton(master=button_frame, text="Previous", **btn_style,
                                command=lambda: previous_table(text_box))
    prev_button.pack(side="left", padx=10)

    next_button = ctk.CTkButton(master=button_frame, text="Next", **btn_style,
                                command=lambda: next_table(text_box))
    next_button.pack(side="left", padx=10)

    display_tables(tables[current_table_index], text_box)
    contracts_window.mainloop()

def delete_data(contract_id):
    cursor.execute("SELECT cargo_id, payment_id, itinerary_id "
                   "FROM Contract WHERE contract_id = ?",
                   (contract_id,))
    result = cursor.fetchone()

    if result:
        cargo_id, payment_id, itinerary_id = result

        cursor.execute("SELECT cargo_type_id "
                       "FROM Cargo WHERE cargo_id = ?",
                       (cargo_id,))
        cargo_result = cursor.fetchone()

        if cargo_result:
            cargo_type_id = cargo_result[0]

            cursor.execute("DELETE FROM Cargo WHERE cargo_id = ?", (cargo_id,))
            cursor.execute("DELETE FROM CargoType WHERE cargo_type_id = ?", (cargo_type_id,))
            cursor.execute("DELETE FROM Payment WHERE payment_id = ?", (payment_id,))
            cursor.execute("DELETE FROM Itinerary WHERE itinerary_id = ?", (itinerary_id,))
            cursor.execute("DELETE FROM Contracts WHERE contract_id = ?", (contract_id,))

        cursor.execute("DELETE FROM Contract WHERE contract_id = ?", (contract_id,))

        conn.commit()

        CTkMessagebox(message="Contract with ID {contract_id} deleted successfully", icon="check", option_1="Thanks")
    else:
        CTkMessagebox(message="No contract found with ID {contract_id}", icon="cancel", option_1="OK")
def delete_contract():
    def on_confirm():
        contract_id = entry_d.get()
        delete_data(contract_id)
        dialog.destroy()

    dialog = ctk.CTk()
    dialog.title("Delete contract")

    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()

    dialog_width = 300
    dialog_height = 150

    x_position = (screen_width - dialog_width) // 2
    y_position = (screen_height - dialog_height) // 2

    dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    dialog.resizable(0, 0)

    screen_frame = CTkFrame(master=dialog, width=350, height=200, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    label_d = ctk.CTkLabel(screen_frame, text="Contract ID to delete:", anchor="w",
                           text_color="#000000",justify="left")
    label_d.pack(anchor="w", padx=88, pady=10)

    entry_d = ctk.CTkEntry(screen_frame)
    entry_d.pack(anchor="w", padx=80, pady=5)

    confirm_d = ctk.CTkButton(screen_frame, text="Confirm", fg_color="#000000", hover_color="#4F2346",
                              text_color="#ffffff", command=on_confirm)
    confirm_d.pack(pady=10)

    dialog.mainloop()
def delete_d_data(d_pib):
    cursor.execute("SELECT * FROM Dispatcher "
                   "WHERE d_pib = ?",
                   (d_pib,))
    result = cursor.fetchone()

    if result:
        cursor.execute("DELETE FROM Dispatcher "
                       "WHERE d_pib = ?",
                       (d_pib,))
        conn.commit()
        CTkMessagebox(message=f"Dispatcher with surname '{d_pib}' deleted successfully",
                      icon="check",
                      option_1="Thanks")
    else:
        CTkMessagebox(message=f"No dispatcher found with surname '{d_pib}'",
                      icon="cancel",
                      option_1="OK")
def delete_dispatcher():
    def on_confirm():
        d_pib = entry_d.get()
        delete_d_data(d_pib)
        dialog.destroy()

    dialog = ctk.CTk()
    dialog.title("Delete Dispatcher")

    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()

    dialog_width = 300
    dialog_height = 150

    x_position = (screen_width - dialog_width) // 2
    y_position = (screen_height - dialog_height) // 2

    dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    dialog.resizable(0, 0)

    screen_frame = CTkFrame(master=dialog, width=350, height=200, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    label_d = ctk.CTkLabel(screen_frame, text="Dispatcher pib to delete:", anchor="w",
                           text_color="#000000", justify="left")
    label_d.pack(anchor="w", padx=80, pady=10)

    entry_d = ctk.CTkEntry(screen_frame)
    entry_d.pack(anchor="w", padx=80, pady=5)

    confirm_d = ctk.CTkButton(screen_frame, text="Confirm", fg_color="#000000",
                              hover_color="#4F2346",
                              text_color="#ffffff", command=on_confirm)
    confirm_d.pack(pady=10)

    dialog.mainloop()

def find_dispatcher():
    pib_dialog = CTkInputDialog(text="Enter your full name (PIB):",
                                title="Update info")
    dispatcher_pib = pib_dialog.get_input()

    if dispatcher_pib:
        update_dispatcher(dispatcher_pib)
def update_dispatcher(dispatcher_pib):
    update_dispatcher = CTk()
    update_dispatcher.title(f"Update dispatcher info")

    screen_width = update_dispatcher.winfo_screenwidth()
    screen_height = update_dispatcher.winfo_screenheight()

    app_width = 500
    app_height = 400

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    update_dispatcher.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    update_dispatcher.resizable(0, 0)

    screen_frame = CTkFrame(master=update_dispatcher, width=850, height=750, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    cursor.execute("SELECT d_pib, d_email, d_password, d_phone_number "
                   "FROM Dispatcher "
                   "WHERE d_pib = ?",
                   (dispatcher_pib,))
    dispatcher = cursor.fetchone()

    if dispatcher:
        (existing_pib, existing_email,
         existing_password, existing_phone_number) = dispatcher

        new_name = CTkLabel(master=screen_frame, text="PIB:", **label_style)
        new_name.pack(anchor="w", pady=(18, 0), padx=(50, 0))

        nname_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
        nname_entry.insert(0, existing_pib)
        nname_entry.pack(anchor="w", padx=(50, 0))

        new_phone = CTkLabel(master=screen_frame, text="Phone number(+38):", **label_style)
        new_phone.pack(anchor="w", pady=(18, 0), padx=(50, 0))

        nnew_phone = CTkEntry(master=screen_frame, width=300, **entry_style)
        nnew_phone.insert(0, existing_phone_number)
        nnew_phone.pack(anchor="w", padx=(50, 0))

        CTkLabel(master=screen_frame, text="Email:", **label_style).pack(anchor="w", pady=(18, 0), padx=(50, 0))
        nnew_email = CTkEntry(master=screen_frame, width=300, **entry_style)
        nnew_email.insert(0, existing_email)
        nnew_email.pack(anchor="w", padx=(50, 0))

        CTkLabel(master=screen_frame, text="Password:", **label_style).pack(anchor="w", pady=(15, 0), padx=(50, 0))
        nnew_password = CTkEntry(master=screen_frame, **entry_style, width=300, show="*")
        nnew_password.insert(0, existing_password)
        nnew_password.pack(anchor="w", padx=(50, 0))

        def update_dispatcher_info():
            new_pib = nname_entry.get()
            new_email = nnew_email.get()
            new_password = nnew_password.get()
            new_phone_number = nnew_phone.get()

            if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                CTkMessagebox(message="Invalid email format!",
                              icon="cancel",
                              option_1="OK")
                return

            if len(new_password) < 8:
                CTkMessagebox(message="Password should contain at least 8 characters!",
                              icon="cancel",
                              option_1="OK")
                return

            if len(new_phone_number) < 10 or not new_phone_number.isdigit():
                CTkMessagebox(message="Phone number should contain at least 10 digits!",
                              icon="cancel",
                              option_1="OK")
                return

            cursor.execute(
                "UPDATE Dispatcher SET d_pib = ?, d_email = ?, d_password = ?, d_phone_number = ? "
                "WHERE d_pib = ?",
                (new_pib, new_email, new_password, new_phone_number, dispatcher_pib)
            )
            conn.commit()

            CTkMessagebox(message="Information updated successfully!",
                          icon="check",
                          option_1="Thanks")
            update_dispatcher.destroy()

        update_button = CTkButton(master=screen_frame, text="Update Info", **btn_style,
                                  command=update_dispatcher_info)
        update_button.pack(anchor="w", pady=(20, 0), padx=(50, 0))
    else:
        CTkMessagebox(message="Dispatcher not found!",
                      icon="cancel",
                      option_1="OK")
        update_dispatcher.destroy()

    update_dispatcher.mainloop()

def delete_c_data(c_pib):
    cursor.execute("SELECT * FROM Client "
                   "WHERE c_pib = ?",
                   (c_pib,))
    result = cursor.fetchone()

    if result:
        cursor.execute("DELETE FROM Client "
                       "WHERE c_pib = ?",
                       (c_pib,))
        conn.commit()
        CTkMessagebox(message=f"Client with surname '{c_pib}' deleted successfully",
                      icon="check",
                      option_1="Thanks")
    else:
        CTkMessagebox(message=f"No client found with surname '{c_pib}'",
                      icon="cancel", option_1="OK")
def delete_client():
    def on_confirm():
        c_pib = entry_c.get()
        delete_c_data(c_pib)
        dialog1.destroy()

    dialog1 = ctk.CTk()
    dialog1.title("Delete Client")

    screen_width = dialog1.winfo_screenwidth()
    screen_height = dialog1.winfo_screenheight()

    dialog_width = 300
    dialog_height = 150

    x_position = (screen_width - dialog_width) // 2
    y_position = (screen_height - dialog_height) // 2

    dialog1.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    dialog1.resizable(0, 0)

    screen_frame = CTkFrame(master=dialog1, width=350, height=200, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    label_c = ctk.CTkLabel(screen_frame, text="Client pib to delete:", anchor="w",
                           text_color="#000000", justify="left")
    label_c.pack(anchor="w", padx=90, pady=10)

    entry_c = ctk.CTkEntry(screen_frame)
    entry_c.pack(anchor="w", padx=80, pady=5)

    confirm_c = ctk.CTkButton(screen_frame, text="Confirm", fg_color="#000000", hover_color="#4F2346",
                              text_color="#ffffff", command=on_confirm)
    confirm_c.pack(pady=10)

    dialog1.mainloop()

def create_contract():
    global screen_frame
    window_number = 1
    contract_window = CTk()
    contract_window.title(f"New contract")

    screen_width = contract_window.winfo_screenwidth()
    screen_height = contract_window.winfo_screenheight()

    app_width = 600
    app_height = 500

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    contract_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    contract_window.resizable(0, 0)

    screen_frame = CTkFrame(master=contract_window, width=850, height=750, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    contract_data = {
        "departure_station": "",
        "arrival_station": "",
        "route_length": 0.0,
        "c_pib": "",
        "c_phone_number": "",
        "payment_amount": 0.0,
        "cargo_name": "",
        "quantity": 0,
        "weight": 0.0,
        "client_id": 0,
        "dispatcher_id": 0,
        "conclusion_date": "",
        "cargo_id": 0,
        "itinerary_id": 0
    }

    def next_step():
        nonlocal window_number
        window_number += 1
        show_current_step()

    def show_current_step():
        global screen_frame
        screen_frame.destroy()
        screen_frame = CTkFrame(master=contract_window, width=850, height=750, fg_color="#897E9B")
        screen_frame.pack_propagate(0)
        screen_frame.pack(expand=True, fill="both")

        if window_number == 1:
            # cargo`s name
            type_label = CTkLabel(master=screen_frame, text="Choose your cargo type:", **label_style)
            type_label.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

            type_combobox = CTkComboBox(master=screen_frame, values=['   ', 'Freight', 'Coal', 'Grains', 'Steel', 'Lumber',
                                                                     'Oil', 'Chemicals', 'Machinery',
                                                                     'Automobiles', 'Containers', 'Livestock',
                                                                     'Cement', 'Fertilizer', 'Papers'], width=250)
            type_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=45)

            add_label = CTkLabel(master=screen_frame, text="Or enter new type:", **label_style)
            add_label.place(relx=0, rely=0.1, anchor="w", x=420, y=5)

            type_entry = CTkEntry(master=screen_frame, width=140)
            type_entry.place(relx=0, rely=0.1, anchor="w", x=420, y=45)

            def insert_type(cargo_name, description, dimensions):
                try:
                    cursor.execute("INSERT INTO CargoType (cargo_name, description, dimensions) VALUES (?, ?, ?)",
                                   (cargo_name, description, dimensions))
                    conn.commit()
                    CTkMessagebox(message="Info saved!",
                                  icon="check", option_1="Ok")
                except sqlite3.Error as e:
                    conn.rollback()
                    CTkMessagebox(title="Error", message="Type info is not saved", icon="cancel")
            def insert_cargo(cargo_type_id, quantity, weight):
                cursor.execute("SELECT COUNT(*) FROM CargoType WHERE cargo_type_id = ?", (cargo_type_id,))
                count = cursor.fetchone()[0]
                if count == 0:
                    CTkMessagebox(title="Error", message="cargo_type_id does not exist in the CargoType table",
                                  icon="cancel")
                    return
                cursor.execute("INSERT INTO Cargo (cargo_type_id, quantity, weight) VALUES (?, ?, ?)",
                               (cargo_type_id, quantity, weight))
                conn.commit()

            # adding new type
            def new_type():
                new_cargo_type = type_entry.get().strip()
                if new_cargo_type == "":
                    return
                if not new_cargo_type[0].isupper():
                    tooltip_add.configure(message="Please enter the new cargo type with a capital letter!")
                    return
                existing_cargo_types = type_combobox.cget('values')
                new_cargo_type = type_entry.get()
                existing_cargo_types.append(new_cargo_type)
                type_combobox.configure(values=existing_cargo_types)

            add_btn1 = CTkButton(master=screen_frame, text="Add", width=40, **btn_style, command=new_type)
            add_btn1.place(relx=0, rely=0.1, anchor="w", x=350, y=45)

            tooltip_add = CTkToolTip(add_btn1, message="Please enter cargo type with a capital letter and in plural!"
                                                       "\n                                                   "
                                                       "\nNot allowed: \nMinerals, \nExplosives, \nRadioactives,"
                                                       "\nToxics, \nPerishables, \nFirearms,\nChemicals, \nAmmunition, \nNarcotics"
                                                       "\nPoisons, \nWaste materials, \nLiquids, \nGases")
            # adding new type

            cargo_type_checked = False
            def cargo_type_check(cargo_obj):
                global cargo_type_checked
                if cargo_obj.isCargoType():
                    cargo_type_checked = True
                    CTkMessagebox(message="Cargo type is available", icon="check", option_1="Thanks")
                    save.configure(state="normal")
                else:
                    cargo_type_checked = False
                    CTkMessagebox(title="Error",
                                  message="This cargo type is not available!", icon="cancel")
                    save.configure(state="disabled")

            # adding data to table "cargo types"
            def save_cargo():
                global cargo_type_checked

                if not cargo_type_checked:
                    CTkMessagebox(title="Error",
                                  message="Please check cargo type availability first",
                                  icon="cancel")
                    return

                if (not type_combobox.get().strip()
                        or not dim_entry.get()
                        or not weight_input.get()
                        or not quantity_input.get()):
                    CTkMessagebox(title="Error",
                                  message="Please fill in all fields",
                                  icon="cancel")
                    return

                if not weight_input.get().isdigit():
                    CTkMessagebox(title="Error",
                                  message="Weight should contain only digits",
                                  icon="cancel")
                    return

                if not quantity_input.get().isdigit():
                    CTkMessagebox(title="Error",
                                  message="Quantity should contain only digits",
                                  icon="cancel")
                    return

                if not dim_entry.get().replace('*', '').isdigit():
                    CTkMessagebox(title="Error",
                                  message="Dimensions should contain only digits or '*'",
                                  icon="cancel")
                    return

                # save cargo type data
                cargo_name = type_combobox.get().strip()
                description = desc_entry.get()
                dimensions = dim_entry.get()
                insert_type(cargo_name, description, dimensions)
                cargo_obj = CargoType(cargo_name, description,
                                      dimensions, quantity_input.get(), weight_input.get())

                # save cargo data
                selected_type = type_combobox.get()
                quantity = quantity_input.get()
                weight = weight_input.get()
                cursor.execute("SELECT cargo_type_id FROM CargoType WHERE cargo_name = ?",
                               (selected_type,))
                result = cursor.fetchone()

                if result is None:
                    CTkMessagebox(title="Error",
                                  message="Selected cargo type not found",
                                  icon="cancel")
                    return

                cargo_type_id = result[0]
                insert_cargo(cargo_type_id, quantity, weight)

            # buttons
            check_btn = CTkButton(master=screen_frame, text="Check availability", **btn_style,
                                  command=lambda: cargo_type_check(CargoType(type_combobox.get(),
                                  dim_entry.get(), weight_input.get(), quantity_input.get(), desc_entry.get())))
            check_btn.place(relx=0, rely=0.1, anchor="w", x=30, y=300)

            save = CTkButton(master=screen_frame, text="Save type", **btn_style, width=90, command=save_cargo)
            save.place(relx=0, rely=0.1, anchor="w", x=200, y=300)
            save.configure(state="disabled")

            reminder0 = CTkLabel(master=screen_frame, text="Don`t forget to save the type!",
                                text_color="#CCCCCC", anchor="w", justify="left",
                                 font=("Arial Rounded MT Bold", 14))
            reminder0.place(relx=0, rely=0.1, anchor="w", x=300, y=300)

            # cargo`s dimension
            type_label1 = CTkLabel(master=screen_frame, text="Enter dimensions:", **label_style)
            type_label1.place(relx=0, rely=0.1, anchor="w", x=30, y=95)

            dim_entry = CTkEntry(master=screen_frame,width=150, height=30, **entry_style)
            dim_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=135)

            # cargo`s description
            type_label2 = CTkLabel(master=screen_frame, text="Add description (if necessary):", **label_style)
            type_label2.place(relx=0, rely=0.1, anchor="w", x=30, y=185)

            desc_entry = CTkEntry(master=screen_frame, width=350, height=50, **entry_style)
            desc_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=225)

            # cargo`s weight
            weight_label = CTkLabel(master=screen_frame, text="Enter weight:(tons)",
                                    **label_style)
            weight_label.place(relx=0, rely=0.1, anchor="w", x=420, y=95)

            weight_input = CTkEntry(master=screen_frame, width=150, height=30, **entry_style)
            weight_input.place(relx=0, rely=0.1, anchor="w", x=420, y=135)

            # cargo`s quantity
            quantity_label = CTkLabel(master=screen_frame, text="Enter quantity:", **label_style)
            quantity_label.place(relx=0, rely=0.1, anchor="w", x=420, y=185)

            quantity_input = CTkEntry(master=screen_frame, width=150, height=30, **entry_style)
            quantity_input.place(relx=0, rely=0.1, anchor="w", x=420, y=225)

            next_btn = CTkButton(master=screen_frame, text="Next step", **btn_style, command=next_step)
            next_btn.place(relx=0, rely=0.1, anchor="w", x=420, y=400)

        elif window_number == 2:
            def find_connection():
                dep_station = dep_entry.get()
                arr_station = arr_entry.get()

                if dep_station and dep_station[0].islower():
                    CTkMessagebox(message="Please enter the departure station with a capital letter!",
                                  icon="cancel")
                    return
                if arr_station and arr_station[0].islower():
                    CTkMessagebox(message="Please enter the arrival station with a capital letter!",
                                  icon="cancel")
                    return

                map_obj = Map(dep_station, arr_station, 0, 0)
                is_connection, distance, duration = map_obj.is_station()

                if is_connection:
                    message = (f"Railway connection exists!\nDistance: {distance} km"
                               f"\nDuration: {duration} hours")
                    CTkMessagebox(message=message, icon="check", option_1="Ok")
                    result_text.delete("1.0", "end")
                    result_text.insert("1.0", message)
                    save_btn.configure(state="normal")
                else:
                    CTkMessagebox(title="Error",
                                  message="Railway connection doesn't exist",
                                  icon="cancel")
                    save_btn.configure(state="disabled")

            def save_route():
                dep_station = dep_entry.get()
                arr_station = arr_entry.get()

                map = Map(dep_station, arr_station, 0, 0)
                is_connection, distance, duration = map.is_station()

                if is_connection:
                    cursor.execute(
                        "INSERT INTO Itinerary (departure_station, arrival_station, route_length, duration) "
                        "VALUES (?, ?, ?, ?)",
                        (dep_station, arr_station, distance, duration))
                    conn.commit()
                    CTkMessagebox(message="Route saved successfully!", icon="info", option_1="Ok")
                else:
                    CTkMessagebox(title="Error", message="Cannot save route. Railway connection doesn't exist",
                                  icon="cancel")

            label1 = CTkLabel(master=screen_frame,
                              text="Enter the stations and check if the railway connection exists:",
                              text_color="#000000", anchor="w", justify="left",
                              font=("Arial Rounded MT Bold", 17))
            label1.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

            label2 = CTkLabel(master=screen_frame,
                              text="Reminder:\nSystem works only with ukrainian cities."
                                   "\nBegin with capital letter.",
                              text_color="#CCCCCC", anchor="w", justify="left",
                              font=("Arial Rounded MT Bold", 14))
            label2.place(relx=0, rely=0.1, anchor="w", x=30, y=60)

            dep_label = CTkLabel(master=screen_frame, text="Departure station:", **label_style)
            dep_label.place(relx=0, rely=0.1, anchor="w", x=30, y=130)

            dep_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            dep_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=160)

            arr_label = CTkLabel(master=screen_frame, text="Arrival station:", **label_style)
            arr_label.place(relx=0, rely=0.1, anchor="w", x=30, y=190)

            arr_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            arr_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=220)

            result_text = CTkTextbox(master=screen_frame, width=180, height=200)
            result_text.place(relx=0, rely=0.1, anchor="w", x=370, y=170)

            # buttons
            check_btn1 = CTkButton(master=screen_frame, text="Check availability", **btn_style,
                                   command=find_connection).place(relx=0, rely=0.1, anchor="w", x=30, y=320)

            save_btn = CTkButton(master=screen_frame, text="Save route", width=90, **btn_style,
                                 command=save_route, state="disabled")
            save_btn.place(relx=0, rely=0.1, anchor="w", x=200, y=320)

            reminder = CTkLabel(master=screen_frame, text="Dont forget to save the route!:",
                                text_color="#CCCCCC", anchor="w", justify="left",
                                font=("Arial Rounded MT Bold", 14))
            reminder.place(relx=0, rely=0.1, anchor="w", x=200, y=350)

            next_btn = CTkButton(master=screen_frame, text="Next step", **btn_style,
                                 command=next_step).place(relx=0, rely=0.1, anchor="w", x=420, y=400)

        elif window_number == 3:

            payment_label = CTkLabel(master=screen_frame, text="Almost done!"
                                                               "\nNow make the payment",
                                    text_color="#000000", anchor="w",
                                    justify="left",
                                    font=("Arial Rounded MT Bold", 18))
            payment_label.place(relx=0, rely=0.1, anchor="w", x=30, y=10)

            list_label = CTkLabel(master=screen_frame,
                                  text="Click button 'Accept payment' to see the price for the tranportation"
                                       "\nand save the payment",  text_color="#CCCCCC", anchor="w", justify="left",
                                  font=("Arial Rounded MT Bold", 14))
            list_label.place(relx=0, rely=0.1, anchor="w", x=30, y=80)

            def record_payment(calculated_tariff):
                try:
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()

                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    cursor.execute(
                        "INSERT INTO Payment (payment_amount, payment_datetime) VALUES (?, ?)",
                        (calculated_tariff, current_datetime))

                    conn.commit()
                    conn.close()
                    CTkMessagebox(message="Payment recorded successfully!", icon="check", option_1="Thanks")
                except sqlite3.Error as e:
                    CTkMessagebox(message="Payment is not recorded!", icon="cancel", option_1="OK")

            def calculate_tariff():
                global calculated_tariff
                try:
                    cursor.execute(
                        "SELECT ct.cargo_name, c.weight "
                        "FROM Cargo c INNER JOIN CargoType ct "
                        "ON c.cargo_type_id = ct.cargo_type_id "
                        "ORDER BY c.rowid DESC LIMIT 1")
                    cargo_data = cursor.fetchone()

                    cursor.execute("SELECT route_length, duration "
                                   "FROM Itinerary "
                                   "ORDER BY rowid DESC LIMIT 1")
                    route_data = cursor.fetchone()
                    display_data(cargo_data, route_data)

                    if cargo_data and route_data:
                        cargo_type, weight = cargo_data
                        distance, duration = route_data

                        calc_obj = Calc(None, distance,
                                        None, duration, cargo_type, weight)
                        calc_obj.calculate_price()
                        calculated_tariff = calc_obj.get_price()
                        record_payment(calculated_tariff)

                        textbox1.configure(state="normal")
                        textbox1.delete("1.0", "end")
                        textbox1.insert("end", f"Calculated tariff: "
                                               f"{calculated_tariff}$")
                        textbox1.configure(state="disabled")

                        display_data(cargo_data, route_data)

                except sqlite3.Error as e:
                    print("Error:", e)
            def display_data(cargo_data, route_data):
                if cargo_data and route_data:
                    cargo_type, weight = cargo_data
                    distance, duration = route_data

                    textbox.configure(state="normal")
                    textbox.delete("1.0", "end")
                    headers = (f"{'Cargo Type':<35}{'Weight':<35}"
                               f"{'Distance':<35}{'Duration':<35}\n")
                    table_data = headers
                    row_data = (f"{cargo_type:<40}{weight:<40}"
                                f"{distance:<40}{duration:<40}\n")
                    table_data += row_data
                    textbox.insert("end", table_data)
                    textbox.configure(state="disabled")
            def display():
                try:
                    calculate_tariff()
                except sqlite3.Error as e:
                    CTkMessagebox(message="Error", icon="cancel", option_1="OK")

            display_button = CTkButton(master=screen_frame, text="Accept payment", **btn_style,
                                       width=90, command=display)
            display_button.place(relx=0, rely=0.1, anchor="w", x=30, y=350)

            textbox = CTkTextbox(master=screen_frame, width=500, height=80)
            textbox.place(relx=0, rely=0.1, anchor="w", x=30, y=155)
            textbox1 = CTkTextbox(master=screen_frame, width=500, height=80)
            textbox1.place(relx=0, rely=0.1, anchor="w", x=30, y=255)

            next_btn = CTkButton(master=screen_frame, text="Next step", **btn_style, command=next_step)
            next_btn.place(relx=0, rely=0.1, anchor="w", x=420, y=400)

        elif window_number == 4:

            cl_label = CTkLabel(master=screen_frame, text="Register the client:",
                               text_color="#000000", anchor="w",
                               justify="left",
                               font=("Arial Rounded MT Bold", 18))
            cl_label.place(relx=0, rely=0.1, anchor="w", x=30, y=2)

            cl_label1 = CTkLabel(master=screen_frame, text="Last step!"
                                                           "\nYou have to register the client to the system"
                                                           "\nAfter 'Next step' the contract will be saved",
                                 text_color="#CCCCCC", anchor="w", justify="left",
                                 font=("Arial Rounded MT Bold", 14))
            cl_label1.place(relx=0, rely=0.1, anchor="w", x=30, y=50)

            cl_label2 = CTkLabel(master=screen_frame, text="*Reminder"
                                                           "\nIf the client already exists"
                                                           "\njust skip this step",
                                 text_color="#CCCCCC", anchor="w", justify="left",
                                 font=("Arial Rounded MT Bold", 14))
            cl_label2.place(relx=0, rely=0.1, anchor="w", x=400, y=5)


            rec_pib = CTkLabel(master=screen_frame, text="Enter pib:", **label_style)
            rec_pib.place(relx=0, rely=0.1, anchor="w", x=30, y=100)
            pib_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            pib_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=135)


            rec_ph = CTkLabel(master=screen_frame, text="Enter phone number:", **label_style)
            rec_ph.place(relx=0, rely=0.1, anchor="w", x=30, y=170)
            ph_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            ph_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=205)


            rec_email = CTkLabel(master=screen_frame, text="Enter email:", **label_style)
            rec_email.place(relx=0, rely=0.1, anchor="w", x=30, y=240)
            email_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            email_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=275)


            rec_password = CTkLabel(master=screen_frame, text="Enter password:", **label_style)
            rec_password.place(relx=0, rely=0.1, anchor="w", x=30, y=310)
            password_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            password_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=345)

            def create_client(cursor):
                pib = pib_entry.get().strip()
                phone_number = ph_entry.get().strip()
                email = email_entry.get().strip()
                password = password_entry.get().strip()

                try:
                    if not pib or not phone_number or not email or not password:
                        CTkMessagebox(message="Please fill in all the fields",
                                      icon="cancel",
                                      option_1="OK")
                        return
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        CTkMessagebox(message="Invalid email format!",
                                      icon="cancel",
                                      option_1="OK")
                        return
                    if len(password) < 8:
                        CTkMessagebox(message="Password should contain at least 8 characters!",
                                      icon="cancel",
                                      option_1="OK")
                        return
                    if len(phone_number) < 10 or not phone_number.isdigit():
                        CTkMessagebox(message="Phone number should contain at least 10 digits!",
                                      icon="cancel",
                                      option_1="OK")
                        return

                    cursor.execute("SELECT * FROM Client WHERE c_email = ? OR c_phone_number = ?",
                                   (email, phone_number))
                    existing_client = cursor.fetchone()
                    if existing_client:
                        client_id = existing_client[0]
                        CTkMessagebox(message="This user already exists! ", icon="cancel", option_1="OK")
                    else:
                        cursor.execute(
                            "INSERT INTO Client (c_pib, c_phone_number, c_email, c_password) VALUES (?, ?, ?, ?)",
                            (pib, phone_number, email, password))
                        conn.commit()
                        client_id = cursor.lastrowid
                        CTkMessagebox(message="Registration successful!", icon="check", option_1="Thanks")
                except sqlite3.Error as e:
                    CTkMessagebox(message="Error", icon="cancel", option_1="OK")

            # buttons
            save_client = CTkButton(master=screen_frame, text="Register client", **btn_style,
                                    command=lambda: create_client(cursor))
            save_client.place(relx=0, rely=0.1, anchor="w", x=30, y=400)

            next_btn = CTkButton(master=screen_frame, text="Next step", **btn_style,
                                 command=next_step).place(relx=0, rely=0.1, anchor="w", x=420, y=400)

        elif window_number == 5:
            #contract
            cursor.execute("SELECT client_id "
                           "FROM Client "
                           "ORDER BY client_id "
                           "DESC LIMIT 1")
            client_id = cursor.fetchone()[0]

            cursor.execute("SELECT payment_id "
                           "FROM Payment "
                           "ORDER BY payment_id "
                           "DESC LIMIT 1")
            payment_id = cursor.fetchone()[0]

            cursor.execute("SELECT cargo_id "
                           "FROM Cargo "
                           "ORDER BY cargo_id "
                           "DESC LIMIT 1")
            cargo_id = cursor.fetchone()[0]

            cursor.execute("SELECT itinerary_id "
                           "FROM Itinerary "
                           "ORDER BY itinerary_id "
                           "DESC LIMIT 1")
            itinerary_id = cursor.fetchone()[0]

            def create(cursor, client_id, payment_id,
                       dispatcher_id, cargo_id, itinerary_id):
                contract_list = ContractList()
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    cursor.execute(
                        "INSERT INTO Contract (conclusion_date, client_id,"
                        " payment_id, dispatcher_id, cargo_id, itinerary_id) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (current_datetime, client_id, payment_id,
                         dispatcher_id, cargo_id, itinerary_id))
                    conn.commit()
                    contract_id = cursor.lastrowid

                    cursor.execute("SELECT quantity, weight, cargo_type_id "
                                   "FROM Cargo "
                                   "WHERE cargo_id = ?", (cargo_id,))
                    cargo_data1 = cursor.fetchone()
                    quantity, weight, cargo_type_id = cargo_data1

                    cursor.execute("SELECT cargo_name, description, dimensions "
                                   "FROM CargoType "
                                   "WHERE cargo_type_id = ?",
                                   (cargo_type_id,))
                    cargo_data2 = cursor.fetchone()
                    cargo_obj = CargoType(cargo_data2[0], cargo_data2[1],
                                          cargo_data2[2], quantity, weight)

                    cursor.execute("SELECT departure_station, arrival_station,"
                                   " route_length, duration "
                        "FROM Itinerary "
                        "WHERE itinerary_id = ?",
                        (itinerary_id,))
                    map_data = cursor.fetchone()
                    map_obj = Map(*map_data)

                    cursor.execute("SELECT payment_amount, payment_datetime "
                                   "FROM Payment "
                                   "WHERE payment_id = ?",
                                   (payment_id,))
                    payment_data = cursor.fetchone()
                    calc_obj = Calc(payment_data[0], payment_data[1], cargo_data2[0],
                                    map_data[2], map_data[3], weight)

                    cursor.execute("SELECT c_email, c_phone_number, c_pib "
                                   "FROM Client "
                                   "WHERE client_id = ?",
                                   (client_id,))
                    client_data = cursor.fetchone()
                    c_email, c_phone_number, pib_c = client_data

                    cursor.execute("SELECT d_pib "
                                   "FROM Dispatcher "
                                   "WHERE dispatcher_id = ?", (dispatcher_id,))
                    dispatcher_data = cursor.fetchone()
                    pib_d = dispatcher_data[0]

                    contract = Contract(contract_id, current_datetime,
                                        pib_c, c_phone_number, c_email,
                                        pib_d, cargo_obj, map_obj, calc_obj)

                    register = Register(contract, map_obj, calc_obj,contract_list)

                    contract_info = ContractInfo(contract_id)
                    contract_list.add_contract(contract_info)

                    CTkMessagebox(message="Contract saved successfully!",
                                  icon="check",
                                  option_1="Thanks")
                    return contract_id
                except sqlite3.Error as e:
                    CTkMessagebox(message="Error: " + str(e),
                                  icon="cancel",
                                  option_1="OK")
                    return None

            def enter_pib():
                def save_dispatcher_id():
                    try:
                        dispatcher_pib = pib_entry.get()
                        client_phone = client_phone_entry.get()
                        cursor.execute("SELECT dispatcher_id "
                                       "FROM Dispatcher "
                                       "WHERE d_pib = ?",
                                       (dispatcher_pib,))
                        dispatcher_data = cursor.fetchone()

                        if dispatcher_data:
                            dispatcher_id = dispatcher_data[0]
                            cursor.execute("SELECT client_id "
                                           "FROM Client "
                                           "WHERE c_phone_number = ?",
                                           (client_phone,))
                            client_data = cursor.fetchone()

                            if client_data:
                                client_id = client_data[0]
                                contract_id = create(cursor, client_id, payment_id,
                                                     dispatcher_id, cargo_id, itinerary_id)

                                if contract_id:
                                    print_button(contract_id)
                                dialog_window.destroy()
                            else:
                                CTkMessagebox(message="Client with provided phone number not found!",
                                              icon="cancel",
                                              option_1="OK")
                        else:
                            CTkMessagebox(message="Dispatcher with provided PIB not found!",
                                          icon="cancel",
                                          option_1="OK")
                    except sqlite3.Error as e:
                        CTkMessagebox(message="Database error: " + str(e),
                                      icon="cancel",
                                      option_1="OK")

                def on_closing():
                    dialog_window.destroy()

                dialog_window = ctk.CTk()
                dialog_window.title("Attention")

                screen_width = dialog_window.winfo_screenwidth()
                screen_height = dialog_window.winfo_screenheight()

                dialog_width = 300
                dialog_height = 200

                x_position = (screen_width - dialog_width) // 2
                y_position = (screen_height - dialog_height) // 2
                dialog_window.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
                dialog_window.resizable(0, 0)

                pib_label = ctk.CTkLabel(dialog_window, text="Confirm your PIB one more time:")
                pib_label.pack()

                pib_entry = ctk.CTkEntry(dialog_window)
                pib_entry.pack()

                client_phone_label = ctk.CTkLabel(dialog_window, text="Phone number of the client:")
                client_phone_label.pack()

                client_phone_entry = ctk.CTkEntry(dialog_window)
                client_phone_entry.pack()

                confirm_button = ctk.CTkButton(dialog_window, text="Confirm", command=save_dispatcher_id)
                confirm_button.pack()
                dialog_window.mainloop()

            savec_btn = CTkButton(master=screen_frame, text="Save contract",
                                  **btn_style, command=enter_pib)
            savec_btn.place(relx=0, rely=0, anchor="w", x=220, y=180)

            def get_contract_data(cursor, contract_id):
                try:
                    cursor.execute("SELECT * FROM Contract "
                                   "WHERE contract_id = ?", (contract_id,))
                    contract_data = cursor.fetchone()
                    if not contract_data:
                        print("No contract data found.")
                        return None, None, None, None, None, None, None


                    cursor.execute("SELECT * FROM Client "
                                   "WHERE client_id = ?", (contract_data[2],))
                    client_data = cursor.fetchone()
                    if not client_data:
                        print("No client data found.")
                        return contract_data, None, None, None, None, None, None


                    cursor.execute("SELECT * FROM Payment "
                                   "WHERE payment_id = ?", (contract_data[5],))
                    payment_data = cursor.fetchone()
                    if not payment_data:
                        print("No payment data found.")
                        return contract_data, client_data, None, None, None, None, None


                    cursor.execute("SELECT * FROM Dispatcher "
                                   "WHERE dispatcher_id = ?", (contract_data[3],))
                    dispatcher_data = cursor.fetchone()
                    if not dispatcher_data:
                        print("No dispatcher data found.")
                        return contract_data, client_data, payment_data, None, None, None, None


                    cursor.execute("SELECT * FROM Cargo "
                                   "WHERE cargo_id = ?", (contract_data[4],))
                    cargo_data = cursor.fetchone()
                    if not cargo_data:
                        print("No cargo data found.")
                        return (contract_data, client_data, payment_data,
                                dispatcher_data, None, None, None)


                    cursor.execute("SELECT * FROM CargoType "
                                   "WHERE cargo_type_id = ?", (cargo_data[1],))
                    cargo_type_data = cursor.fetchone()
                    if not cargo_type_data:
                        print("No cargo type data found.")
                        return (contract_data, client_data, payment_data,
                                dispatcher_data, cargo_data, None, None)


                    cursor.execute("SELECT * FROM Itinerary "
                                   "WHERE itinerary_id = ?", (contract_data[6],))
                    itinerary_data = cursor.fetchone()
                    if not itinerary_data:
                        print("No itinerary data found.")
                        return (contract_data, client_data, payment_data,
                                dispatcher_data, cargo_data, cargo_type_data, None)


                    return (contract_data, client_data, payment_data,
                            dispatcher_data, cargo_data, cargo_type_data, itinerary_data)
                except sqlite3.Error as e:
                    print(f"Error fetching contract data: {e}")
                    return None, None, None, None, None, None, None

            def finish():
                contract_window.destroy()

            def print_contract(contract_id):
                try:
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()

                    (contract_data, client_data, payment_data, dispatcher_data,
                     cargo_data, cargo_type_data, itinerary_data) = get_contract_data(
                        cursor, contract_id)

                    if not contract_data:
                        CTkMessagebox(message="Failed to fetch contract data",
                                      icon="cancel",
                                      option_1="OK")
                        return

                    company_name = "Rail Cargo Solutions"
                    head_office = "Head office: Odesa, Ukraine"

                    client_info = (
                        f"\nPIB: {client_data[1]}\nPhone number: {client_data[2]}"
                        f"\nEmail: {client_data[3]}") \
                        if client_data else "Client information not available"


                    payment_info = (
                        f"\nPayment amount: {payment_data[1]} UAH"
                        f"\nPayment date: {payment_data[2]}") \
                        if payment_data else "Payment information not available"


                    dispatcher_info = f"\nPIB: {dispatcher_data[1]}" \
                        if dispatcher_data else "Dispatcher information not available"


                    cargo_info = (
                        f"\nCargo type: {cargo_type_data[1]}"
                        f"\nDescription: {cargo_type_data[2]}"
                        f"\nDimensions: {cargo_type_data[3]} metres"
                        f"\nQuantity: {cargo_data[2]}\nWeight: {cargo_data[3]} tons") \
                        if cargo_data and cargo_type_data else "Cargo information not available"


                    itinerary_info = (
                        f"\nDeparture station: {itinerary_data[1]}"
                        f"\nArrival station: {itinerary_data[2]}"
                        f"\nRoute length: {itinerary_data[3]} km"
                        f"\nDuration: {itinerary_data[4]} hour(s)") \
                        if itinerary_data else "Itinerary information not available"


                    contract_details = f"""
                    
            Contract ID: {contract_data[0]}
            Conclusion Date: {contract_data[1]}

            \tClient Information:
            {client_info}

            \tDispatcher Information:
            {dispatcher_info}

            \tCargo Information:
            {cargo_info}

            \tItinerary Information:
            {itinerary_info}

            \tPayment Information:
            {payment_info}
            """
                    hdc = win32ui.CreateDC()
                    hdc.CreatePrinterDC(win32print.GetDefaultPrinter())
                    hdc.StartDoc("Contract")
                    hdc.StartPage()

                    hdc.SetMapMode(win32con.MM_TWIPS)

                    header_font = win32ui.CreateFont({
                        "name": "Arial",
                        "height": 400,
                        "weight": win32con.FW_BOLD,
                    })
                    hdc.SelectObject(header_font)
                    hdc.TextOut(1000, -1000, company_name)
                    hdc.TextOut(1000, -1500, head_office)

                    body_font = win32ui.CreateFont({
                        "name": "Arial",
                        "height": 320,
                        "weight": win32con.FW_NORMAL,
                    })

                    bold_body_font = win32ui.CreateFont({
                        "name": "Arial",
                        "height": 320,
                        "weight": win32con.FW_BOLD,
                    })

                    y_offset = -2000

                    for line in contract_details.split('\n'):
                        if (" Information:" in line or "Contract ID" in line
                                or "Conclusion Date" in line):
                            hdc.SelectObject(bold_body_font)
                        else:
                            hdc.SelectObject(body_font)
                        hdc.TextOut(1000, y_offset, line)
                        y_offset -= 300

                    hdc.EndPage()
                    hdc.EndDoc()
                    hdc.DeleteDC()

                    conn.close()
                except Exception as e:
                    print(f"Error in print_contract: {e}")
            def print_button(contract_id):
                print_btn = CTkButton(master=screen_frame,
                                      text="Print contract", **btn_style,
                                      command=lambda: print_contract(contract_id))
                print_btn.place(relx=0, rely=0, anchor="w", x=220, y=230)

            finish_btn = CTkButton(master=screen_frame, text="Finish", **btn_style, command=finish)
            finish_btn.place(relx=0, rely=0, anchor="w", x=220, y=280)

    show_current_step()
    contract_window.mainloop()
def modifying_contract():
    global screen_frame
    window_number = 1
    cont_window = CTk()
    cont_window.title("Updating the contract")

    screen_width = cont_window.winfo_screenwidth()
    screen_height = cont_window.winfo_screenheight()

    app_width = 600
    app_height = 500

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    cont_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    cont_window.resizable(0, 0)

    screen_frame = CTkFrame(master=cont_window, width=850, height=750, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    dialog = CTkInputDialog(text="Enter contract ID:", title="Update contract")
    contract_id = dialog.get_input()

    if contract_id is None:
        return

    contract_id = int(contract_id)
    def get_contract_data(cursor, contract_id):
        try:
            cursor.execute("SELECT * FROM Contract WHERE contract_id = ?", (contract_id,))
            contract_data = cursor.fetchone()
            if not contract_data:
                print("No contract data found.")
                return None, None, None, None, None, None, None

            cursor.execute("SELECT * FROM Client WHERE client_id = ?", (contract_data[2],))
            client_data = cursor.fetchone()
            if not client_data:
                print("No client data found.")
                return contract_data, None, None, None, None, None, None

            cursor.execute("SELECT * FROM Payment WHERE payment_id = ?", (contract_data[5],))
            payment_data = cursor.fetchone()
            if not payment_data:
                print("No payment data found.")
                return contract_data, client_data, None, None, None, None, None

            cursor.execute("SELECT * FROM Dispatcher WHERE dispatcher_id = ?", (contract_data[3],))
            dispatcher_data = cursor.fetchone()
            if not dispatcher_data:
                print("No dispatcher data found.")
                return contract_data, client_data, payment_data, None, None, None, None

            cursor.execute("SELECT * FROM Cargo WHERE cargo_id = ?", (contract_data[4],))
            cargo_data = cursor.fetchone()
            if not cargo_data:
                print("No cargo data found.")
                return contract_data, client_data, payment_data, dispatcher_data, None, None, None

            cursor.execute("SELECT * FROM CargoType WHERE cargo_type_id = ?", (cargo_data[1],))
            cargo_type_data = cursor.fetchone()
            if not cargo_type_data:
                print("No cargo type data found.")
                return contract_data, client_data, payment_data, dispatcher_data, cargo_data, None, None

            cursor.execute("SELECT * FROM Itinerary WHERE itinerary_id = ?", (contract_data[6],))
            itinerary_data = cursor.fetchone()
            if not itinerary_data:
                print("No itinerary data found.")
                return contract_data, client_data, payment_data, dispatcher_data, cargo_data, cargo_type_data, None

            return contract_data, client_data, payment_data, dispatcher_data, cargo_data, cargo_type_data, itinerary_data
        except sqlite3.Error as e:
            print(f"Error fetching contract data: {e}")
            return None, None, None, None, None, None, None

    (contract_data, client_data, payment_data,
     dispatcher_data, cargo_data, cargo_type_data,
     itinerary_data) = get_contract_data(cursor, contract_id)

    if not contract_data:
        CTkMessagebox(title="Error", message="Contract not found", icon="cancel")
        return

    def next_step():
        nonlocal window_number
        window_number += 1
        show_current_step()

    def show_current_step():
        global screen_frame
        screen_frame.destroy()
        screen_frame = CTkFrame(master=cont_window, width=850, height=750, fg_color="#897E9B")
        screen_frame.pack_propagate(0)
        screen_frame.pack(expand=True, fill="both")

        if window_number == 1:

            data_text = f"""
                Contract ID: {contract_data[0]}
                Conclusion date: {contract_data[1]}

                Client email: {client_data[1]}
                Client phone: {client_data[2]}
                Client PIB: {client_data[3]}

                Dispatcher PIB: {dispatcher_data[1]}

                Name: {cargo_type_data[1]}
                Description: {cargo_type_data[2]}
                Dimensions: {cargo_type_data[3]}  
                Quantity: {cargo_data[2]}
                Weight: {cargo_data[3]}

                Departure station: {itinerary_data[1]}
                Arrival station: {itinerary_data[2]}
                Route length: {itinerary_data[3]}
                Duration: {itinerary_data[4]}

                Payment amount: {payment_data[1]}
                Payment date: {payment_data[2]}
                """

            text_box = CTkTextbox(screen_frame, width=400, height=400)
            text_box.pack(padx=60, pady=130, fill='both', expand=False)
            text_box.insert('1.0', data_text)
            text_box.configure(state='disabled')

            info_label = CTkLabel(master=screen_frame, text="Here can modify:\n1 Cargo info and route info"
                                                            "\n2 Payment sum will be calculated automatically",
                                  text_color="#CCCCCC", anchor="w", justify="left", font=("Arial Rounded MT Bold", 16))
            info_label.place(relx=0, rely=0.1, anchor="w", x=60, y=15)

            next_btn = CTkButton(master=screen_frame, text="Next", **btn_style, command=next_step)
            next_btn.place(relx=0.9, rely=0.9, anchor="se")

        elif window_number == 2:
            def update_cargo():
                cargo_name = type_combobox.get().strip()
                description = desc_entry.get().strip()
                dimensions = dim_entry.get().strip()
                quantity = quantity_input.get().strip()
                weight = weight_input.get().strip()

                if not cargo_name or not dimensions or not weight or not quantity:
                    CTkMessagebox(message="Please fill in all fields", icon="cancel", option_1="OK")
                    return

                try:
                    cursor.execute(
                        "UPDATE CargoType SET cargo_name = ?, description = ?, dimensions = ? WHERE cargo_type_id = ?",
                        (cargo_name, description, dimensions, cargo_type_data[0]))
                    cursor.execute("UPDATE Cargo SET quantity = ?, weight = ? WHERE cargo_id = ?",
                                   (quantity, weight, cargo_data[0]))
                    conn.commit()
                    CTkMessagebox(message="Cargo information updated successfully", icon="check", option_1="OK")
                except sqlite3.Error as e:
                    CTkMessagebox(message="An error occurred", icon="cancel", option_1="OK")

            type_label = CTkLabel(master=screen_frame, text="Choose new cargo type:", **label_style)
            type_label.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

            initial_values = ['Freight', 'Coal', 'Grains', 'Steel', 'Lumber', 'Oil', 'Chemicals', 'Machinery',
                              'Automobiles', 'Containers', 'Livestock', 'Cement', 'Fertilizer', 'Papers']

            type_combobox = CTkComboBox(screen_frame, values=[cargo_type_data[1]] + initial_values, width=250)
            type_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=45)
            type_combobox.set(cargo_type_data[1])

            add_label = CTkLabel(master=screen_frame, text="Or enter new type:", **label_style)
            add_label.place(relx=0, rely=0.1, anchor="w", x=420, y=5)

            type_entry = CTkEntry(master=screen_frame, width=140)
            type_entry.place(relx=0, rely=0.1, anchor="w", x=420, y=45)

            tooltip_add = CTkToolTip(type_entry, message="Add new cargo type")
            tooltip_add.show()

            def new_type():
                new_cargo_type = type_entry.get().strip()
                if new_cargo_type == "":
                    return
                if not new_cargo_type[0].isupper():
                    tooltip_add.configure(message="Please enter the new cargo type with a capital letter!")
                    return
                existing_cargo_types = list(type_combobox.cget('values'))
                existing_cargo_types.append(new_cargo_type)
                type_combobox.configure(values=existing_cargo_types)
            add_button = CTkButton(master=screen_frame, text="Add", width=40, **btn_style, command=new_type)
            add_button.place(relx=0, rely=0.1, anchor="w", x=350, y=45)


            cargo_type_checked = False
            def cargo_type_check(cargo_obj):
                global cargo_type_checked
                if cargo_obj.isCargoType():
                    cargo_type_checked = True
                    CTkMessagebox(message="Cargo type is available", icon="check", option_1="Thanks")
                    update_btn.configure(state="normal")
                else:
                    cargo_type_checked = False
                    CTkMessagebox(title="Error", message="This cargo type is not available!", icon="cancel")
                    update_btn.configure(state="disabled")


            type_label2 = CTkLabel(master=screen_frame, text="Add description (if necessary):", **label_style)
            type_label2.place(relx=0, rely=0.1, anchor="w", x=30, y=185)

            desc_entry = CTkEntry(master=screen_frame, width=350, height=50, **entry_style)
            desc_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=225)
            desc_entry.insert(0, cargo_type_data[2])

            type_label1 = CTkLabel(master=screen_frame, text="Enter dimensions:", **label_style)
            type_label1.place(relx=0, rely=0.1, anchor="w", x=30, y=95)
            dim_entry = CTkEntry(master=screen_frame, width=150, height=30, **entry_style)
            dim_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=135)
            dim_entry.insert(0, cargo_type_data[3])

            quantity_label = CTkLabel(master=screen_frame, text="Enter quantity:", **label_style)
            quantity_label.place(relx=0, rely=0.1, anchor="w", x=420, y=185)
            quantity_input = CTkEntry(master=screen_frame, width=150, height=30, **entry_style)
            quantity_input.place(relx=0, rely=0.1, anchor="w", x=420, y=225)
            quantity_input.insert(0, cargo_data[2])

            weight_label = CTkLabel(master=screen_frame, text="Enter weight:(tons)", **label_style)
            weight_label.place(relx=0, rely=0.1, anchor="w", x=420, y=95)
            weight_input = CTkEntry(master=screen_frame, width=150, height=30, **entry_style)
            weight_input.place(relx=0, rely=0.1, anchor="w", x=420, y=135)
            weight_input.insert(0, cargo_data[3])

            check_btn = CTkButton(master=screen_frame, text="Check availability", **btn_style,
                                  command=lambda: cargo_type_check(
                                      CargoType(type_combobox.get(), dim_entry.get(), weight_input.get(),
                                                quantity_input.get(), desc_entry.get())))
            check_btn.place(relx=0, rely=0.1, anchor="w", x=30, y=300)

            update_btn = CTkButton(screen_frame, text="Update cargo", **btn_style, command=update_cargo)
            update_btn.place(relx=0, rely=0.1, anchor="w", x=200, y=300)
            update_btn.configure(state="disabled")

            next_btn = CTkButton(master=screen_frame, text="Next", **btn_style, command=next_step)
            next_btn.place(relx=0.9, rely=0.9, anchor="se")

        elif window_number == 3:
            def fetch_stations():
                cursor.execute("SELECT DISTINCT departure_station FROM Itinerary")
                dep_stations = [row[0] for row in cursor.fetchall()]
                cursor.execute("SELECT DISTINCT arrival_station FROM Itinerary")
                arr_stations = [row[0] for row in cursor.fetchall()]
                return dep_stations, arr_stations

            def update_station():
                old_dep_station = dep_combobox.get()
                new_dep_station = dep_entry.get().strip()
                old_arr_station = arr_combobox.get()
                new_arr_station = arr_entry.get().strip()

                if new_dep_station and not new_dep_station[0].isupper():
                    CTkMessagebox(message="Please enter the new departure station with a capital letter!",
                                  icon="cancel")
                    return
                if new_arr_station and not new_arr_station[0].isupper():
                    CTkMessagebox(message="Please enter the new arrival station with a capital letter!", icon="cancel")
                    return

                try:
                    cursor.execute("UPDATE Itinerary SET departure_station = ? WHERE departure_station = ?",
                                   (new_dep_station, old_dep_station))
                    cursor.execute("UPDATE Itinerary SET arrival_station = ? WHERE arrival_station = ?",
                                   (new_arr_station, old_arr_station))

                    # Обчислення нового значення route_length та duration
                    map_obj = Map(new_dep_station, new_arr_station, 0, 0)
                    is_connection, distance, duration = map_obj.is_station()

                    if is_connection:
                        cursor.execute(
                            "UPDATE Itinerary SET route_length = ?, duration = ? WHERE departure_station = ? AND arrival_station = ?",
                            (distance, duration, new_dep_station, new_arr_station))
                        conn.commit()
                        CTkMessagebox(message="Stations and route details updated successfully!", icon="info",
                                      option_1="Ok")
                    else:
                        CTkMessagebox(message="Cannot find railway connection between the updated stations",
                                      icon="cancel")

                    refresh_comboboxes()
                except sqlite3.Error as e:
                    CTkMessagebox(message=f"Error updating stations: {e}", icon="cancel")

            def refresh_comboboxes():
                dep_stations, arr_stations = fetch_stations()
                dep_combobox.configure(values=dep_stations)
                arr_combobox.configure(values=arr_stations)

            label1 = CTkLabel(master=screen_frame, text="Update stations", text_color="#000000", anchor="w",
                              justify="left", font=("Arial Rounded MT Bold", 17))
            label1.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

            dep_label = CTkLabel(master=screen_frame, text="Select and update departure station:", **label_style)
            dep_label.place(relx=0, rely=0.1, anchor="w", x=30, y=50)

            dep_stations, arr_stations = fetch_stations()

            dep_combobox = CTkComboBox(master=screen_frame, values=dep_stations, width=300)
            dep_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=80)

            dep_entry = CTkEntry(master=screen_frame, width=300)
            dep_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=110)

            arr_label = CTkLabel(master=screen_frame, text="Select and update arrival station:", **label_style)
            arr_label.place(relx=0, rely=0.1, anchor="w", x=30, y=150)

            arr_combobox = CTkComboBox(master=screen_frame, values=arr_stations, width=300)
            arr_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=180)

            arr_entry = CTkEntry(master=screen_frame, width=300)
            arr_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=210)

            update_btn = CTkButton(master=screen_frame, text="Update stations", width=90, **btn_style,
                                   command=update_station)
            update_btn.place(relx=0, rely=0.1, anchor="w", x=30, y=250)

            next_btn = CTkButton(master=screen_frame, text="Next", **btn_style, command=next_step)
            next_btn.place(relx=0.9, rely=0.9, anchor="se")

        elif window_number == 4:
            def record_payment(calculated_tariff):
                try:
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()
                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    cursor.execute("SELECT payment_id "
                                   "FROM Payment ORDER BY payment_id DESC LIMIT 1")
                    payment_record = cursor.fetchone()

                    if payment_record:
                        payment_id = payment_record[0]
                        cursor.execute(
                            "UPDATE Payment SET payment_amount = ?, payment_datetime = ? WHERE payment_id = ?",
                            (calculated_tariff, current_datetime, payment_id))
                    else:
                        cursor.execute(
                            "INSERT INTO Payment (payment_amount, payment_datetime) VALUES (?, ?)",
                            (calculated_tariff, current_datetime))

                    conn.commit()
                    conn.close()
                    CTkMessagebox(message="Payment recorded successfully!", icon="check", option_1="Thanks")
                except sqlite3.Error as e:
                    CTkMessagebox(message="Payment is not recorded!", icon="cancel", option_1="OK")

            def calculate_tariff():
                global calculated_tariff
                try:
                    cursor.execute(
                        "SELECT ct.cargo_name, c.weight "
                        "FROM Cargo c INNER JOIN CargoType ct ON c.cargo_type_id = ct.cargo_type_id "
                        "ORDER BY c.rowid DESC LIMIT 1")
                    cargo_data = cursor.fetchone()

                    cursor.execute("SELECT route_length, duration "
                                   "FROM Itinerary ORDER BY rowid DESC LIMIT 1")
                    route_data = cursor.fetchone()
                    display_data(cargo_data, route_data)

                    if cargo_data and route_data:
                        cargo_type, weight = cargo_data
                        distance, duration = route_data

                        calc_obj = Calc(None, distance, None, duration, cargo_type, weight)
                        calc_obj.calculate_price()
                        calculated_tariff = calc_obj.get_price()
                        record_payment(calculated_tariff)

                        textbox1.configure(state="normal")
                        textbox1.delete("1.0", "end")
                        textbox1.insert("end", f"Calculated tariff: {calculated_tariff}$")
                        textbox1.configure(state="disabled")

                        display_data(cargo_data, route_data)

                except sqlite3.Error as e:
                    print("Error:", e)

            def display_data(cargo_data, route_data):
                if cargo_data and route_data:
                    cargo_type, weight = cargo_data
                    distance, duration = route_data

                    textbox.configure(state="normal")
                    textbox.delete("1.0", "end")
                    headers = f"{'Cargo Type':<35}{'Weight':<35}{'Distance':<35}{'Duration':<35}\n"
                    table_data = headers
                    row_data = f"{cargo_type:<40}{weight:<40}{distance:<40}{duration:<40}\n"
                    table_data += row_data
                    textbox.insert("end", table_data)
                    textbox.configure(state="disabled")

            def display():
                try:
                    calculate_tariff()
                except sqlite3.Error as e:
                    CTkMessagebox(message="Error", icon="cancel", option_1="OK")

            payment_label = CTkLabel(master=screen_frame, text="Almost done!"
                                                               "\nNow make the payment",
                                     text_color="#000000", anchor="w",
                                     justify="left",
                                     font=("Arial Rounded MT Bold", 18))
            payment_label.place(relx=0, rely=0.1, anchor="w", x=30, y=10)

            list_label = CTkLabel(master=screen_frame,
                                  text="Click button 'Accept payment' to see the price "
                                       "for the transportation" "\nand save the payment",
                                  text_color="#CCCCCC", anchor="w", justify="left",
                                  font=("Arial Rounded MT Bold", 14))
            list_label.place(relx=0, rely=0.1, anchor="w", x=30, y=80)

            display_button = CTkButton(master=screen_frame, text="Accept payment", **btn_style,
                                       width=90, command=display)
            display_button.place(relx=0, rely=0.1, anchor="w", x=30, y=350)

            textbox = CTkTextbox(master=screen_frame, width=500, height=80)
            textbox.place(relx=0, rely=0.1, anchor="w", x=30, y=155)
            textbox1 = CTkTextbox(master=screen_frame, width=500, height=80)
            textbox1.place(relx=0, rely=0.1, anchor="w", x=30, y=255)

    show_current_step()
    cont_window.mainloop()
def dispatcher_window():
    app = CTk()
    app.title("Dispatcher window")

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    app_width = 750
    app_height = 650

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    app.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    app.resizable(0, 0)

    right_frame = CTkFrame(master=app, width=550, height=650, fg_color="#897E9B")
    right_frame.pack_propagate(0)
    right_frame.pack(expand=True, side="right")

    CTkLabel(master=right_frame, text="").pack(expand=True, side="right")
    left_frame = CTkFrame(master=app, width=200, height=650, fg_color="#FFFFFF")
    left_frame.pack_propagate(0)
    left_frame.pack(expand=True, side="left")

    # right frame
    CTkLabel(master=right_frame, text="You are logged as a dispatcher",
             text_color="#000000", anchor="w",
             justify="center",
             font=("Hanson", 20)).place(relx=0, rely=0, anchor="w", x=30, y=100)


    req_frame1 = ctk.CTkFrame(master=right_frame, fg_color="#FFFFFF", width=550, height=95)
    req_frame1.place(relx=0, rely=0, anchor="w", x=30, y=50)


    first_btn = ctk.CTkButton(master=req_frame1, text="Contracts\nby dispatcher", **btn_style,
                              command=find1)
    first_btn.pack(side="left", padx=10, pady=10)


    second_btn = ctk.CTkButton(master=req_frame1, text="Search\nclients", **btn_style)
    second_btn.pack(side="left", padx=10, pady=10)


    third_btn = ctk.CTkButton(master=req_frame1, text="Contracts\nby date", **btn_style)
    third_btn.pack(side="left", padx=10, pady=10)


    # left frame --> buttons
    info_btn = CTkButton(master=left_frame, text="Change my info", **btn_style,
                         command=find_dispatcher)
    info_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))


    c_btn = CTkButton(master=left_frame, text="New contract", **btn_style,
             command=lambda: create_contract())
    c_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))


    list_btn = CTkButton(master=left_frame, text="All contracts", **btn_style,
                         command=contracts_window)
    list_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))


    up_btn = CTkButton(master=left_frame, text="Delete contract", **btn_style,
                           command=delete_contract)
    up_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))


    add_btn = CTkButton(master=left_frame, text="Update contract", **btn_style,
                        command=modifying_contract)
    add_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))


    deld_btn = CTkButton(master=left_frame, text="Deactivate \ndispatcher account", **btn_style,
                        command=delete_dispatcher)
    deld_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))


    delc_btn = CTkButton(master=left_frame, text="Deactivate \nclient account", **btn_style,
                        command=delete_client)
    delc_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))

    app.mainloop()