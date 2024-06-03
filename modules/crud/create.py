import sqlite3
from datetime import datetime
from CTkToolTip import *
import customtkinter as ctk
from customtkinter import *
from CTkMessagebox import CTkMessagebox

from classes.Map import Map
from classes.Calc import Calc
from classes.Register import Register
from classes.Contract import Contract
from classes.CargoType import CargoType
from classes.ContractInfo import ContractInfo
from classes.ContractInfo import ContractList

from database.database_setup import cursor, conn
from modules.print import print_contract
from modules.auth.register import register_client

regional_centers = Map.regional_centers

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

            type_combobox = CTkComboBox(master=screen_frame,
                                        values=['   ', 'Freight', 'Coal', 'Grains', 'Steel', 'Lumber',
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
                    cursor.execute("INSERT INTO CargoType (cargo_name, description, dimensions)"
                                   "VALUES (?, ?, ?)",
                                   (cargo_name, description, dimensions))
                    conn.commit()

                    CTkMessagebox(message="Info saved!",
                                  icon="check",
                                  option_1="Ok")

                except sqlite3.Error as e:
                    conn.rollback()
                    CTkMessagebox(title="Error",
                                  message="Type info is not saved",
                                  icon="cancel")

            def insert_cargo(cargo_type_id, quantity, weight):
                cursor.execute("SELECT COUNT(*) "
                               "FROM CargoType "
                               "WHERE cargo_type_id = ?", (cargo_type_id,))
                count = cursor.fetchone()[0]
                if count == 0:
                    CTkMessagebox(title="Error",
                                  message="cargo type id does not exist in the Cargo type table",
                                  icon="cancel")
                    return
                cursor.execute("INSERT INTO Cargo (cargo_type_id, quantity, weight) "
                               "VALUES (?, ?, ?)",
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

            add_btn1 = CTkButton(master=screen_frame, text="Add", width=40,
                                 **btn_style, command=new_type)
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
                    CTkMessagebox(message="Cargo type is available",
                                  icon="check",
                                  option_1="Thanks")
                    save.configure(state="normal")

                else:
                    cargo_type_checked = False
                    CTkMessagebox(title="Error",
                                  message="This cargo type is not available!",
                                  icon="cancel")
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
                cursor.execute("SELECT cargo_type_id "
                               "FROM CargoType "
                               "WHERE cargo_name = ?",
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
                                                                             dim_entry.get(), weight_input.get(),
                                                                             quantity_input.get(), desc_entry.get())))
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

            dim_entry = CTkEntry(master=screen_frame, width=150, height=30, **entry_style)
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

        if window_number == 2:
            def find_connection():
                dep_station = dep_combobox.get()
                arr_station = arr_combobox.get()

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
                dep_station = dep_combobox.get()
                arr_station = arr_combobox.get()

                map = Map(dep_station, arr_station, 0, 0)
                is_connection, distance, duration = map.is_station()

                if is_connection:
                    cursor.execute(
                        "INSERT INTO Itinerary (departure_station, arrival_station,"
                        " route_length, duration) "
                        "VALUES (?, ?, ?, ?)",
                        (dep_station, arr_station, distance, duration))
                    conn.commit()
                    CTkMessagebox(message="Route saved successfully!",
                                  icon="info",
                                  option_1="Ok")
                else:
                    CTkMessagebox(title="Error",
                                  message="Cannot save route. Railway connection doesn't exist",
                                  icon="cancel")

            label1 = CTkLabel(master=screen_frame,
                              text="Enter the stations and check if the railway connection exists:",
                              text_color="#000000", anchor="w", justify="left",
                              font=("Arial Rounded MT Bold", 17))
            label1.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

            label2 = CTkLabel(master=screen_frame,
                              text="Reminder:\nSystem works only with Ukrainian cities."
                                   "\nBegin with capital letter.",
                              text_color="#CCCCCC", anchor="w", justify="left",
                              font=("Arial Rounded MT Bold", 14))
            label2.place(relx=0, rely=0.1, anchor="w", x=30, y=60)

            dep_label = CTkLabel(master=screen_frame, text="Departure station:", **label_style)
            dep_label.place(relx=0, rely=0.1, anchor="w", x=30, y=130)

            dep_combobox = ctk.CTkComboBox(master=screen_frame, values=regional_centers, width=300)
            dep_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=160)

            arr_label = CTkLabel(master=screen_frame, text="Arrival station:", **label_style)
            arr_label.place(relx=0, rely=0.1, anchor="w", x=30, y=190)

            arr_combobox = ctk.CTkComboBox(master=screen_frame, values=regional_centers, width=300)
            arr_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=220)

            result_text = CTkTextbox(master=screen_frame, width=180, height=200)
            result_text.place(relx=0, rely=0.1, anchor="w", x=370, y=170)

            # buttons
            check_btn1 = CTkButton(master=screen_frame, text="Check availability", **btn_style,
                                   command=find_connection).place(relx=0, rely=0.1, anchor="w", x=30, y=320)

            save_btn = CTkButton(master=screen_frame, text="Save route", width=90, **btn_style,
                                 command=save_route, state="disabled")
            save_btn.place(relx=0, rely=0.1, anchor="w", x=200, y=320)

            reminder = CTkLabel(master=screen_frame, text="Don't forget to save the route!:",
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
                                       "\nand save the payment", text_color="#CCCCCC", anchor="w", justify="left",
                                  font=("Arial Rounded MT Bold", 14))
            list_label.place(relx=0, rely=0.1, anchor="w", x=30, y=80)

            def record_payment(calculated_tariff):
                try:
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()

                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    cursor.execute(
                        "INSERT INTO Payment (payment_amount, payment_datetime) "
                        "VALUES (?, ?)",
                        (calculated_tariff, current_datetime))

                    conn.commit()
                    conn.close()
                    CTkMessagebox(message="Payment recorded successfully!",
                                  icon="check",
                                  option_1="Thanks")
                except sqlite3.Error as e:
                    CTkMessagebox(message="Payment is not recorded!",
                                  icon="cancel",
                                  option_1="OK")

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

            display_button = CTkButton(master=screen_frame, text="Accept payment",
                                       **btn_style, width=90, command=display)
            display_button.place(relx=0, rely=0.1, anchor="w", x=30, y=350)

            textbox = CTkTextbox(master=screen_frame, width=500, height=80)
            textbox.place(relx=0, rely=0.1, anchor="w", x=30, y=155)
            textbox1 = CTkTextbox(master=screen_frame, width=500, height=80)
            textbox1.place(relx=0, rely=0.1, anchor="w", x=30, y=255)

            next_btn = CTkButton(master=screen_frame, text="Next step",
                                 **btn_style, command=next_step)
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

            # buttons
            save_client = CTkButton(master=screen_frame, text="Register client",
                                    **btn_style,
                                    command=lambda: register_client(cursor, pib_entry,
                                                                    email_entry, password_entry, ph_entry))
            save_client.place(relx=0, rely=0.1, anchor="w", x=30, y=400)

            next_btn = CTkButton(master=screen_frame, text="Next step", **btn_style,
                                 command=next_step).place(relx=0, rely=0.1, anchor="w", x=420, y=400)

        elif window_number == 5:
            # contract
            def fetch_last_id(cursor, table, column):
                cursor.execute(f"SELECT {column} "
                               f"FROM {table} ORDER BY {column} DESC LIMIT 1")
                return cursor.fetchone()[0]

            def fetch_data(cursor, query, params=()):
                cursor.execute(query, params)
                return cursor.fetchone()

            def create_contract(cursor, conn, client_id, payment_id,
                                dispatcher_id, cargo_id, itinerary_id):

                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    cursor.execute(
                        "INSERT INTO Contract (conclusion_date, client_id,"
                        "payment_id, dispatcher_id, cargo_id, itinerary_id) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (current_datetime, client_id, payment_id, dispatcher_id, cargo_id, itinerary_id))
                    conn.commit()
                    contract_id = cursor.lastrowid

                    cargo_data1 = fetch_data(cursor,
                                             "SELECT quantity, weight, cargo_type_id "
                                             "FROM Cargo WHERE cargo_id = ?",
                                             (cargo_id,))
                    quantity, weight, cargo_type_id = cargo_data1

                    cargo_data2 = fetch_data(cursor,
                                             "SELECT cargo_name, description, dimensions "
                                             "FROM CargoType WHERE cargo_type_id = ?",
                                             (cargo_type_id,))
                    cargo_obj = CargoType(cargo_data2[0], cargo_data2[1], cargo_data2[2], quantity, weight)

                    map_data = fetch_data(cursor,
                                          "SELECT departure_station, arrival_station, route_length, duration "
                                          "FROM Itinerary WHERE itinerary_id = ?",
                                          (itinerary_id,))
                    map_obj = Map(*map_data)

                    payment_data = fetch_data(cursor,
                                              "SELECT payment_amount, payment_datetime "
                                              "FROM Payment WHERE payment_id = ?",
                                              (payment_id,))
                    calc_obj = Calc(payment_data[0], payment_data[1], cargo_data2[0], map_data[2], map_data[3], weight)

                    client_data = fetch_data(cursor,
                                             "SELECT c_email, c_phone_number, c_pib "
                                             "FROM Client WHERE client_id = ?",
                                             (client_id,))
                    c_email, c_phone_number, pib_c = client_data

                    dispatcher_data = fetch_data(cursor, "SELECT d_pib "
                                                         "FROM Dispatcher WHERE dispatcher_id = ?",
                                                 (dispatcher_id,))
                    pib_d = dispatcher_data[0]

                    contract = Contract(contract_id, current_datetime, pib_c,
                                        c_phone_number, c_email, pib_d, cargo_obj,
                                        map_obj, calc_obj)
                    contract_list = ContractList()
                    register = Register(contract, map_obj, calc_obj, contract_list)

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

            def enter_pib(cursor, conn, payment_id, cargo_id, itinerary_id):
                def save_dispatcher_id():
                    try:
                        dispatcher_pib = pib_entry.get()
                        client_phone = client_phone_entry.get()
                        dispatcher_data = fetch_data(cursor, "SELECT dispatcher_id "
                                                             "FROM Dispatcher WHERE d_pib = ?",
                                                     (dispatcher_pib,))

                        if dispatcher_data:
                            dispatcher_id = dispatcher_data[0]
                            client_data = fetch_data(cursor, "SELECT client_id "
                                                             "FROM Client WHERE c_phone_number = ?",
                                                     (client_phone,))

                            if client_data:
                                client_id = client_data[0]
                                contract_id = create_contract(cursor, conn, client_id,
                                                              payment_id, dispatcher_id,
                                                              cargo_id, itinerary_id)

                                if contract_id:
                                    print_button(contract_id)
                                dialog_window.destroy()
                            else:
                                ctk.CTkMessagebox(message="Client with provided phone number not found!",
                                                  icon="cancel",
                                                  option_1="OK")
                        else:
                            ctk.CTkMessagebox(message="Dispatcher with provided PIB not found!",
                                              icon="cancel",
                                              option_1="OK")
                    except sqlite3.Error as e:
                        ctk.CTkMessagebox(message="Database error: " + str(e),
                                          icon="cancel",
                                          option_1="OK")

                dialog_window = ctk.CTk()
                dialog_window.title("Attention")

                screen_width = dialog_window.winfo_screenwidth()
                screen_height = dialog_window.winfo_screenheight()

                dialog_width = 300
                dialog_height = 270

                x_position = (screen_width - dialog_width) // 2
                y_position = (screen_height - dialog_height) // 2
                dialog_window.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
                dialog_window.resizable(0, 0)

                pib_label = ctk.CTkLabel(dialog_window,
                                         text="Confirm your PIB one more time:")
                pib_label.pack(pady=10)

                pib_entry = ctk.CTkEntry(dialog_window)
                pib_entry.pack(pady=10)

                client_phone_label = ctk.CTkLabel(dialog_window,
                                                  text="Phone number of the client:")
                client_phone_label.pack(pady=10)

                client_phone_entry = ctk.CTkEntry(dialog_window)
                client_phone_entry.pack(pady=10)

                confirm_button = ctk.CTkButton(dialog_window, text="Confirm", **btn_style,
                                               command=save_dispatcher_id)
                confirm_button.pack(pady=10)
                dialog_window.mainloop()

            def print_button(contract_id):
                print_btn = ctk.CTkButton(master=screen_frame, text="Print contract", **btn_style,
                                          command=lambda: print_contract(contract_id))
                print_btn.place(relx=0, rely=0, anchor="w", x=220, y=230)


            client_id = fetch_last_id(cursor, "Client", "client_id")
            payment_id = fetch_last_id(cursor, "Payment", "payment_id")
            cargo_id = fetch_last_id(cursor, "Cargo", "cargo_id")
            itinerary_id = fetch_last_id(cursor, "Itinerary", "itinerary_id")


            savec_btn = ctk.CTkButton(master=screen_frame, text="Save contract",
                                      **btn_style,
                                      command=lambda: enter_pib(cursor, conn,
                                                                payment_id, cargo_id, itinerary_id))
            savec_btn.place(relx=0, rely=0, anchor="w", x=220, y=180)

            def finish():
                contract_window.destroy()

            finish_btn = ctk.CTkButton(master=screen_frame, text="Finish",
                                       **btn_style, command=finish)
            finish_btn.place(relx=0, rely=0, anchor="w", x=220, y=280)

    show_current_step()
    contract_window.mainloop()
