import sqlite3
from datetime import datetime, timedelta
from CTkMessagebox import CTkMessagebox


# 1
def get_contracts_last_week_data(user_id):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        one_week_ago = datetime.now() - timedelta(days=7)
        query = """
            SELECT
                Contract.contract_id,
                Contract.conclusion_date,
                Client.c_pib,
                Dispatcher.d_pib,
                CargoType.cargo_name,
                Cargo.quantity,
                Cargo.weight,
                Itinerary.departure_station,
                Itinerary.arrival_station,
                Itinerary.route_length,
                Itinerary.duration,
                Payment.payment_amount,
                Payment.payment_datetime
            FROM Contract
            JOIN Client ON Contract.client_id = Client.client_id
            JOIN Dispatcher ON Contract.dispatcher_id = Dispatcher.dispatcher_id
            JOIN Cargo ON Contract.cargo_id = Cargo.cargo_id
            JOIN CargoType ON Cargo.cargo_type_id = CargoType.cargo_type_id
            JOIN Itinerary ON Contract.itinerary_id = Itinerary.itinerary_id
            JOIN Payment ON Contract.payment_id = Payment.payment_id
            WHERE Contract.client_id = ? AND Contract.conclusion_date >= ?
        """
        cursor.execute(query, (user_id, one_week_ago.strftime('%Y-%m-%d')))
        contracts = cursor.fetchall()
        conn.close()
        return contracts
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []


def display_contracts_last_week(user_id, result_textbox):
    try:
        contracts = get_contracts_last_week_data(user_id)
        if not contracts:
            raise ValueError("No contracts found in the last week")
        result_textbox.delete('1.0', 'end')
        for contract in contracts:
            contract_data = {
                "contract_id": contract[0],
                "conclusion_date": contract[1],
                "client_info": f"PIB: {contract[2]}",
                "dispatcher_info": f"PIB: {contract[3]}",
                "cargo_info": f"Type: {contract[4]}, Quantity: {contract[5]}, "
                              f" Weight: {contract[6]}",
                "itinerary_info": f"Departure: {contract[7]}, Arrival: {contract[8]},"
                                  f"Route Length: {contract[9]}, Duration: {contract[10]}",
                "payment_info": f"Amount: {contract[11]}, Date/Time: {contract[12]}"
            }
            formatted_output = (
                f"Contract ID: {contract_data['contract_id']}\n"
                f"Conclusion Date: {contract_data['conclusion_date']}\n\n"
                f"\tClient Information: \n{contract_data['client_info']}\n\n"
                f"\tDispatcher Information: \n{contract_data['dispatcher_info']}\n\n"
                f"\tCargo Information: \n{contract_data['cargo_info']}\n\n"
                f"\tItinerary Information: \n{contract_data['itinerary_info']}\n\n"
                f"\tPayment Information: \n{contract_data['payment_info']}\n"
                "\n---------------------------------\n"
            )
            result_textbox.insert('end', formatted_output)
    except ValueError as ve:
        CTkMessagebox(message=str(ve),
                      icon="cancel",
                      option_1="OK")
    except Exception as e:
        CTkMessagebox(message=f"An error occurred: {e}",
                      icon="cancel",
                      option_1="OK")


# 2
def get_user_data(user_id, result_textbox):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = """
            SELECT c_pib, c_phone_number, c_email
            FROM Client
            WHERE client_id = ?
        """
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        result_textbox.delete('1.0', 'end')
        if user_data:
            formatted_output = (
                f"Client Information:\n"
                f"PIB: {user_data[0]}\n"
                f"Phone Number: {user_data[1]}\n"
                f"Email: {user_data[2]}\n"
            )
            result_textbox.insert('end', formatted_output)
        else:
            result_textbox.insert('end', "No user data found.\n")
    except sqlite3.Error as e:
        CTkMessagebox(message=f"SQLite error: {e}",
                      icon="cancel",
                      option_1="OK")
    except Exception as e:
        CTkMessagebox(message=f"An error occurred: {e}",
                      icon="cancel",
                      option_1="OK")


# 3
def get_contracts_above_weight(user_id, result_textbox, weight):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = """
            SELECT
                Contract.conclusion_date,
                CargoType.cargo_name,
                Cargo.quantity,
                Cargo.weight
            FROM Contract
            JOIN Cargo ON Contract.cargo_id = Cargo.cargo_id
            JOIN CargoType ON Cargo.cargo_type_id = CargoType.cargo_type_id
            WHERE Contract.client_id = ? AND Cargo.weight > ?
        """
        cursor.execute(query, (user_id, weight))
        contracts = cursor.fetchall()
        conn.close()

        result_textbox.delete('1.0', 'end')
        if contracts:
            for contract in contracts:
                formatted_output = (
                    f"Conclusion Date: {contract[0]}\n"
                    f"Cargo Type: {contract[1]}\n"
                    f"Quantity: {contract[2]}\n"
                    f"Weight: {contract[3]}\n"
                    "\n---------------------------------\n"
                )
                result_textbox.insert('end', formatted_output)
        else:
            result_textbox.insert('end', "No contracts found with weight greater than specified.\n")
    except sqlite3.Error as e:
        CTkMessagebox(message=f"SQLite error: {e}",
                      icon="cancel",
                      option_1="OK")
    except Exception as e:
        CTkMessagebox(message=f"An error occurred: {e}",
                      icon="cancel",
                      option_1="OK")


# 4
def get_user_payments(user_id, result_textbox):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = """
            SELECT
                Payment.payment_amount,
                Payment.payment_datetime
            FROM Payment
            JOIN Contract ON Payment.payment_id = Contract.payment_id
            WHERE Contract.client_id = ?
        """
        cursor.execute(query, (user_id,))
        payments = cursor.fetchall()
        conn.close()

        result_textbox.delete('1.0', 'end')
        if payments:
            for payment in payments:
                formatted_output = (
                    f"Payment Amount: {payment[0]}\n"
                    f"Payment Date/Time: {payment[1]}\n"
                    "\n---------------------------------\n"
                )
                result_textbox.insert('end', formatted_output)
        else:
            result_textbox.insert('end', "No payments found.\n")
    except sqlite3.Error as e:
        CTkMessagebox(message=f"SQLite error: {e}",
                      icon="cancel",
                      option_1="OK")
    except Exception as e:
        CTkMessagebox(message=f"An error occurred: {e}",
                      icon="cancel",
                      option_1="OK")
