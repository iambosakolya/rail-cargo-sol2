import re
import sqlite3
import win32ui
import win32print
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
                cargo_name = type_combobox.get().strip()
                description = desc_entry.get()
                dimensions = dim_entry.get()
                insert_type(cargo_name, description, dimensions)

                # save cargo data
                selected_type = type_combobox.get()
                quantity = quantity_input.get()
                weight = weight_input.get()
                cursor.execute("SELECT cargo_type_id FROM CargoType WHERE cargo_name = ?", (selected_type,))
                result = cursor.fetchone()

                if result is None:
                    CTkMessagebox(title="Error", message="Selected cargo type not found", icon="cancel")
                    return

                cargo_type_id = result[0]
                insert_cargo(cargo_type_id, quantity, weight)

            # buttons
            check_btn = CTkButton(master=screen_frame, text="Check availability",  **btn_style,
                            command=lambda: cargo_type_check(CargoType(type_combobox.get(), dim_entry.get(), weight_input.get(),
                                                                            quantity_input.get(), desc_entry.get())))
            check_btn.place(relx=0, rely=0.1, anchor="w", x=30, y=300)

            save = CTkButton(master=screen_frame, text="Save type", **btn_style, width=90, command=save_cargo)
            save.place(relx=0, rely=0.1, anchor="w", x=200, y=300)
            save.configure(state="disabled")

            reminder0 = CTkLabel(master=screen_frame, text="Dont forget to save the type!:",
                                text_color="#CCCCCC", anchor="w", justify="left", font=("Arial Rounded MT Bold", 14))
            reminder0.place(relx=0, rely=0.1, anchor="w", x=200, y=350)

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

                if dep_station and dep_station[0].islower():
                    CTkMessagebox(message="Please enter the departure station with a capital letter!", icon="cancel")
                    return
                if arr_station and arr_station[0].islower():
                    CTkMessagebox(message="Please enter the arrival station with a capital letter!", icon="cancel")
                    return

                map_instance = Map(dep_station, arr_station, 0, 0)
                is_connection, distance, duration = map_instance.is_station()

                if is_connection:
                    message = f"Railway connection exists!\nDistance: {distance} km\nDuration: {duration} hours"
                    CTkMessagebox(message=message, icon="check", option_1="Ok")
                    result_text.delete("1.0", "end")
                    result_text.insert("1.0", message)
                    save_btn.configure(state="normal")
                else:
                    CTkMessagebox(title="Error", message="Railway connection doesn't exist", icon="cancel")
                    save_btn.configure(state="disabled")

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

            label1 = CTkLabel(master=screen_frame,
                              text="Enter the stations and check if the railway connection exists:",
                              text_color="#000000", anchor="w", justify="left", font=("Arial Rounded MT Bold", 17))
            label1.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

            label2 = CTkLabel(master=screen_frame,
                              text="Reminder:\nSystem works only with ukrainian cities.\nBegin with capital letter.",
                              text_color="#CCCCCC", anchor="w", justify="left", font=("Arial Rounded MT Bold", 14))
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
                                text_color="#CCCCCC", anchor="w", justify="left", font=("Arial Rounded MT Bold", 14))
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
                        "SELECT ct.cargo_name, c.weight FROM Cargo c INNER JOIN CargoType ct ON c.cargo_type_id = ct.cargo_type_id ORDER BY c.rowid DESC LIMIT 1")
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

            cl_label1 = CTkLabel(master=screen_frame, text="Last step!\nYou have to register the client to the system"
                                                           "\nAfter 'Next step' the contract will be saved",
                                 text_color="#CCCCCC", anchor="w", justify="left", font=("Arial Rounded MT Bold", 14))
            cl_label1.place(relx=0, rely=0.1, anchor="w", x=30, y=50)

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
                        CTkMessagebox(message="Please fill in all the fields", icon="cancel", option_1="OK")
                        return
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        CTkMessagebox(message="Invalid email format!", icon="cancel", option_1="OK")
                        return
                    if len(password) < 8:
                        CTkMessagebox(message="Password should contain at least 8 characters!", icon="cancel",
                                      option_1="OK")
                        return
                    if len(phone_number) < 10 or not phone_number.isdigit():
                        CTkMessagebox(message="Phone number should contain at least 10 digits!", icon="cancel",
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
            cursor.execute("SELECT client_id FROM Client ORDER BY client_id DESC LIMIT 1")
            client_id = cursor.fetchone()[0]

            cursor.execute("SELECT payment_id FROM Payment ORDER BY payment_id DESC LIMIT 1")
            payment_id = cursor.fetchone()[0]

            cursor.execute("SELECT cargo_id FROM Cargo ORDER BY cargo_id DESC LIMIT 1")
            cargo_id = cursor.fetchone()[0]

            cursor.execute("SELECT itinerary_id FROM Itinerary ORDER BY itinerary_id DESC LIMIT 1")
            itinerary_id = cursor.fetchone()[0]

            def create_contract(cursor, dispatcher_id, client_id):
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    cursor.execute(
                        "INSERT INTO Contract (conclusion_date, client_id, payment_id, dispatcher_id, cargo_id, itinerary_id) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (current_datetime, client_id, payment_id, dispatcher_id, cargo_id, itinerary_id))
                    conn.commit()
                    CTkMessagebox(message="Contract saved successfully!", icon="check", option_1="Thanks")
                except sqlite3.Error as e:
                    CTkMessagebox(message="Error", icon="cancel", option_1="OK")

            def enter_pib():
                def save_dispatcher_id():
                    dispatcher_pib = pib_entry.get()
                    client_phone = pib_cl.get()  # Отримуємо номер телефону клієнта
                    cursor.execute("SELECT dispatcher_id FROM Dispatcher WHERE d_pib = ?", (dispatcher_pib,))
                    dispatcher_data = cursor.fetchone()
                    if dispatcher_data:
                        dispatcher_id = dispatcher_data[0]
                        # Додайте запит для отримання айді клієнта за номером телефону
                        cursor.execute("SELECT client_id FROM Client WHERE c_phone_number = ?", (client_phone,))
                        client_data = cursor.fetchone()
                        if client_data:
                            client_id = client_data[0]
                            create_contract(cursor, dispatcher_id,
                                            client_id)  # Передайте айді клієнта в функцію create_contract
                            dialog_window.destroy()
                        else:
                            CTkMessagebox(message="Client with provided phone number not found!", icon="cancel",
                                          option_1="OK")
                    else:
                        CTkMessagebox(message="Dispatcher with provided PIB not found!", icon="cancel", option_1="OK")

                dialog_window = customtkinter.CTk()
                dialog_window.geometry("300x250")
                dialog_window.title("Attention")

                pib_label = customtkinter.CTkLabel(dialog_window, text="Confirm your PIB one more time:")
                pib_label.pack()

                pib_entry = customtkinter.CTkEntry(dialog_window)
                pib_entry.pack()

                pib_cl = customtkinter.CTkLabel(dialog_window, text="Phone number of the client:")
                pib_cl.pack()

                pib_cl = customtkinter.CTkEntry(dialog_window)
                pib_cl.pack()

                confirm_button = customtkinter.CTkButton(dialog_window, text="Confirm", command=save_dispatcher_id)
                confirm_button.pack()
                dialog_window.mainloop()

            enter_pib()

            # def print_contract_data(contract_data):
            #     printer_name = win32print.GetDefaultPrinter()
            #
            #     hprinter = win32print.OpenPrinter(printer_name)
            #     hprinter_start_doc = win32print.StartDocPrinter(hprinter, 1, ("Contract", None, "RAW"))
            #     hprinter_start_page = win32print.StartPagePrinter(hprinter)
            #
            #     dc = win32ui.CreateDC()
            #     dc.CreatePrinterDC(printer_name)
            #     dc.StartDoc("Contract")
            #     dc.StartPage()
            #
            #     # Print contract data
            #     for category, data in contract_data.items():
            #         dc.TextOut(10, 10, f"{category}: {data}")
            #
            #     dc.EndPage()
            #     dc.EndDoc()
            #
            #     win32print.EndPagePrinter(hprinter)
            #     win32print.EndDocPrinter(hprinter)
            #     win32print.ClosePrinter(hprinter)
            # def gather_data(cursor):
            #     try:
            #         # Fetch data from Client table
            #         cursor.execute("SELECT * FROM Client WHERE client_id = (SELECT MAX(client_id) FROM Client)")
            #         client_data = cursor.fetchone()
            #
            #         # Fetch data from Payment table
            #         cursor.execute("SELECT * FROM Payment WHERE payment_id = (SELECT MAX(payment_id) FROM Payment)")
            #         payment_data = cursor.fetchone()
            #
            #         # Fetch data from Dispatcher table
            #         cursor.execute(
            #             "SELECT * FROM Dispatcher WHERE dispatcher_id = (SELECT MAX(dispatcher_id) FROM Dispatcher)")
            #         dispatcher_data = cursor.fetchone()
            #
            #         # Fetch data from Cargo table
            #         cursor.execute("SELECT * FROM Cargo WHERE cargo_id = (SELECT MAX(cargo_id) FROM Cargo)")
            #         cargo_data = cursor.fetchone()
            #
            #         # Fetch data from Itinerary table
            #         cursor.execute(
            #             "SELECT * FROM Itinerary WHERE itinerary_id = (SELECT MAX(itinerary_id) FROM Itinerary)")
            #         itinerary_data = cursor.fetchone()
            #
            #         # Fetch data from CargoType table for cargo_type_id from Cargo table
            #         cursor.execute("SELECT * FROM CargoType WHERE cargo_type_id = ?", (cargo_data[1],))
            #         cargo_type_data = cursor.fetchone()
            #
            #         # Organize gathered data into printable format
            #         contract_data = {
            #             "Client Data": client_data,
            #             "Payment Data": payment_data,
            #             "Dispatcher Data": dispatcher_data,
            #             "Cargo Data": cargo_data,
            #             "Itinerary Data": itinerary_data,
            #             "Cargo Type Data": cargo_type_data
            #         }
            #
            #         # Print contract data
            #         print_contract_data(contract_data)
            #     except sqlite3.Error as e:
            #         CTkMessagebox(message="Error", icon="check", option_1="OK")
            #
            #
            # print_contract = CTkButton(master=screen_frame, text="Print contract", **btn_style,
            #                            command=gather_data(cursor))
            # print_contract.place(relx=0, rely=0.1, anchor="w", x=420, y=100)
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
