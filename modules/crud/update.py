import re
import sqlite3
from datetime import datetime
import customtkinter
from CTkToolTip import *
import customtkinter as ctk
from customtkinter import *
from CTkMessagebox import CTkMessagebox

from classes.Map import Map
from classes.Calc import Calc
from classes.CargoType import CargoType
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