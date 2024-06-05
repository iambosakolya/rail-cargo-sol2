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

# def delete_d_data(d_pib):
#     cursor.execute("SELECT * FROM Dispatcher "
#                    "WHERE d_pib = ?",
#                    (d_pib,))
#     result = cursor.fetchone()
#
#     if result:
#         cursor.execute("DELETE FROM Dispatcher "
#                        "WHERE d_pib = ?",
#                        (d_pib,))
#         conn.commit()
#         CTkMessagebox(message=f"Dispatcher with surname '{d_pib}' deleted successfully",
#                       icon="check",
#                       option_1="Thanks")
#     else:
#         CTkMessagebox(message=f"No dispatcher found with surname '{d_pib}'",
#                       icon="cancel",
#                       option_1="OK")
#
# def delete_dispatcher():
#     def on_confirm():
#         d_pib = entry_d.get()
#         delete_d_data(d_pib)
#         dialog.destroy()
#
#     dialog = ctk.CTk()
#     dialog.title("Delete Dispatcher")
#
#     screen_width = dialog.winfo_screenwidth()
#     screen_height = dialog.winfo_screenheight()
#
#     dialog_width = 350
#     dialog_height = 150
#
#     x_position = (screen_width - dialog_width) // 2
#     y_position = (screen_height - dialog_height) // 2
#
#     dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
#     dialog.resizable(0, 0)
#
#     screen_frame = CTkFrame(master=dialog, width=350, height=200, fg_color="#897E9B")
#     screen_frame.pack_propagate(0)
#     screen_frame.pack(expand=True, fill="both")
#
#     label_d = ctk.CTkLabel(screen_frame, text="Dispatcher pib to delete:", **label_style)
#     label_d.pack(pady=10)
#
#     entry_d = ctk.CTkEntry(screen_frame)
#     entry_d.pack(pady=10)
#
#     confirm_d = ctk.CTkButton(screen_frame, text="Confirm", fg_color="#000000",
#                               hover_color="#4F2346",
#                               text_color="#ffffff", command=on_confirm)
#     confirm_d.pack(pady=10)
#
#     dialog.mainloop()

def delete_dispatcher(dispatcher_id):
    cursor.execute("SELECT d_pib FROM Dispatcher WHERE dispatcher_id = ?", (dispatcher_id,))
    result = cursor.fetchone()

    if result:
        dispatcher_pib = result[0]

        cursor.execute("SELECT contract_id, payment_id, itinerary_id, cargo_id "
                       "FROM Contract WHERE dispatcher_id = ?", (dispatcher_id,))
        contracts = cursor.fetchall()

        for contract in contracts:
            contract_id, payment_id, itinerary_id, cargo_id = contract

            cursor.execute("SELECT COUNT(*) FROM Contract WHERE payment_id = ?", (payment_id,))
            payment_count = cursor.fetchone()[0]
            if payment_count == 1:
                cursor.execute("DELETE FROM Payment WHERE payment_id = ?", (payment_id,))

            cursor.execute("SELECT COUNT(*) FROM Contract WHERE itinerary_id = ?", (itinerary_id,))
            itinerary_count = cursor.fetchone()[0]
            if itinerary_count == 1:
                cursor.execute("DELETE FROM Itinerary WHERE itinerary_id = ?", (itinerary_id,))

            cursor.execute("SELECT COUNT(*) FROM Contract WHERE cargo_id = ?", (cargo_id,))
            cargo_count = cursor.fetchone()[0]
            if cargo_count == 1:
                # Знайти тип вантажу
                cursor.execute("SELECT cargo_type_id FROM Cargo WHERE cargo_id = ?", (cargo_id,))
                cargo_type = cursor.fetchone()
                if cargo_type:
                    cargo_type_id = cargo_type[0]

                    cursor.execute("DELETE FROM Cargo WHERE cargo_id = ?", (cargo_id,))

                    cursor.execute("SELECT COUNT(*) FROM Cargo WHERE cargo_type_id = ?", (cargo_type_id,))
                    cargo_type_count = cursor.fetchone()[0]
                    if cargo_type_count == 0:
                        cursor.execute("DELETE FROM CargoType WHERE cargo_type_id = ?", (cargo_type_id,))

        cursor.execute("DELETE FROM Contract WHERE dispatcher_id = ?", (dispatcher_id,))

        cursor.execute("DELETE FROM Dispatcher WHERE dispatcher_id = ?", (dispatcher_id,))
        conn.commit()

        CTkMessagebox(message=f"Dispatcher '{dispatcher_pib}' and related data deleted successfully",
                      icon="check",
                      option_1="Thanks")
    else:
        CTkMessagebox(message=f"No dispatcher found with ID '{dispatcher_id}'",
                      icon="cancel",
                      option_1="OK")

def confirm_delete_d(dispatcher_id):
    confirm_window = ctk.CTkToplevel()
    confirm_window.title("Confirm delete")

    screen_width = confirm_window.winfo_screenwidth()
    screen_height = confirm_window.winfo_screenheight()

    app_width = 350
    app_height = 200

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_width) // 2

    confirm_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    confirm_window.resizable(0, 0)

    label = ctk.CTkLabel(confirm_window, text="Are you sure? It will delete your account permanently")
    label.pack(padx=20, pady=20)

    button_frame = ctk.CTkFrame(confirm_window)
    button_frame.pack(pady=10)

    def on_confirm():
        delete_dispatcher(dispatcher_id)
        confirm_window.destroy()

    def on_cancel():
        confirm_window.destroy()

    yes_button = ctk.CTkButton(button_frame, text="Yes", **btn_style,
                               command=on_confirm)
    yes_button.grid(row=0, column=0, padx=10)

    no_button = ctk.CTkButton(button_frame, text="No",  **btn_style,
                              command=on_cancel)
    no_button.grid(row=0, column=1, padx=10)


#client delete from the side of a dispatcher
def delete_c_data(client_id):
    cursor.execute("SELECT contract_id, payment_id, itinerary_id, cargo_id FROM Contract WHERE client_id = ?", (client_id,))
    contracts = cursor.fetchall()

    for contract in contracts:
        contract_id, payment_id, itinerary_id, cargo_id = contract

        cursor.execute("SELECT COUNT(*) FROM Contract WHERE payment_id = ?", (payment_id,))
        payment_count = cursor.fetchone()[0]
        if payment_count == 1:
            cursor.execute("DELETE FROM Payment WHERE payment_id = ?", (payment_id,))

        cursor.execute("SELECT COUNT(*) FROM Contract WHERE itinerary_id = ?", (itinerary_id,))
        itinerary_count = cursor.fetchone()[0]
        if itinerary_count == 1:
            cursor.execute("DELETE FROM Itinerary WHERE itinerary_id = ?", (itinerary_id,))

        cursor.execute("SELECT COUNT(*) FROM Contract WHERE cargo_id = ?", (cargo_id,))
        cargo_count = cursor.fetchone()[0]
        if cargo_count == 1:
            cursor.execute("SELECT cargo_type_id FROM Cargo WHERE cargo_id = ?", (cargo_id,))
            cargo_type = cursor.fetchone()
            if cargo_type:
                cargo_type_id = cargo_type[0]

                cursor.execute("DELETE FROM Cargo WHERE cargo_id = ?", (cargo_id,))

                cursor.execute("SELECT COUNT(*) FROM Cargo WHERE cargo_type_id = ?", (cargo_type_id,))
                cargo_type_count = cursor.fetchone()[0]
                if cargo_type_count == 0:
                    cursor.execute("DELETE FROM CargoType WHERE cargo_type_id = ?", (cargo_type_id,))

    cursor.execute("DELETE FROM Contract WHERE client_id = ?", (client_id,))

    cursor.execute("DELETE FROM Client WHERE client_id = ?", (client_id,))
    conn.commit()

# Функція для видалення клієнта через інтерфейс
def delete_client():
    def on_confirm():
        selected_client = option_menu.get()
        client_id = client_dict[selected_client]
        delete_c_data(client_id)
        dialog1.destroy()

    dialog1 = ctk.CTk()
    dialog1.title("Delete client")

    screen_width = dialog1.winfo_screenwidth()
    screen_height = dialog1.winfo_screenheight()

    dialog_width = 350
    dialog_height = 150

    x_position = (screen_width - dialog_width) // 2
    y_position = (screen_height - dialog_height) // 2

    dialog1.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    dialog1.resizable(0, 0)

    screen_frame = ctk.CTkFrame(master=dialog1, width=dialog_width, height=dialog_height, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    label_c = ctk.CTkLabel(screen_frame, text="Select client to delete:", **label_style)
    label_c.pack(pady=10)

    cursor.execute("SELECT client_id, c_pib, c_phone_number FROM Client")
    clients = cursor.fetchall()
    client_dict = {f"{client[1]} \n(Phone: {client[2]})": client[0] for client in clients}

    option_menu = ctk.CTkOptionMenu(screen_frame, values=list(client_dict.keys()), text_color="#000000",
                                    fg_color="#D3D3D3")
    option_menu.pack(pady=10)

    confirm_c = ctk.CTkButton(screen_frame, text="Confirm", **btn_style, command=on_confirm)
    confirm_c.pack(pady=10)

    dialog1.mainloop()


# from the side of a client
def delete_client_me(client_id):
    cursor.execute("SELECT c_pib FROM Client WHERE client_id = ?", (client_id,))
    result = cursor.fetchone()

    if result:
        client_pib = result[0]

        cursor.execute("SELECT contract_id, payment_id, itinerary_id, cargo_id "
                       "FROM Contract WHERE client_id = ?", (client_id,))
        contracts = cursor.fetchall()

        for contract in contracts:
            contract_id, payment_id, itinerary_id, cargo_id = contract

            cursor.execute("SELECT COUNT(*) FROM Contract WHERE payment_id = ?", (payment_id,))
            payment_count = cursor.fetchone()[0]
            if payment_count == 1:
                cursor.execute("DELETE FROM Payment WHERE payment_id = ?", (payment_id,))

            cursor.execute("SELECT COUNT(*) FROM Contract WHERE itinerary_id = ?", (itinerary_id,))
            itinerary_count = cursor.fetchone()[0]
            if itinerary_count == 1:
                cursor.execute("DELETE FROM Itinerary WHERE itinerary_id = ?", (itinerary_id,))

            cursor.execute("SELECT COUNT(*) FROM Contract WHERE cargo_id = ?", (cargo_id,))
            cargo_count = cursor.fetchone()[0]
            if cargo_count == 1:

                cursor.execute("SELECT cargo_type_id FROM Cargo WHERE cargo_id = ?", (cargo_id,))
                cargo_type = cursor.fetchone()
                if cargo_type:
                    cargo_type_id = cargo_type[0]

                    cursor.execute("DELETE FROM Cargo WHERE cargo_id = ?", (cargo_id,))

                    cursor.execute("SELECT COUNT(*) FROM Cargo WHERE cargo_type_id = ?", (cargo_type_id,))
                    cargo_type_count = cursor.fetchone()[0]
                    if cargo_type_count == 0:
                        cursor.execute("DELETE FROM CargoType WHERE cargo_type_id = ?", (cargo_type_id,))

        cursor.execute("DELETE FROM Contract WHERE client_id = ?", (client_id,))

        cursor.execute("DELETE FROM Client WHERE client_id = ?", (client_id,))
        conn.commit()

        CTkMessagebox(message=f"Client '{client_pib}' and related data deleted successfully",
                      icon="check",
                      option_1="Thanks")
    else:
        CTkMessagebox(message=f"No client found with ID '{client_id}'",
                      icon="cancel",
                      option_1="OK")
def confirm_delete_c(client_id):
    confirm_window = ctk.CTkToplevel()
    confirm_window.title("Confirm Delete")

    screen_width = confirm_window.winfo_screenwidth()
    screen_height = confirm_window.winfo_screenheight()

    app_width = 350
    app_height = 200

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    confirm_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    confirm_window.resizable(0, 0)

    label = ctk.CTkLabel(confirm_window, text="Are you sure? It will delete the client account permanently.")
    label.pack(padx=20, pady=20)

    button_frame = ctk.CTkFrame(confirm_window)
    button_frame.pack(pady=10)

    def on_confirm():
        delete_client_me(client_id)
        confirm_window.destroy()

    def on_cancel():
        confirm_window.destroy()

    yes_button = ctk.CTkButton(button_frame, text="Yes", command=on_confirm)
    yes_button.grid(row=0, column=0, padx=10)

    no_button = ctk.CTkButton(button_frame, text="No", command=on_cancel)
    no_button.grid(row=0, column=1, padx=10)


