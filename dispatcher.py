import sqlite3
import customtkinter
from CTkToolTip import *
from customtkinter import *
from classes.Map import Map
from datetime import datetime
from classes.Calc import Calc
from database import cursor, conn
from classes.Tariff import Tariff
from classes.Contract import Contract
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

def insert_type(name, description, dimensions):
    try:
        cursor.execute("INSERT INTO CargoType (name, description, dimensions) VALUES (?, ?, ?)", (name, description, dimensions))
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
        CTkMessagebox(title="Error", message="cargo_type_id does not exist in the CargoType table", icon="cancel")
        return
    cursor.execute("INSERT INTO Cargo (cargo_type_id, quantity, weight) VALUES (?, ?, ?)", (cargo_type_id, quantity, weight))
    conn.commit()
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
            def cargo_type_check(cargo_instance):
                global cargo_type_checked
                if cargo_instance.isCargoType():
                    cargo_type_checked = True
                    CTkMessagebox(message="Cargo type is available", icon="check", option_1="Thanks")
                    save.configure(state="normal")
                else:
                    cargo_type_checked = False
                    CTkMessagebox(title="Error", message="This cargo type is not available!", icon="cancel")
                    save.configure(state="disabled")

            # adding data to table "cargo types"
            def save_cargo():
                global cargo_type_checked

                if not cargo_type_checked:
                    CTkMessagebox(title="Error", message="Please check cargo type availability first", icon="cancel")
                    return

                if not type_combobox.get().strip() or not dim_entry.get() or not weight_input.get() or not quantity_input.get():
                    CTkMessagebox(title="Error", message="Please fill in all fields", icon="cancel")
                    return

                if not weight_input.get().isdigit():
                    CTkMessagebox(title="Error", message="Weight should contain only digits", icon="cancel")
                    return

                if not quantity_input.get().isdigit():
                    CTkMessagebox(title="Error", message="Quantity should contain only digits", icon="cancel")
                    return

                if not dim_entry.get().replace('*', '').isdigit():
                    CTkMessagebox(title="Error", message="Dimensions should contain only digits or '*'",  icon="cancel")
                    return

                # save cargo type data
                name = type_combobox.get().strip()
                description = desc_entry.get()
                dimensions = dim_entry.get()
                insert_type(name, description, dimensions)

                # save cargo data
                selected_type = type_combobox.get()
                quantity = quantity_input.get()
                weight = weight_input.get()
                cursor.execute("SELECT cargo_type_id FROM CargoType WHERE name = ?", (selected_type,))
                result = cursor.fetchone()

                if result is None:
                    CTkMessagebox(title="Error", message="Selected cargo type not found", icon="cancel")
                    return

                cargo_type_id = result[0]
                insert_cargo(cargo_type_id, quantity, weight)

                # adding data to table contract
                save_contract_data()
            def save_contract_data():
                cargo_name = type_combobox.get().strip()
                quantity = quantity_input.get()
                weight = weight_input.get()

                contract_data["cargo_name"] = cargo_name
                contract_data["quantity"] = quantity
                contract_data["weight"] = weight
            # adding data to table contract

            # buttons
            check_btn = CTkButton(master=screen_frame, text="Check availability",  **btn_style,
                            command=lambda: cargo_type_check(CargoType(type_combobox.get(), dim_entry.get(), weight_input.get(),
                                                                            quantity_input.get(), desc_entry.get())))
            check_btn.place(relx=0, rely=0.1, anchor="w", x=30, y=300)

            save = CTkButton(master=screen_frame, text="Save type", **btn_style, width=90, command=save_cargo)
            save.place(relx=0, rely=0.1, anchor="w", x=200, y=300)
            save.configure(state="disabled")

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
            weight_label.place(relx=0, rely=0.1, anchor="w", x=420, y=185)

            weight_input = CTkEntry(master=screen_frame, width=150, height=30,**entry_style)
            weight_input.place(relx=0, rely=0.1, anchor="w", x=420, y=225)

            # cargo`s quantity
            quantity_label = CTkLabel(master=screen_frame, text="Enter quantity:", **label_style)
            quantity_label.place(relx=0, rely=0.1, anchor="w", x=420, y=265)

            quantity_input = CTkEntry(master=screen_frame, width=150, height=30, **entry_style)
            quantity_input.place(relx=0, rely=0.1, anchor="w", x=420, y=295)

            next_btn = CTkButton(master=screen_frame, text="Next step", **btn_style, command=next_step)
            next_btn.place(relx=0, rely=0.1, anchor="w", x=420, y=400)

        elif window_number == 2:
            def find_connection():
                dep_station = dep_entry.get()
                arr_station = arr_entry.get()
                map_instance = Map(dep_station, arr_station, 0, 0)
                is_connection, distance, duration = map_instance.is_station()

                if is_connection:
                    CTkMessagebox(message=f"Railway connection exists! Distance: {distance} km,"
                                          f"Duration: {duration} hours",
                        icon="check", option_1="Ok")
                    distance_label.configure(text=f"Distance: {distance} km")
                    duration_label.configure(text=f"Duration: {duration} hours")
                else:
                    CTkMessagebox(title="Error", message="Railway connection doesn't exist",
                                  icon="cancel")
            def save_route():
                dep_station = dep_entry.get()
                arr_station = arr_entry.get()

                map = Map(dep_station, arr_station, 0, 0)
                is_connection, distance, duration = map.is_station()

                if is_connection:
                    cursor.execute(
                        "INSERT INTO Itinerary (departure_station, arrival_station, route_length, duration) VALUES (?, ?, ?, ?)",
                        (dep_station, arr_station, distance, duration))
                    conn.commit()
                    CTkMessagebox(message="Route saved successfully!", icon="info", option_1="Ok")
                else:
                    CTkMessagebox(title="Error", message="Cannot save route. Railway connection doesn't exist",
                                  icon="cancel")

            label1 = CTkLabel(master=screen_frame, text="Enter the stations and check "
                                                        "if the railway connection exists:",
                              text_color="#000000", anchor="w",
                              justify="left", font=("Arial Rounded MT Bold", 17))
            label1.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

            dep_label = CTkLabel(master=screen_frame, text="Departure station:", **label_style)
            dep_label.place(relx=0, rely=0.1, anchor="w", x=30, y=60)

            dep_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            dep_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=90)

            arr_label = CTkLabel(master=screen_frame, text="Arrival station:", **label_style)
            arr_label.place(relx=0, rely=0.1, anchor="w", x=30, y=130)

            arr_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            arr_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=160)

            check_btn1 = CTkButton(master=screen_frame, text="Check availability", **btn_style,
                                   command=find_connection)
            check_btn1.place(relx=0, rely=0.1, anchor="w", x=30, y=250)

            distance_label = CTkLabel(master=screen_frame, text="", **label_style)
            distance_label.place(relx=0, rely=0.1, anchor="w", x=350, y=50)

            duration_label = CTkLabel(master=screen_frame, text="", **label_style)
            duration_label.place(relx=0, rely=0.1, anchor="w", x=350, y=100)

            def save_contract_data():
                departure_station = dep_entry.get().strip()
                arrival_station = arr_entry.get().strip()
                distance = distance_label.cget("text").split(":")[1].strip()

                # Зберігаємо дані про контракт
                contract_data["departure_station"] = departure_station
                contract_data["arrival_station"] = arrival_station
                contract_data["route_length"] = distance

            save_btn = CTkButton(master=screen_frame, text="Save and proceed", width=90,
                                 **btn_style, command=save_contract_data)
            save_btn.place(relx=0, rely=0.1, anchor="w", x=200, y=400)

            save1 = CTkButton(master=screen_frame, text="Save route", width=90,
                              **btn_style, command=save_route)
            save1.place(relx=0, rely=0.1, anchor="w", x=200, y=250)

            next_btn = CTkButton(master=screen_frame, text="Next step", **btn_style,
                                 command=next_step)
            next_btn.place(relx=0, rely=0.1, anchor="w", x=420, y=400)

        elif window_number == 3:

            payment_label = CTkLabel(master=screen_frame, text="Payment",
                                    text_color="#000000", anchor="w",
                                    justify="left",
                                    font=("Arial Rounded MT Bold", 17))
            payment_label.place(relx=0, rely=0, anchor="w", x=270, y=35)

            list_label = CTkLabel(master=screen_frame,
                                  text="1 Click button 'Display' to see the price"
                                       "\nand save the payment", **label_style)
            list_label.place(relx=0, rely=0.1, anchor="w", x=30, y=45)

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

                    print("Payment recorded successfully.")

                except sqlite3.Error as e:
                    print("Error:", e)
            def calculate_tariff():
                global calculated_tariff
                try:
                    cursor.execute(
                        "SELECT ct.name, c.weight FROM Cargo c INNER JOIN CargoType ct ON c.cargo_type_id = ct.cargo_type_id ORDER BY c.rowid DESC LIMIT 1")
                    cargo_data = cursor.fetchone()

                    cursor.execute("SELECT route_length, duration FROM Itinerary ORDER BY rowid DESC LIMIT 1")
                    route_data = cursor.fetchone()

                    display_data(cargo_data, route_data)

                    if cargo_data and route_data:
                        cargo_type, weight = cargo_data
                        distance, _ = route_data

                        calc_instance = Calc(None, distance, None, cargo_type, weight)
                        calc_instance.calculate_price()
                        calculated_tariff = calc_instance.get_price()

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
                    print("Error:", e)

            display_button = CTkButton(master=screen_frame, text="Display and"
                                                                 "\naccept the payment", **btn_style,
                                       width=90, command=display)
            display_button.place(relx=0, rely=0.1, anchor="w", x=30, y=320)

            textbox = CTkTextbox(master=screen_frame, width=500, height=80)
            textbox.place(relx=0, rely=0.1, anchor="w", x=30, y=135)

            textbox1 = CTkTextbox(master=screen_frame, width=500, height=80)
            textbox1.place(relx=0, rely=0.1, anchor="w", x=30, y=235)

            def save_contract_data():
                payment_amount = calculated_tariff
                contract_data["payment_amount"] = payment_amount

            save_btn = CTkButton(master=screen_frame, text="Save and proceed", width=90,
                                 **btn_style,command=save_contract_data)
            save_btn.place(relx=0, rely=0.1, anchor="w", x=200, y=350)

            next_btn = CTkButton(master=screen_frame, text="Next step", **btn_style,
                                 command=next_step)
            next_btn.place(relx=0, rely=0.1, anchor="w", x=420, y=400)

        elif window_number == 4:
            cl_label = CTkLabel(master=screen_frame, text="Register the client:",
                               text_color="#000000", anchor="w",
                               justify="left",
                               font=("Arial Rounded MT Bold", 18))
            cl_label.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

            rec_pib = CTkLabel(master=screen_frame, text="Enter pib:", **label_style)
            rec_pib.place(relx=0, rely=0.1, anchor="w", x=30, y=35)

            pib_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            pib_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=65)

            rec_ph = CTkLabel(master=screen_frame, text="Enter phone number:", **label_style)
            rec_ph.place(relx=0, rely=0.1, anchor="w", x=30, y=95)

            ph_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            ph_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=125)

            rec_email = CTkLabel(master=screen_frame, text="Enter email:", **label_style)
            rec_email.place(relx=0, rely=0.1, anchor="w", x=30, y=155)

            email_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            email_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=185)

            rec_password = CTkLabel(master=screen_frame, text="Enter password:", **label_style)
            rec_password.place(relx=0, rely=0.1, anchor="w", x=30, y=215)

            password_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
            password_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=245)

            def save_contract_data():
                c_pib = pib_entry.get()
                c_phone_number = ph_entry.get()

                # Зберігаємо дані про контракт
                contract_data["c_pib"] = c_pib
                contract_data["c_phone_number"] = c_phone_number
            def create_client(cursor):
                pib = pib_entry.get().strip()
                phone_number = ph_entry.get().strip()
                email = email_entry.get().strip()
                password = password_entry.get().strip()

                try:
                    if not pib or not phone_number or not email or not password:
                        print("Please fill in all fields.")
                        return
                    cursor.execute(
                        "INSERT INTO Client (c_pib, c_phone_number, c_email, c_password) VALUES (?, ?, ?, ?)",
                        (pib, phone_number, email, password)
                    )
                    conn.commit()
                    print("Client created successfully.")
                except sqlite3.Error as e:
                    print("Error:", e)

            save_client = CTkButton(master=screen_frame, text="Register client", **btn_style,
                                    command=lambda: create_client(cursor))
            save_client.place(relx=0, rely=0.1, anchor="w", x=30, y=300)

            save_btn = CTkButton(master=screen_frame, text="Save and proceed", width=90,
                                 **btn_style, command=save_contract_data)
            save_btn.place(relx=0, rely=0.1, anchor="w", x=200, y=350)

            def create(contract_data):
                cargo_name = contract_data.get("cargo_name", "")
                quantity = contract_data.get("quantity", "")
                weight = contract_data.get("weight", "")
                departure_station = contract_data.get("departure_station", "")
                arrival_station = contract_data.get("arrival_station", "")
                route_length = contract_data.get("route_length", "")
                payment_amount = contract_data.get("payment_amount", "")
                c_pib = contract_data.get("c_pib", "")
                c_phone_number = contract_data.get("c_phone_number", "")
                d_pib = contract_data.get("d_pib", "")

                try:
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()

                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    cursor.execute("SELECT client_id FROM Client ORDER BY client_id DESC LIMIT 1")
                    client_id = cursor.fetchone()
                    if client_id:
                        client_id = client_id[0]
                    else:
                        raise ValueError("No clients found.")

                    cursor.execute("SELECT dispatcher_id FROM Dispatcher ORDER BY dispatcher_id DESC LIMIT 1")
                    dispatcher_id = cursor.fetchone()
                    if dispatcher_id:
                        dispatcher_id = dispatcher_id[0]
                    else:
                        raise ValueError("No dispatchers found.")

                    cursor.execute(
                        "SELECT cargo_type_id FROM CargoType WHERE name = ? ORDER BY cargo_type_id DESC LIMIT 1",
                        (cargo_name,))
                    cargo_type_id = cursor.fetchone()
                    if cargo_type_id:
                        cargo_type_id = cargo_type_id[0]
                    else:
                        raise ValueError("No cargo types found with the provided name.")

                    cursor.execute(
                        "SELECT route_id FROM Itinerary WHERE departure_station = ? AND arrival_station = ? ORDER BY route_id DESC LIMIT 1",
                        (departure_station, arrival_station))
                    route_id = cursor.fetchone()
                    if route_id:
                        route_id = route_id[0]
                    else:
                        raise ValueError("No routes found with the provided departure and arrival stations.")

                    cursor.execute("SELECT payment_id FROM Payment ORDER BY payment_id DESC LIMIT 1")
                    payment_id = cursor.fetchone()
                    if payment_id:
                        payment_id = payment_id[0]
                    else:
                        raise ValueError("No payments found.")

                    cursor.execute(
                        "INSERT INTO Contract (departure_station, arrival_station, route_length, c_pib, c_phone_number, payment_amount,"
                        "cargo_name, quantity, weight, client_id, dispatcher_id, conclusion_date, cargo_type_id, itinerary_id, payment_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (departure_station, arrival_station, route_length, c_pib, c_phone_number,
                         payment_amount, cargo_name, quantity, weight, client_id, dispatcher_id,
                         current_datetime, cargo_type_id, route_id, payment_id))
                    conn.commit()
                    conn.close()

                    print("Contract data recorded successfully.")

                except sqlite3.Error as e:
                    print("Error:", e)
                except ValueError as ve:
                    print("Value Error:", ve)

            save_contract = CTkButton(master=screen_frame, text="Save contract",  **btn_style,
                                      command=lambda: create(contract_data))
            save_contract.place(relx=0, rely=0.1, anchor="w", x=30, y=420)

    show_current_step()
    contract_window.mainloop()
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

    CTkLabel(master=right_frame, text="You are logged as a dispatcher",
             text_color="#000000", anchor="w",
             justify="center",
             font=("Arial Rounded MT Bold", 25)).place(relx=0, rely=0, anchor="w", x=90, y=30)

    c_btn = CTkButton(master=left_frame, text="New contract", **btn_style,
             command=lambda: create_contract())
    c_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))

    up_btn = CTkButton(master=left_frame, text="Delete contract", **btn_style)
    up_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))

    del_btn = CTkButton(master=left_frame, text="Update contract", **btn_style)
    del_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))

    add_btn = CTkButton(master=left_frame, text="Add new....", **btn_style)
    add_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))

    app.mainloop()
