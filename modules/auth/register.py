import re
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton
from database.database_setup import cursor, conn
from classes.Users import Dispatcher, Client

from ui.style import entry_style, btn_style_user, label_style

VERIFICATION_CODE = "SECRET2024"

def show_verification_code_dialog(pib_entry, ph_entry, email_entry, password_entry, user_type_combo):
    dialog = CTk()
    dialog.title("Verification code")

    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()

    app_width = 300
    app_height = 200

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    dialog.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    dialog.resizable(0, 0)

    CTkLabel(dialog, text="Enter verification code"
                          "\nAsk your admin for code:").pack(pady=(20, 10))

    verification_code_entry = CTkEntry(dialog, **entry_style, width=200)
    verification_code_entry.pack(pady=(0, 10))

    def on_submit():
        verification_code = verification_code_entry.get()
        if verification_code == VERIFICATION_CODE:
            register_main(pib_entry, ph_entry, email_entry, password_entry, user_type_combo, verification_code_entry, dialog)
        else:
            CTkMessagebox(title="Error", message="Invalid verification code!", icon="cancel", option_1="OK")

    submit_button = CTkButton(dialog, text="Submit", **btn_style_user, command=on_submit)
    submit_button.pack(pady=(10, 20))

    dialog.mainloop()

def register_main(pib_entry, ph_entry, email_entry, password_entry, user_type_combo, verification_code_entry=None, dialog=None):
    user_type = user_type_combo.get()
    if user_type == "Dispatcher":
        if verification_code_entry:
            d_pib = pib_entry.get()
            d_email = email_entry.get()
            d_password = password_entry.get()
            d_phone_number = ph_entry.get()
            verification_code = verification_code_entry.get()

            if verification_code != VERIFICATION_CODE:
                CTkMessagebox(title="Error", message="Invalid verification code!", icon="cancel", option_1="OK")
                return

            if not re.match(r"[^@]+@[^@]+\.[^@]+", d_email):
                CTkMessagebox(title="Error", message="Invalid email format!", icon="cancel", option_1="OK")
                return

            if len(d_password) < 8:
                CTkMessagebox(title="Error", message="Password should contain at least 8 characters!", icon="cancel", option_1="OK")
                return

            if len(d_phone_number) < 10 or not d_phone_number.isdigit():
                CTkMessagebox(title="Error", message="Phone number should contain at least 10 digits!", icon="cancel", option_1="OK")
                return

            cursor.execute("SELECT * FROM Dispatcher WHERE d_email = ? OR d_phone_number = ?", (d_email, d_phone_number))
            existing_dispatcher = cursor.fetchone()
            if existing_dispatcher:
                CTkMessagebox(title="Error", message="User with this email or phone number already exists!", icon="cancel", option_1="OK")
            else:
                dispatcher = Dispatcher(d_pib, d_email, d_password, d_phone_number)
                cursor.execute("INSERT INTO Dispatcher (d_pib, d_email, d_password, d_phone_number) VALUES (?, ?, ?, ?)",
                               (dispatcher.get_d_pib(), dispatcher.get_d_email(), dispatcher.get_d_password(),
                                dispatcher.get_d_phone_number()))
                conn.commit()

                CTkMessagebox(title="Success", message="Registration successful!", icon="check", option_1="Thanks")
                dialog.destroy()
                open_dispatcher_window()
        else:
            show_verification_code_dialog(pib_entry, ph_entry, email_entry, password_entry, user_type_combo)
    elif user_type == "Client":
        CTkMessagebox(title="Error", message="Only dispatcher can register a client!", icon="cancel", option_1="OK")

def register_client(cursor, name_entry, email_entry, password_entry, phone_entry):
    c_pib = name_entry.get()
    c_email = email_entry.get()
    c_password = password_entry.get()
    c_phone_number = phone_entry.get()

    if not re.match(r"[^@]+@[^@]+\.[^@]+", c_email):
        CTkMessagebox(message="Invalid email format!",
                      icon="cancel",
                      option_1="OK")
        return

    if len(c_password) < 8:
        CTkMessagebox(message="Password should contain at least 8 characters!",
                      icon="cancel",
                      option_1="OK")
        return

    if len(c_phone_number) < 10 or not c_phone_number.isdigit():
        CTkMessagebox(message="Phone number should contain at least 10 digits!",
                      icon="cancel",
                      option_1="OK")
        return

    cursor.execute("SELECT * FROM Client WHERE c_email = ? OR c_phone_number = ?", (c_email, c_phone_number))
    existing_client = cursor.fetchone()
    if existing_client:
        CTkMessagebox(message="User with this email or phone number already exists!",
                      icon="cancel",
                      option_1="OK")
        return

    client = Client(c_pib, c_email, c_password, c_phone_number)
    cursor.execute("INSERT INTO Client (c_pib, c_email, c_password, c_phone_number) VALUES (?, ?, ?, ?)",
                   (client.get_c_pib(), client.get_c_email(), client.get_c_password(), client.get_с_phone_num()))

    CTkMessagebox(message="Registration successful!",
                  icon="check",
                  option_1="Thanks")
    conn.commit()
