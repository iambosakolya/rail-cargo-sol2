import sqlite3
import win32print
import win32ui
import win32con
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk

from classes.RailCargoSol import RailCargoSol
from ui.style import label_style, btn_style_user, entry_style


def get_contract_data(cursor, contract_id):
    try:
        cursor.execute("SELECT * FROM Contract "
                       "WHERE contract_id = ?", (contract_id,))
        contract_data = cursor.fetchone()
        if not contract_data:
            return None, None, None, None, None, None, None

        cursor.execute("SELECT * FROM Client "
                       "WHERE client_id = ?", (contract_data[2],))
        client_data = cursor.fetchone()
        if not client_data:
            return contract_data, None, None, None, None, None, None

        cursor.execute("SELECT * FROM Payment "
                       "WHERE payment_id = ?", (contract_data[5],))
        payment_data = cursor.fetchone()
        if not payment_data:
            return contract_data, client_data, None, None, None, None, None

        cursor.execute("SELECT * FROM Dispatcher "
                       "WHERE dispatcher_id = ?", (contract_data[3],))
        dispatcher_data = cursor.fetchone()
        if not dispatcher_data:
            return contract_data, client_data, payment_data, None, None, None, None

        cursor.execute("SELECT * FROM Cargo "
                       "WHERE cargo_id = ?", (contract_data[4],))
        cargo_data = cursor.fetchone()
        if not cargo_data:
            return (contract_data, client_data, payment_data,
                    dispatcher_data, None, None, None)

        cursor.execute("SELECT * FROM CargoType "
                       "WHERE cargo_type_id = ?", (cargo_data[1],))
        cargo_type_data = cursor.fetchone()
        if not cargo_type_data:
            return (contract_data, client_data, payment_data,
                    dispatcher_data, cargo_data, None, None)

        cursor.execute("SELECT * FROM Itinerary "
                       "WHERE itinerary_id = ?", (contract_data[6],))
        itinerary_data = cursor.fetchone()
        if not itinerary_data:
            return (contract_data, client_data, payment_data,
                    dispatcher_data, cargo_data, cargo_type_data, None)

        return (contract_data, client_data, payment_data,
                dispatcher_data, cargo_data, cargo_type_data, itinerary_data)
    except sqlite3.Error as e:
        print(f"Error fetching contract data: {e}")
        return None, None, None, None, None, None, None


def select_contract_print(client_id):
    def print_selected_contract():
        selected_contract_id = contract_var.get()
        if selected_contract_id:
            print_client_contract(selected_contract_id)
        else:
            CTkMessagebox(title="Error", message="Please select a contract to print.", icon="warning")

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT contract_id FROM Contract WHERE client_id=?", (client_id,))
    contracts = cursor.fetchall()
    conn.close()

    if not contracts:
        CTkMessagebox(title="No Contracts", message="No contracts found for this client.", icon="info")
        return

    contract_ids = [str(contract[0]) for contract in contracts]

    contract_selection_window = ctk.CTk()
    contract_selection_window.title("Select Contract")

    screen_width = contract_selection_window.winfo_screenwidth()
    screen_height = contract_selection_window.winfo_screenheight()

    app_width = 350
    app_height = 200

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    contract_selection_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    contract_selection_window.resizable(0, 0)

    ctk.CTkLabel(contract_selection_window, text="Select a contract to print:").pack(pady=10)

    contract_var = ctk.StringVar(contract_selection_window)
    contract_var.set(contract_ids[0])

    option_menu = ctk.CTkOptionMenu(contract_selection_window, text_color="#000000",
                                        button_color="#565B5E", fg_color="#D3D3D3",
                                    variable=contract_var, values=contract_ids)
    option_menu.pack(pady=10)

    ctk.CTkButton(contract_selection_window, text="Print contract", **btn_style_user,
                  command=print_selected_contract).pack(pady=10)

    contract_selection_window.mainloop()


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

        rail_cargo_sol = RailCargoSol(city_location=head_office,
                                      company_name=company_name)

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
        hdc.TextOut(1000, -1000, str(rail_cargo_sol))

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


def print_client_contract(contract_id):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        (contract_data, client_data, payment_data, dispatcher_data,
         cargo_data, cargo_type_data, itinerary_data) = get_contract_data(cursor, contract_id)

        if not contract_data:
            CTkMessagebox(message="Failed to fetch contract data", icon="cancel", option_1="OK")
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
            if (" Information:" in line or "Contract ID" in line or "Conclusion Date" in line):
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