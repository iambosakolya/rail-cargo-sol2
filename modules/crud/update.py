import re
import sqlite3
from datetime import datetime
from CTkToolTip import *
from customtkinter import *
from CTkMessagebox import CTkMessagebox

from classes.Map import Map
from classes.Calc import Calc
from classes.CargoType import CargoType
from database.database_setup import cursor, conn

from modules.print import print_contract

from ui.style import label_style, btn_style, entry_style, btn_style_user

regional_centers = Map.regional_centers


def find_dispatcher(dispatcher_id):
    cursor.execute("SELECT d_pib, d_email, d_password, d_phone_number "
                   "FROM Dispatcher "
                   "WHERE dispatcher_id = ?", (dispatcher_id,))
    dispatcher = cursor.fetchone()

    if dispatcher:
        update_dispatcher(dispatcher)

def update_dispatcher(dispatcher):
    (existing_pib, existing_email, existing_password,
     existing_phone_number) = dispatcher

    update_dispatcher_window = CTk()
    update_dispatcher_window.title("Update Dispatcher info")

    screen_width = update_dispatcher_window.winfo_screenwidth()
    screen_height = update_dispatcher_window.winfo_screenheight()

    app_width = 500
    app_height = 400

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    update_dispatcher_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    update_dispatcher_window.resizable(0, 0)

    screen_frame = CTkFrame(master=update_dispatcher_window, width=850, height=750, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    CTkLabel(master=screen_frame, text="PIB:", **label_style).pack(anchor="w", pady=(18, 0), padx=(50, 0))
    pib_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
    pib_entry.insert(0, existing_pib)
    pib_entry.pack(anchor="w", padx=(50, 0))

    CTkLabel(master=screen_frame, text="Phone number (+38):", **label_style).pack(anchor="w", pady=(18, 0), padx=(50, 0))
    phone_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
    phone_entry.insert(0, existing_phone_number)
    phone_entry.pack(anchor="w", padx=(50, 0))

    CTkLabel(master=screen_frame, text="Email:", **label_style).pack(anchor="w", pady=(18, 0), padx=(50, 0))
    email_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
    email_entry.insert(0, existing_email)
    email_entry.pack(anchor="w", padx=(50, 0))

    CTkLabel(master=screen_frame, text="Password:", **label_style).pack(anchor="w", pady=(15, 0), padx=(50, 0))
    password_entry = CTkEntry(master=screen_frame, **entry_style, width=300, show="*")
    password_entry.insert(0, existing_password)
    password_entry.pack(anchor="w", padx=(50, 0))

    def update_dispatcher_info():
        new_pib = pib_entry.get()
        new_email = email_entry.get()
        new_password = password_entry.get()
        new_phone_number = phone_entry.get()

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
            "UPDATE Dispatcher "
            "SET d_pib = ?, d_email = ?, d_password = ?, d_phone_number = ? "
            "WHERE d_email = ?",
            (new_pib, new_email, new_password, new_phone_number, existing_email)
        )
        conn.commit()

        CTkMessagebox(message="Information updated successfully!",
                      icon="check",
                      option_1="Thanks")
        update_dispatcher_window.destroy()

    update_button = CTkButton(master=screen_frame,
                              text="Update Info", **btn_style_user,
                              command=update_dispatcher_info)

    update_button.pack(anchor="w", pady=(20, 0), padx=(50, 0))

    update_dispatcher_window.mainloop()

def find_client(user_id):
    cursor.execute("SELECT c_pib, c_email, c_password, c_phone_number "
                   "FROM Client "
                   "WHERE client_id = ?", (user_id,))
    client = cursor.fetchone()

    if client:
        update_client(client)

def update_client(client):
    existing_pib, existing_email, existing_password, existing_phone_number = client

    update_client_window = CTk()
    update_client_window.title("Update client info")

    screen_width = update_client_window.winfo_screenwidth()
    screen_height = update_client_window.winfo_screenheight()

    app_width = 500
    app_height = 400

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    update_client_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    update_client_window.resizable(0, 0)

    screen_frame = CTkFrame(master=update_client_window, width=850, height=750, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    CTkLabel(master=screen_frame, text="PIB:", **label_style).pack(anchor="w", pady=(18, 0), padx=(50, 0))
    pib_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
    pib_entry.insert(0, existing_pib)
    pib_entry.pack(anchor="w", padx=(50, 0))

    CTkLabel(master=screen_frame, text="Phone number (+38):", **label_style).pack(anchor="w", pady=(18, 0), padx=(50, 0))
    phone_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
    phone_entry.insert(0, existing_phone_number)
    phone_entry.pack(anchor="w", padx=(50, 0))

    CTkLabel(master=screen_frame, text="Email:", **label_style).pack(anchor="w", pady=(18, 0), padx=(50, 0))
    email_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
    email_entry.insert(0, existing_email)
    email_entry.pack(anchor="w", padx=(50, 0))

    CTkLabel(master=screen_frame, text="Password:", **label_style).pack(anchor="w", pady=(15, 0), padx=(50, 0))
    password_entry = CTkEntry(master=screen_frame, **entry_style, width=300, show="*")
    password_entry.insert(0, existing_password)
    password_entry.pack(anchor="w", padx=(50, 0))

    def update_client_info():
        new_pib = pib_entry.get()
        new_email = email_entry.get()
        new_password = password_entry.get()
        new_phone_number = phone_entry.get()

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
            "UPDATE Client "
            "SET c_pib = ?, c_email = ?, c_password = ?, c_phone_number = ?"
            " WHERE c_email = ?",
            (new_pib, new_email, new_password, new_phone_number, existing_email)
        )
        conn.commit()

        CTkMessagebox(message="Information updated successfully!",
                      icon="check",
                      option_1="Thanks")
        update_client_window.destroy()

    update_button = CTkButton(master=screen_frame, text="Update Info", **btn_style_user,
                              command=update_client_info)

    update_button.pack(anchor="w", pady=(20, 0), padx=(50, 0))

    update_client_window.mainloop()


def fetch_contract_data(contract_id):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''
                SELECT Contract.contract_id, Contract.conclusion_date,
                 Client.c_email, Client.c_phone_number, Client.c_pib, 
                 Dispatcher.d_pib, CargoType.cargo_name,
                 CargoType.description, CargoType.dimensions, Cargo.quantity, 
                 Cargo.weight, Itinerary.departure_station, Itinerary.arrival_station,
                 Itinerary.route_length, Itinerary.duration, Payment.payment_amount,
                 Payment.payment_datetime, Cargo.cargo_type_id, Cargo.cargo_id

                FROM Contract JOIN Client ON Contract.client_id = Client.client_id
                JOIN Dispatcher ON Contract.dispatcher_id = Dispatcher.dispatcher_id
                JOIN Cargo ON Contract.cargo_id = Cargo.cargo_id
                JOIN CargoType ON Cargo.cargo_type_id = CargoType.cargo_type_id
                JOIN Itinerary ON Contract.itinerary_id = Itinerary.itinerary_id
                JOIN Payment ON Contract.payment_id = Payment.payment_id
                WHERE Contract.contract_id = ?
            ''', (contract_id,))
        data = cursor.fetchone()
        conn.close()

        if data:
            return {
                "contract_id": data[0],
                "conclusion_date": data[1],
                "client_email": data[2],
                "client_phone": data[3],
                "client_pib": data[4],
                "dispatcher_pib": data[5],
                "cargo_name": data[6],
                "cargo_description": data[7],
                "cargo_dimensions": data[8],
                "cargo_quantity": data[9],
                "cargo_weight": data[10],
                "departure_station": data[11],
                "arrival_station": data[12],
                "route_length": data[13],
                "duration": data[14],
                "payment_amount": data[15],
                "payment_datetime": data[16],
                "cargo_type_id": data[17],
                "cargo_id": data[18]
            }
        else:
            return None
    except sqlite3.Error as e:
        CTkMessagebox(message=f"Error fetching contract data: {e}", icon="cancel")
        return None


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

    if not contract_id:
        return

    try:
        contract_id = int(contract_id)
    except ValueError:
        CTkMessagebox(title="Error", message="Invalid contract ID", icon="cancel")
        return

    contract_data = fetch_contract_data(contract_id)

    if not contract_data:
        CTkMessagebox(title="Error", message="Contract not found", icon="cancel")
        return

    def next_step():
        nonlocal window_number
        window_number += 1
        show_current_step(contract_id)

    def show_current_step(contract_id):
        global screen_frame
        screen_frame.destroy()
        screen_frame = CTkFrame(master=cont_window, width=850, height=750, fg_color="#897E9B")
        screen_frame.pack_propagate(0)
        screen_frame.pack(expand=True, fill="both")


        if window_number == 1:
            data_text = f"""
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
                           """

            text_box = CTkTextbox(screen_frame, width=400, height=400)
            text_box.pack(padx=60, pady=130, fill='both', expand=False)
            text_box.insert('1.0', data_text)
            text_box.configure(state='disabled')

            info_label = CTkLabel(master=screen_frame, text="Here can modify:\n1 Cargo info and route info"
                                                            "\n2 Payment sum will be calculated automatically",
                                  text_color="#CCCCCC", anchor="w", justify="left",
                                  font=("Arial Rounded MT Bold", 16))
            info_label.place(relx=0, rely=0.1, anchor="w", x=60, y=15)

            next_btn = CTkButton(master=screen_frame, text="Next", **btn_style_user,
                                 command=next_step)
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
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE CargoType SET cargo_name = ?, description = ?, dimensions = ? "
                        "WHERE cargo_type_id = ?",
                        (cargo_name, description, dimensions, contract_data['cargo_type_id']))

                    cursor.execute("UPDATE Cargo SET quantity = ?, weight = ? "
                                   "WHERE cargo_id = ?",
                                   (quantity, weight, contract_data['cargo_id']))
                    conn.commit()
                    CTkMessagebox(message="Cargo information updated successfully", icon="check", option_1="OK")
                    conn.close()
                except sqlite3.Error as e:
                    CTkMessagebox(message="An error occurred", icon="cancel", option_1="OK")

            type_label = CTkLabel(master=screen_frame, text="Choose new cargo type:",
                                  **label_style)
            type_label.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

            initial_values = ['Freight', 'Coal', 'Grains', 'Steel', 'Lumber', 'Oil', 'Chemicals', 'Machinery',
                              'Automobiles', 'Containers', 'Livestock', 'Cement', 'Fertilizer', 'Papers']

            type_combobox = CTkComboBox(screen_frame, values=[contract_data['cargo_name']] + initial_values, width=250)
            type_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=45)
            type_combobox.set(contract_data['cargo_name'])

            add_label = CTkLabel(master=screen_frame, text="Or enter new type:",
                                 **label_style)
            add_label.place(relx=0, rely=0.1, anchor="w", x=420, y=5)

            type_entry = CTkEntry(master=screen_frame, width=140)
            type_entry.place(relx=0, rely=0.1, anchor="w", x=420, y=45)

            def new_type():
                new_cargo_type = type_entry.get().strip()
                if new_cargo_type == "":
                    return
                existing_cargo_types = list(type_combobox.cget('values'))
                existing_cargo_types.append(new_cargo_type)
                type_combobox.configure(values=existing_cargo_types)

            add_button = CTkButton(master=screen_frame, text="Add", width=40,
                                   **btn_style_user, command=new_type)
            add_button.place(relx=0, rely=0.1, anchor="w", x=350, y=45)

            desc_label = CTkLabel(master=screen_frame, text="Add description (if necessary):",
                                  **label_style)
            desc_label.place(relx=0, rely=0.1, anchor="w", x=30, y=185)

            desc_entry = CTkEntry(master=screen_frame, width=350, height=50)
            desc_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=225)
            desc_entry.insert(0, contract_data['cargo_description'])

            dim_label = CTkLabel(master=screen_frame, text="Enter dimensions:",
                                 **label_style)
            dim_label.place(relx=0, rely=0.1, anchor="w", x=30, y=95)
            dim_entry = CTkEntry(master=screen_frame, width=150, height=30)

            dim_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=135)
            dim_entry.insert(0, contract_data['cargo_dimensions'])

            quantity_label = CTkLabel(master=screen_frame, text="Enter quantity:",
                                      **label_style)
            quantity_label.place(relx=0, rely=0.1, anchor="w", x=420, y=185)
            quantity_input = CTkEntry(master=screen_frame, width=150, height=30)
            quantity_input.place(relx=0, rely=0.1, anchor="w", x=420, y=225)
            quantity_input.insert(0, contract_data['cargo_quantity'])

            weight_label = CTkLabel(master=screen_frame, text="Enter weight (tons):",
                                    **label_style)
            weight_label.place(relx=0, rely=0.1, anchor="w", x=420, y=95)

            weight_input = CTkEntry(master=screen_frame, width=150, height=30)
            weight_input.place(relx=0, rely=0.1, anchor="w", x=420, y=135)
            weight_input.insert(0, contract_data['cargo_weight'])

            def cargo_type_check(cargo_obj):
                if cargo_obj.isCargoType():
                    CTkMessagebox(message="Cargo type is available",
                                  icon="check",
                                  option_1="Thanks")
                    update_btn.configure(state="normal")
                else:
                    CTkMessagebox(title="Error",
                                  message="This cargo type is not available!",
                                  icon="cancel")
                    update_btn.configure(state="disabled")

            check_btn = CTkButton(master=screen_frame, text="Check availability", **btn_style_user,
                                  command=lambda: cargo_type_check(
                                      CargoType(type_combobox.get(), dim_entry.get(), weight_input.get(),
                                                quantity_input.get(), desc_entry.get())))
            check_btn.place(relx=0, rely=0.1, anchor="w", x=30, y=300)

            update_btn = CTkButton(screen_frame, text="Update cargo", **btn_style_user,
                                   command=update_cargo)
            update_btn.place(relx=0, rely=0.1, anchor="w", x=200, y=300)
            update_btn.configure(state="disabled")

            next_btn = CTkButton(master=screen_frame, text="Next", **btn_style_user,
                                 command=next_step)
            next_btn.place(relx=0.9, rely=0.9, anchor="se")

        elif window_number == 3:
            def fetch_stations():
                conn = sqlite3.connect('data.db')
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT departure_station "
                               "FROM Itinerary")
                dep_stations = [row[0] for row in cursor.fetchall()]
                cursor.execute("SELECT DISTINCT arrival_station "
                               "FROM Itinerary")
                arr_stations = [row[0] for row in cursor.fetchall()]
                conn.close()
                return dep_stations, arr_stations

            def update_station():
                old_dep_station = dep_combobox.get().strip()
                new_dep_station = new_dep_combobox.get().strip()
                old_arr_station = arr_combobox.get().strip()
                new_arr_station = new_arr_combobox.get().strip()

                try:
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()

                    cursor.execute("UPDATE Itinerary "
                                   "SET departure_station = ? "
                                   "WHERE departure_station = ?",
                                   (new_dep_station, old_dep_station))

                    cursor.execute("UPDATE Itinerary "
                                   "SET arrival_station = ? "
                                   "WHERE arrival_station = ?",
                                   (new_arr_station, old_arr_station))

                    map_obj = Map(new_dep_station, new_arr_station, 0, 0)
                    is_connection, distance, duration = map_obj.is_station()

                    if is_connection:
                        cursor.execute(
                            "UPDATE Itinerary SET route_length = ?, duration = ? "
                            "WHERE departure_station = ? "
                            "AND arrival_station = ?",
                            (distance, duration, new_dep_station, new_arr_station))
                        conn.commit()
                        CTkMessagebox(message="Stations and route details updated successfully!",
                                      icon="info",
                                      option_1="Ok")
                    else:
                        conn.rollback()
                        CTkMessagebox(message="Cannot find railway connection between the updated stations",
                                      icon="cancel")

                    conn.close()
                    refresh_comboboxes()
                except sqlite3.Error as e:
                    CTkMessagebox(message=f"Error updating stations: {e}",
                                  icon="cancel")

            def refresh_comboboxes():
                dep_stations, arr_stations = fetch_stations()
                dep_combobox.configure(values=[contract_data["departure_station"]])
                arr_combobox.configure(values=[contract_data["arrival_station"]])
                new_dep_combobox.configure(values=regional_centers)
                new_arr_combobox.configure(values=regional_centers)

            screen_frame.destroy()
            screen_frame = CTkFrame(master=cont_window, width=850, height=750, fg_color="#897E9B")
            screen_frame.pack_propagate(0)
            screen_frame.pack(expand=True, fill="both")

            label1 = CTkLabel(master=screen_frame, text="Update stations", text_color="#000000", anchor="w",
                              justify="left", font=("Arial Rounded MT Bold", 17))
            label1.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

            dep_label = CTkLabel(master=screen_frame, text="Select current departure station:", **label_style)
            dep_label.place(relx=0, rely=0.1, anchor="w", x=30, y=50)

            dep_combobox = CTkComboBox(master=screen_frame, values=[contract_data["departure_station"]], width=300)
            dep_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=80)

            new_dep_label = CTkLabel(master=screen_frame, text="Select new departure station:", **label_style)
            new_dep_label.place(relx=0, rely=0.1, anchor="w", x=30, y=110)

            new_dep_combobox = CTkComboBox(master=screen_frame, values=regional_centers, width=300)
            new_dep_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=140)

            arr_label = CTkLabel(master=screen_frame, text="Select current arrival station:", **label_style)
            arr_label.place(relx=0, rely=0.1, anchor="w", x=30, y=170)

            arr_combobox = CTkComboBox(master=screen_frame, values=[contract_data["arrival_station"]], width=300)
            arr_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=200)

            new_arr_label = CTkLabel(master=screen_frame, text="Select new arrival station:", **label_style)
            new_arr_label.place(relx=0, rely=0.1, anchor="w", x=30, y=230)

            new_arr_combobox = CTkComboBox(master=screen_frame, values=regional_centers, width=300)
            new_arr_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=260)

            update_btn = CTkButton(master=screen_frame, text="Update stations", width=90, **btn_style_user,
                                   command=update_station)
            update_btn.place(relx=0, rely=0.1, anchor="w", x=30, y=300)

            next_btn = CTkButton(master=screen_frame, text="Next", **btn_style_user, command=next_step)
            next_btn.place(relx=0.9, rely=0.9, anchor="se")

            refresh_comboboxes()

        elif window_number == 4:

            payment_label = CTkLabel(master=screen_frame, text="Almost done!\nNow make the payment",
                                     text_color="#000000", anchor="w",
                                     justify="left", font=("Arial Rounded MT Bold", 18))
            payment_label.place(relx=0, rely=0.1, anchor="w", x=30, y=10)

            list_label = CTkLabel(master=screen_frame,
                                  text="Click button 'Accept payment' to see the price for the transportation"
                                       "\nand save the payment",
                                  text_color="#CCCCCC", anchor="w", justify="left",
                                  font=("Arial Rounded MT Bold", 14))
            list_label.place(relx=0, rely=0.1, anchor="w", x=30, y=80)

            def update_payment(calculated_tariff, contract_id):
                try:
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()

                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    cursor.execute(
                        "UPDATE Payment SET payment_amount = ?, payment_datetime = ? "
                        "WHERE payment_id = (SELECT payment_id FROM Contract WHERE contract_id = ?)",
                        (calculated_tariff, current_datetime, contract_id))

                    conn.commit()
                    conn.close()
                    CTkMessagebox(message="Payment updated successfully!",
                                  icon="check", option_1="Thanks")
                except sqlite3.Error as e:
                    CTkMessagebox(message="Payment is not updated!", icon="cancel", option_1="OK")

            def calculate_tariff(contract_id):
                global calculated_tariff
                try:
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()

                    cursor.execute('''
                        SELECT ct.cargo_name, c.weight
                        FROM Cargo c
                        INNER JOIN CargoType ct ON c.cargo_type_id = ct.cargo_type_id
                        WHERE c.cargo_id = (
                            SELECT cargo_id
                            FROM Contract
                            WHERE contract_id = ?
                        )
                    ''', (contract_id,))
                    cargo_data = cursor.fetchone()

                    cursor.execute('''
                        SELECT route_length, duration
                        FROM Itinerary
                        WHERE itinerary_id = (
                            SELECT itinerary_id
                            FROM Contract
                            WHERE contract_id = ?
                        )
                    ''', (contract_id,))
                    route_data = cursor.fetchone()
                    conn.close()

                    if cargo_data and route_data:
                        cargo_type, weight = cargo_data
                        distance, duration = route_data

                        calc_obj = Calc(None, distance, None, duration, cargo_type, weight)
                        calc_obj.calculate_price()
                        calculated_tariff = calc_obj.get_price()
                        update_payment(calculated_tariff, contract_id)

                        textbox1.configure(state="normal")
                        textbox1.delete("1.0", "end")
                        textbox1.insert("end", f"Calculated tariff: {calculated_tariff}₴")
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
                    row_data = f"{cargo_type:<40}{weight:<40}{distance:<40}{duration:<40}\n"
                    table_data = headers + row_data
                    textbox.insert("end", table_data)
                    textbox.configure(state="disabled")

            def display():
                try:
                    calculate_tariff(contract_id)
                except sqlite3.Error as e:
                    CTkMessagebox(message="Error", icon="cancel", option_1="OK")

            display_button = CTkButton(master=screen_frame, text="Accept payment", **btn_style_user, width=90, command=display)
            display_button.place(relx=0, rely=0.1, anchor="w", x=30, y=350)

            textbox = CTkTextbox(master=screen_frame, width=500, height=80)
            textbox.place(relx=0, rely=0.1, anchor="w", x=30, y=155)
            textbox1 = CTkTextbox(master=screen_frame, width=500, height=80)
            textbox1.place(relx=0, rely=0.1, anchor="w", x=30, y=255)

            next_btn = CTkButton(master=screen_frame, text="Next step", **btn_style_user, command=next_step)
            next_btn.place(relx=0, rely=0.1, anchor="w", x=420, y=400)

        elif window_number == 5:
            def finish():
                cont_window.destroy()

            finish_btn = CTkButton(master=screen_frame, text="Finish",
                                       **btn_style_user, command=finish)
            finish_btn.place(relx=0, rely=0, anchor="w", x=220, y=280)

    show_current_step(contract_id)
    cont_window.mainloop()
