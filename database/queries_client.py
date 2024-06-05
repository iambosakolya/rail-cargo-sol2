import sqlite3
from datetime import datetime
import customtkinter as ctk
from database.database_setup import cursor, conn
from customtkinter import *
from CTkMessagebox import CTkMessagebox

def format_output(data, headers):
    formatted = "\n".join([f"{header}: {value}" for header, value in zip(headers, data)])
    return formatted + "\n\n"

def get_user_contracts(user_id, result_textbox):
    try:
        query = """
            SELECT * FROM Contract
            WHERE client_id = ?
        """
        cursor.execute(query, (user_id,))
        contracts = cursor.fetchall()
        if not contracts:
            raise ValueError("No contracts found")
        result_textbox.delete('1.0', 'end')
        headers = [desc[0] for desc in cursor.description]
        for contract in contracts:
            result_textbox.insert('end', format_output(contract, headers))
    except Exception as e:
        CTkMessagebox(message=str(e), icon="cancel", option_1="OK")

def get_user_data(user_id, result_textbox):
    try:
        query = """
            SELECT * FROM Client
            WHERE client_id = ?
        """
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
        if not user_data:
            raise ValueError("User data not found")
        result_textbox.delete('1.0', 'end')
        headers = [desc[0] for desc in cursor.description]
        result_textbox.insert('end', format_output(user_data, headers))
    except Exception as e:
        CTkMessagebox(message=str(e), icon="cancel", option_1="OK")

def get_contracts_above_weight(user_id, result_textbox, weight=5):
    try:
        query = """
            SELECT * FROM Contract
            JOIN Cargo ON Contract.cargo_id = Cargo.cargo_id
            WHERE Contract.client_id = ? AND Cargo.weight > ?
        """
        cursor.execute(query, (user_id, weight))
        contracts = cursor.fetchall()
        if not contracts:
            raise ValueError("No contracts found with weight above 5t")
        result_textbox.delete('1.0', 'end')
        headers = [desc[0] for desc in cursor.description]
        for contract in contracts:
            result_textbox.insert('end', format_output(contract, headers))
    except Exception as e:
        CTkMessagebox(message=str(e), icon="cancel", option_1="OK")

def get_user_payments(user_id, result_textbox):
    try:
        query = """
            SELECT Payment.* FROM Payment
            JOIN Contract ON Payment.payment_id = Contract.payment_id
            WHERE Contract.client_id = ?
        """
        cursor.execute(query, (user_id,))
        payments = cursor.fetchall()
        if not payments:
            raise ValueError("No payments found")
        result_textbox.delete('1.0', 'end')
        headers = [desc[0] for desc in cursor.description]
        for payment in payments:
            result_textbox.insert('end', format_output(payment, headers))
    except Exception as e:
        CTkMessagebox(message=str(e), icon="cancel", option_1="OK")
