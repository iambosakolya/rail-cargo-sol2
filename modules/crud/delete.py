import sqlite3
import database.database_setup

from datetime import datetime
import customtkinter
import customtkinter as ctk
from customtkinter import *
from CTkMessagebox import CTkMessagebox

from database.database_setup import cursor, conn


label_style = {
    "text_color": "#000000",
    "anchor": "w",
    "justify": "center",
    "font": ("Arial Rounded MT Bold", 15)
}
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


def delete_data(contract_id):
    cursor.execute("SELECT cargo_id, payment_id, itinerary_id "
                   "FROM Contract WHERE contract_id = ?",
                   (contract_id,))
    result = cursor.fetchone()

    if result:
        cargo_id, payment_id, itinerary_id = result

        cursor.execute("SELECT cargo_type_id "
                       "FROM Cargo WHERE cargo_id = ?",
                       (cargo_id,))
        cargo_result = cursor.fetchone()

        if cargo_result:
            cargo_type_id = cargo_result[0]

            cursor.execute("DELETE FROM Cargo WHERE cargo_id = ?", (cargo_id,))
            cursor.execute("DELETE FROM CargoType WHERE cargo_type_id = ?", (cargo_type_id,))
            cursor.execute("DELETE FROM Payment WHERE payment_id = ?", (payment_id,))
            cursor.execute("DELETE FROM Itinerary WHERE itinerary_id = ?", (itinerary_id,))
            cursor.execute("DELETE FROM Contracts WHERE contract_id = ?", (contract_id,))

        cursor.execute("DELETE FROM Contract WHERE contract_id = ?", (contract_id,))

        conn.commit()

        CTkMessagebox(message=f"Contract with ID {contract_id} deleted successfully", icon="check", option_1="Thanks")
    else:
        CTkMessagebox(message=f"No contract found with ID {contract_id}", icon="cancel", option_1="OK")


def delete_contract():
    def on_confirm():
        contract_id = entry_d.get()
        delete_data(contract_id)
        dialog.destroy()

    dialog = ctk.CTk()
    dialog.title("Delete contract")

    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()

    dialog_width = 350
    dialog_height = 150

    x_position = (screen_width - dialog_width) // 2
    y_position = (screen_height - dialog_height) // 2

    dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    dialog.resizable(0, 0)

    screen_frame = CTkFrame(master=dialog, width=350, height=200, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    label_d = ctk.CTkLabel(screen_frame, text="Contract ID to delete:", **label_style)
    label_d.pack(pady=10)

    entry_d = ctk.CTkEntry(screen_frame)
    entry_d.pack(pady=10)

    confirm_d = ctk.CTkButton(screen_frame, text="Confirm", fg_color="#000000", hover_color="#4F2346",
                              text_color="#ffffff", command=on_confirm)
    confirm_d.pack(pady=10)

    dialog.mainloop()


def delete_d_data(d_pib):
    cursor.execute("SELECT * FROM Dispatcher "
                   "WHERE d_pib = ?",
                   (d_pib,))
    result = cursor.fetchone()

    if result:
        cursor.execute("DELETE FROM Dispatcher "
                       "WHERE d_pib = ?",
                       (d_pib,))
        conn.commit()
        CTkMessagebox(message=f"Dispatcher with surname '{d_pib}' deleted successfully",
                      icon="check",
                      option_1="Thanks")
    else:
        CTkMessagebox(message=f"No dispatcher found with surname '{d_pib}'",
                      icon="cancel",
                      option_1="OK")

def delete_dispatcher():
    def on_confirm():
        d_pib = entry_d.get()
        delete_d_data(d_pib)
        dialog.destroy()

    dialog = ctk.CTk()
    dialog.title("Delete Dispatcher")

    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()

    dialog_width = 350
    dialog_height = 150

    x_position = (screen_width - dialog_width) // 2
    y_position = (screen_height - dialog_height) // 2

    dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    dialog.resizable(0, 0)

    screen_frame = CTkFrame(master=dialog, width=350, height=200, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    label_d = ctk.CTkLabel(screen_frame, text="Dispatcher pib to delete:", **label_style)
    label_d.pack(pady=10)

    entry_d = ctk.CTkEntry(screen_frame)
    entry_d.pack(pady=10)

    confirm_d = ctk.CTkButton(screen_frame, text="Confirm", fg_color="#000000",
                              hover_color="#4F2346",
                              text_color="#ffffff", command=on_confirm)
    confirm_d.pack(pady=10)

    dialog.mainloop()


def delete_c_data(c_pib):
    cursor.execute("SELECT * FROM Client "
                   "WHERE c_pib = ?",
                   (c_pib,))
    result = cursor.fetchone()

    if result:
        cursor.execute("DELETE FROM Client "
                       "WHERE c_pib = ?",
                       (c_pib,))
        conn.commit()
        CTkMessagebox(message=f"Client with surname '{c_pib}' deleted successfully",
                      icon="check",
                      option_1="Thanks")
    else:
        CTkMessagebox(message=f"No client found with surname '{c_pib}'",
                      icon="cancel", option_1="OK")

def delete_client():
    def on_confirm():
        c_pib = entry_c.get()
        delete_c_data(c_pib)
        dialog1.destroy()

    dialog1 = ctk.CTk()
    dialog1.title("Delete Client")

    screen_width = dialog1.winfo_screenwidth()
    screen_height = dialog1.winfo_screenheight()

    dialog_width = 350
    dialog_height = 150

    x_position = (screen_width - dialog_width) // 2
    y_position = (screen_height - dialog_height) // 2

    dialog1.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    dialog1.resizable(0, 0)

    screen_frame = CTkFrame(master=dialog1, width=dialog_width, height=dialog_height, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    label_c = ctk.CTkLabel(screen_frame, text="Client pib to delete:", **label_style)
    label_c.pack(pady=10)

    entry_c = ctk.CTkEntry(screen_frame)
    entry_c.pack(pady=10)

    confirm_c = ctk.CTkButton(screen_frame, text="Confirm", fg_color="#000000", hover_color="#4F2346",
                              text_color="#ffffff", command=on_confirm)
    confirm_c.pack(pady=10)

    dialog1.mainloop()
