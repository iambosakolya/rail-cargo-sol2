import sqlite3
from datetime import datetime, timedelta
import datetime
import customtkinter as ctk

import customtkinter
import customtkinter as ctk
from customtkinter import *
from CTkMessagebox import CTkMessagebox

label_style = {
    "text_color": "#000000",
    "anchor": "w",
    "justify": "left",
    "font": ("Arial Rounded MT Bold", 15)
}

# 1 Вибір з декількох таблиць із сортуванням
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
    cursor.execute(query,
                   (dispatcher_pib,))
    contracts = cursor.fetchall()
    conn.close()
    return contracts
def find_contracts_pib():
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

    label = ctk.CTkLabel(screen_frame, text="Enter Dispatcher PIB:", **label_style)
    label.pack(pady=10)

    entry = ctk.CTkEntry(screen_frame)
    entry.pack(pady=10)

    def on_confirm():
        dispatcher_pib = entry.get()
        if dispatcher_pib:
            root.destroy()
            contracts = get_contracts_by_pib(dispatcher_pib)
            if not contracts:
                CTkMessagebox(message="No contracts found for the given dispatcher PIB!"
                                      "\nTry again!",
                              icon="cancel",
                              option_1="OK")
                return

            result_window = ctk.CTkToplevel()
            result_window.title("Contracts by dispatcher")

            screen_width = result_window.winfo_screenwidth()
            screen_height = result_window.winfo_screenheight()

            app_width = 450
            app_height = 350

            x_position = (screen_width - app_width) // 2
            y_position = (screen_height - app_height) // 2

            result_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
            result_window.resizable(0, 0)

            screen_frame = ctk.CTkFrame(master=result_window, width=450, height=250, fg_color="#FFFFFF")
            screen_frame.pack_propagate(0)
            screen_frame.pack(expand=True, fill="both", padx=10, pady=10)

            label = ctk.CTkLabel(master=screen_frame, text="A list of contracts that were created"
                                                           "\n by the specified dispatcher", **label_style)
            label.pack(pady=10)

            text_box = ctk.CTkTextbox(master=screen_frame, height=170, wrap="none")
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

            def on_close():
                result_window.destroy()

            close_button = ctk.CTkButton(result_window, text="OK", command=on_close, fg_color="#FFFFFF",
                                         hover_color="#897E9B", text_color="#000000",
                                         font=("Arial Rounded MT Bold", 13))
            close_button.pack(pady=10)


    button = ctk.CTkButton(screen_frame, text="Submit", command=on_confirm, fg_color="#000000",
                           hover_color="#4F2346", text_color="#ffffff", font=("Arial Rounded MT Bold", 13))
    button.pack(pady=10)

    root.mainloop()

# 2 Завдання умови відбору з використанням предиката LІKE
# знайти всіх клієнтів, чиє прізвище починається на задану букву
def get_clients_letter(letter):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        client_id, c_pib, c_phone_number
    FROM Client
    WHERE c_pib LIKE ?
    ORDER BY c_pib;
    '''
    cursor.execute(query, (letter + '%',))
    clients = cursor.fetchall()
    conn.close()
    return clients
def find_clients():
    root = ctk.CTkToplevel()
    root.title("Find clients by surname letter")

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

    label = ctk.CTkLabel(screen_frame, text="Enter surname initial first letter:",
                         **label_style)
    label.pack(pady=10)

    entry = ctk.CTkEntry(screen_frame)
    entry.pack(pady=10)

    def on_confirm():
        letter = entry.get()
        if letter:
            root.destroy()
            clients = get_clients_letter(letter)
            if not clients:
                CTkMessagebox(message="No clients found for the given initial!"
                                      "\nTry again!",
                              icon="cancel",
                              option_1="OK")
                return

            result_window = ctk.CTkToplevel()
            result_window.title("Clients by surname initial")

            screen_width = result_window.winfo_screenwidth()
            screen_height = result_window.winfo_screenheight()

            app_width = 450
            app_height = 350

            x_position = (screen_width - app_width) // 2
            y_position = (screen_height - app_height) // 2

            result_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
            result_window.resizable(0, 0)

            screen_frame = ctk.CTkFrame(master=result_window, width=450, height=250, fg_color="#FFFFFF")
            screen_frame.pack_propagate(0)
            screen_frame.pack(expand=True, fill="both", padx=10, pady=10)

            label = ctk.CTkLabel(master=screen_frame, text="A list of clients whose surname starts"
                                                           "\n with the specified initial", **label_style)
            label.pack(pady=10)

            text_box = ctk.CTkTextbox(master=screen_frame, height=150, wrap="none")
            text_box.pack(expand=True, fill="both", padx=10, pady=10)

            for client in clients:
                text_box.insert("end",
                                f"Client PIB: {client[1]} \nPhone: {client[2]}\n"
                                "---------------------------------\n")

            def on_close():
                result_window.destroy()

            close_button = ctk.CTkButton(result_window, text="OK", command=on_close, fg_color="#FFFFFF",
                                         hover_color="#897E9B", text_color="#000000",
                                         font=("Arial Rounded MT Bold", 13))
            close_button.pack(pady=10)

    submit_button = ctk.CTkButton(screen_frame, text="Submit", command=on_confirm, fg_color="#000000",
                                  hover_color="#4F2346", text_color="#ffffff", font=("Arial Rounded MT Bold", 13))
    submit_button.pack(pady=10)



    root.mainloop()

# 3 Завдання умови відбору з використанням предиката BETWEEN
# список контрактів, які були згенеровані в заданий період
def get_contracts_by_date(start_date, end_date):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        contract_id, conclusion_date
    FROM Contract
    WHERE conclusion_date BETWEEN ? AND ?
    ORDER BY conclusion_date;
    '''
    cursor.execute(query, (start_date, end_date))
    contracts = cursor.fetchall()
    conn.close()
    return contracts

def find_contracts_date():
    root = ctk.CTkToplevel()
    root.title("Find contracts by date range")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    app_width = 300
    app_height = 600

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    root.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    root.resizable(0, 0)

    screen_frame = ctk.CTkFrame(master=root, width=300, height=300, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    # Function to get month values
    def get_month_values():
        months = [
            "1 (January)", "2 (February)", "3 (March)", "4 (April)", "5 (May)", "6 (June)",
            "7 (July)", "8 (August)", "9 (September)", "10 (October)", "11 (November)", "12 (December)"
        ]
        return months

    # Start date
    label_start = ctk.CTkLabel(screen_frame, text="Select start date:", **label_style)
    label_start.pack(pady=5)

    label_start_year = ctk.CTkLabel(screen_frame, text="Year:", **label_style)
    label_start_year.pack(pady=5)
    start_year_combobox = ctk.CTkComboBox(
        screen_frame,
        values=[str(year) for year in range(2024, datetime.date.today().year + 1)]
    )
    start_year_combobox.pack(pady=5)

    label_start_month = ctk.CTkLabel(screen_frame, text="Month:", **label_style)
    label_start_month.pack(pady=5)
    start_month_combobox = ctk.CTkComboBox(screen_frame, values=get_month_values())
    start_month_combobox.pack(pady=5)

    label_start_day = ctk.CTkLabel(screen_frame, text="Date:", **label_style)
    label_start_day.pack(pady=5)
    start_day_combobox = ctk.CTkComboBox(screen_frame, values=[str(day) for day in range(1, 32)])
    start_day_combobox.pack(pady=5)

    # End Date Selection
    label_end = ctk.CTkLabel(screen_frame, text="Select end date:", **label_style)
    label_end.pack(pady=5)

    label_end_year = ctk.CTkLabel(screen_frame, text="Year:", **label_style)
    label_end_year.pack(pady=5)
    end_year_combobox = ctk.CTkComboBox(
        screen_frame,
        values=[str(year) for year in range(2024, datetime.date.today().year + 1)]
    )
    end_year_combobox.pack(pady=5)

    label_end_month = ctk.CTkLabel(screen_frame, text="Month:", **label_style)
    label_end_month.pack(pady=5)
    end_month_combobox = ctk.CTkComboBox(screen_frame, values=get_month_values())
    end_month_combobox.pack(pady=5)

    label_end_day = ctk.CTkLabel(screen_frame, text="Date:", **label_style)
    label_end_day.pack(pady=5)
    end_day_combobox = ctk.CTkComboBox(screen_frame, values=[str(day) for day in range(1, 32)])
    end_day_combobox.pack(pady=5)

    def on_confirm():
        try:
            s_year, s_month, s_day = int(start_year_combobox.get()), int(start_month_combobox.get().split()[0]), int(start_day_combobox.get())
            e_year, e_month, e_day = int(end_year_combobox.get()), int(end_month_combobox.get().split()[0]), int(end_day_combobox.get())
            start_date = datetime.date(s_year, s_month, s_day)
            end_date = datetime.date(e_year, e_month, e_day)

            if start_date and end_date:
                root.destroy()
                contracts = get_contracts_by_date(start_date, end_date)
                if not contracts:
                    CTkMessagebox(message="No contracts found for the given date range!\nTry again!",
                                  icon="cancel",
                                  option_1="OK")
                    return

                result_window = ctk.CTkToplevel()
                result_window.title("Contracts by date range")

                screen_width = result_window.winfo_screenwidth()
                screen_height = result_window.winfo_screenheight()

                app_width = 450
                app_height = 350

                x_position = (screen_width - app_width) // 2
                y_position = (screen_height - app_height) // 2

                result_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
                result_window.resizable(0, 0)

                screen_frame = ctk.CTkFrame(master=result_window, width=450, height=250, fg_color="#FFFFFF")
                screen_frame.pack_propagate(0)
                screen_frame.pack(expand=True, fill="both", padx=10, pady=10)

                label = ctk.CTkLabel(master=screen_frame, text="A list of contracts that were created"
                                                               "\n in the specified period", **label_style)
                label.pack(pady=10)

                text_box = ctk.CTkTextbox(master=screen_frame, height=150, wrap="none")
                text_box.pack(expand=True, fill="both", padx=10, pady=10)

                for contract in contracts:
                    text_box.insert("end",
                                    f"Contract ID: {contract[0]} \nConclusion date: {contract[1]}\n"
                                    "---------------------------------\n")

                def on_close():
                    result_window.destroy()

                close_button = ctk.CTkButton(result_window, text="OK", command=on_close, fg_color="#FFFFFF",
                                             hover_color="#897E9B", text_color="#000000",
                                             font=("Arial Rounded MT Bold", 13))
                close_button.pack(pady=10)
        except ValueError:
            CTkMessagebox(message="Invalid date selected! Please select valid dates.",
                          icon="cancel",
                          option_1="OK")

    submit_button = ctk.CTkButton(screen_frame, text="Submit", command=on_confirm, fg_color="#000000",
                                  hover_color="#4F2346", text_color="#ffffff", font=("Arial Rounded MT Bold", 13))
    submit_button.pack(pady=10)

    root.mainloop()

# 4 Агрегатна функція без угруповання
# скільки контрактів було укладено за останній тиждень
def get_contracts_last_week():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = '''
    SELECT COUNT(*) AS contracts_last_week
    FROM Contract
    WHERE conclusion_date BETWEEN DATE('now', '-7 days') AND DATE('now');
    '''
    cursor.execute(query)
    count = cursor.fetchone()[0]
    conn.close()
    return count
def find_contracts_week(result_textbox):
    count = get_contracts_last_week()
    result_textbox.delete("1.0", "end")
    result_textbox.insert("1.0", f"Number of contracts made last week: {count}")

# 5 Агрегатна функція з угрупованням
# Скільки контрактів було укладено кожним диспетчером
def get_contracts_dispatcher():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = '''
    SELECT dispatcher_id, COUNT(*) AS contracts_count
    FROM Contract
    GROUP BY dispatcher_id;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results
def find_contracts_dispatcher(result_textbox):
    results = get_contracts_dispatcher()
    result_textbox.delete("1.0", "end")
    for dispatcher_id, count in results:
        result_textbox.insert("end", f"Dispatcher {dispatcher_id}: {count} contracts\n")

# 6 Використання предиката ALL або ANY
# Хто з диспетчерів уклав найбільшу кількість контрактів
def get_max_contracts():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = '''
    SELECT dispatcher_id, MAX(contract_count) AS max_contracts
    FROM (
        SELECT dispatcher_id, COUNT(*) AS contract_count
        FROM Contract
        GROUP BY dispatcher_id
    )
    '''
    cursor.execute(query)
    result = cursor.fetchone()

    if result and result[0] is not None:
        dispatcher_id = result[0]
        max_contracts = result[1]
        query = '''
        SELECT d_pib
        FROM Dispatcher
        WHERE dispatcher_id = ?;
        '''
        cursor.execute(query, (dispatcher_id,))
        d_pib_result = cursor.fetchone()

        if d_pib_result:
            d_pib = d_pib_result[0]
        else:
            d_pib = None
    else:
        d_pib = None

    conn.close()
    return d_pib


def find_max_contracts(result_textbox):
    d_pib = get_max_contracts()
    result_textbox.delete("1.0", "end")
    if d_pib:
        result_textbox.insert("1.0", f"Dispatcher with max contracts: {d_pib}")
    else:
        result_textbox.insert("1.0", "No data available")

# 7 Корельований підзапит
# знайти клієнтів, які зробили найбільші оплати для кожного типу вантажу, відобразити відповідні дані.
def get_max_payment_clients():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = '''
    SELECT c.client_id, c.c_pib, ct.cargo_name, p.payment_amount
    FROM Client c
    JOIN Contract co ON c.client_id = co.client_id
    JOIN Payment p ON co.payment_id = p.payment_id
    JOIN Cargo ca ON co.cargo_id = ca.cargo_id
    JOIN CargoType ct ON ca.cargo_type_id = ct.cargo_type_id
    WHERE p.payment_amount = (
        SELECT MAX(p2.payment_amount)
        FROM Contract co2
        JOIN Payment p2 ON co2.payment_id = p2.payment_id
        JOIN Cargo ca2 ON co2.cargo_id = ca2.cargo_id
        WHERE ca2.cargo_type_id = ct.cargo_type_id
    )
    ORDER BY ct.cargo_name;
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results
def find_max_payment(result_textbox):
    results = get_max_payment_clients()
    result_textbox.delete("1.0", "end")
    if results:
        for client_id, c_pib, cargo_name, payment_amount in results:
            result_textbox.insert("end", f"\nClient ID: {client_id}\nPIB: {c_pib}\nCargo: {cargo_name}\nPayment: {payment_amount}\n"
                                         f"---------------------------------\n")
    else:
        result_textbox.insert("1.0", "No data available")

# 8 Запит на заперечення
# Запит реалізувати у трьох варіантах: з використанням LEFT JOІN, предиката ІN і предиката EXІSTS;
# хто з диспетчерів не укладав контракти на цьому тижні?

# def get_dispatchers_without_contract():
#     conn = sqlite3.connect('data.db')
#     cursor = conn.cursor()
#
#     # запит з використанням LEFT JOIN
#     query = '''
#     SELECT d.dispatcher_id, d.d_pib
#     FROM Dispatcher d
#     LEFT JOIN Contract c ON d.dispatcher_id = c.dispatcher_id
#     WHERE c.dispatcher_id IS NULL
#     '''
#
#     cursor.execute(query)
#     results = cursor.fetchall()
#
#     conn.close()
#
#     return results

def get_dispatchers_without_contract():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # SQL-запит з використанням предиката IN
    query = '''
    SELECT dispatcher_id, d_pib
    FROM Dispatcher
    WHERE dispatcher_id NOT IN (
        SELECT dispatcher_id
        FROM Contract
    )
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    return results

# def get_dispatchers_without_contract():
#     conn = sqlite3.connect('data.db')
#     cursor = conn.cursor()
#
#     # SQL-запит з використанням предиката EXISTS
#     query = '''
#     SELECT dispatcher_id, d_pib
#     FROM Dispatcher d
#     WHERE NOT EXISTS (
#         SELECT 1
#         FROM Contract c
#         WHERE d.dispatcher_id = c.dispatcher_id
#     )
#     '''
#
#     cursor.execute(query)
#     results = cursor.fetchall()
#
#     conn.close()
#
#     return results

def find_dispatchers(result_textbox):
    results = get_dispatchers_without_contract()
    result_textbox.delete("1.0", "end")
    if results:
        for dispatcher_id, d_pib in results:
            result_textbox.insert("end", f"\nDispatcher PIB: {d_pib}\n"
                                         f"---------------------------------\n")
    else:
        result_textbox.insert("1.0", "No data available")

# 9 Операція об'єднання UNІON із включенням коментарю в кожен рядок
# список усіх диспетчерів з коментарем «Має максимальну кількість заключених контрактів»,
# «Не має в цей час заключених контрактів», "має n заклюених контрактів);
def get_dispatchers_comments():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = '''
    SELECT d.dispatcher_id, d.d_pib, 'Has maximum signed contracts' AS comment
    FROM Dispatcher d
    WHERE d.dispatcher_id IN (
        SELECT co.dispatcher_id
        FROM Contract co
        GROUP BY co.dispatcher_id
        HAVING COUNT(*) = (
            SELECT MAX(contract_count)
            FROM (
                SELECT co.dispatcher_id, COUNT(*) AS contract_count
                FROM Contract co
                GROUP BY co.dispatcher_id
            ) AS contract_table
        )
    )
    UNION
    SELECT d.dispatcher_id, d.d_pib, 'Doesn`t have any signed contracts' AS comment
    FROM Dispatcher d
    WHERE NOT EXISTS (
        SELECT 1
        FROM Contract co
        WHERE co.dispatcher_id = d.dispatcher_id
    )
    UNION
    SELECT d.dispatcher_id, d.d_pib, 'Has ' || COUNT(co.contract_id) || ' signed contracts' AS comment
    FROM Dispatcher d
    LEFT JOIN Contract co ON d.dispatcher_id = co.dispatcher_id
    GROUP BY d.dispatcher_id, d.d_pib
    HAVING COUNT(co.contract_id) > 0 
    AND COUNT(co.contract_id) < (
        SELECT MAX(contract_count)
        FROM (
            SELECT co.dispatcher_id, COUNT(*) AS contract_count
            FROM Contract co
            GROUP BY co.dispatcher_id
        ) AS contract_table
    );
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results
def find_dispatchers_comments(result_textbox):
    results = get_dispatchers_comments()
    result_textbox.delete("1.0", "end")
    if results:
        for dispatcher_id, d_pib, comment in results:
            result_textbox.insert("end", f"\nDispatcher PIB: {d_pib}\nComment: {comment}\n"
                                         f"---------------------------------\n")
    else:
        result_textbox.insert("1.0", "No data available")