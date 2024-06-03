import sqlite3
import win32print
import win32ui
import win32con
from CTkMessagebox import CTkMessagebox

from classes.RailCargoSol import RailCargoSol


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
