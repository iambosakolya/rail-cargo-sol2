import re
from CTkMessagebox import CTkMessagebox
from database.database_setup import cursor, conn
from classes.Users import Dispatcher
from ui.client import client_window
from ui.dispatcher import dispatcher_window


def register(name_entry, phone_entry, email_entry,
             password_entry, user_type_combo):
    user_type = user_type_combo.get()
    if user_type == "Dispatcher":
        d_pib = name_entry.get()
        d_email = email_entry.get()
        d_password = password_entry.get()
        d_phone_number = phone_entry.get()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", d_email):
            CTkMessagebox(message="Invalid email format!",
                          icon="cancel",
                          option_1="OK")
            return

        if len(d_password) < 8:
            CTkMessagebox(message="Password should contain at least 8 characters!",
                          icon="cancel",
                          option_1="OK")
            return

        if len(d_phone_number) < 10 or not d_phone_number.isdigit():
            CTkMessagebox(message="Phone number should contain at least 10 digits!",
                          icon="cancel",
                          option_1="OK")
            return

        cursor.execute("SELECT * FROM Dispatcher "
                       "WHERE d_email = ? OR d_phone_number = ?",
                       (d_email, d_phone_number))
        existing_dispatcher = cursor.fetchone()
        if existing_dispatcher:
            CTkMessagebox(message="User with this email or phone number already exists!",
                          icon="cancel",
                          option_1="OK")
        else:
            dispatcher = Dispatcher(d_pib, d_email, d_password, d_phone_number)
            cursor.execute("INSERT INTO Dispatcher (d_pib, d_email, d_password, d_phone_number)"
                           " VALUES (?, ?, ?, ?)",
                           (dispatcher.get_d_pib(),
                            dispatcher.get_d_email(),
                            dispatcher.get_d_password(),
                            dispatcher.get_d_phone_number()))
            CTkMessagebox(message="Registration successful!",
                          icon="check",
                          option_1="Thanks")

    elif user_type == "Client":
        CTkMessagebox(message="Only dispatcher can register a client!",
                      icon="cancel",
                      option_1="OK")
        # c_pib = name_entry.get()
        # c_email = email_entry.get()
        # c_password = password_entry.get()
        # c_phone_number = phone_entry.get()
        #
        # if not re.match(r"[^@]+@[^@]+\.[^@]+", c_email):
        #     CTkMessagebox(message="Invalid email format!",
        #     icon="cancel",
        #     option_1="OK")
        #     return
        #
        # if len(c_password) < 8:
        #     CTkMessagebox(message="Password should contain at least 8 characters!",
        #     icon="cancel",
        #     option_1="OK")
        #     return
        #
        # if len(c_phone_number) < 10 or not c_phone_number.isdigit():
        #     CTkMessagebox(message="Phone number should contain at least 10 digits!",
        #     icon="cancel",
        #     option_1="OK")
        #     return
        #
        # cursor.execute("SELECT * FROM Client
        # WHERE c_email = ? OR c_phone_number = ?", (c_email, c_phone_number))
        # existing_client = cursor.fetchone()
        # if existing_client:
        #     CTkMessagebox(message="User with this email or phone number already exists!",
        #     icon="cancel",
        #     option_1="OK")
        # else:
        #     client = Client(c_pib, c_email, c_password, c_phone_number)
        #     cursor.execute("INSERT INTO Client (c_pib, c_email, c_password, c_phone_number) VALUES (?, ?, ?, ?)",
        #                    (client.get_c_pib(),
        #                     client.get_c_email(),
        #                     client.get_c_password(),
        #                     client.get_с_phone_num()))
        #     CTkMessagebox(message="Registration successful!",
        #     icon="check",
        #     option_1="Thanks")
    conn.commit()


def login(email_entry, password_entry,
          phone_entry, user_type_combo):
    user_type = user_type_combo.get()
    email = email_entry.get()
    password = password_entry.get()
    phone_number = phone_entry.get()

    if user_type == "Dispatcher":
        cursor.execute("SELECT * FROM Dispatcher "
                       "WHERE d_email=?", (email,))
        user = cursor.fetchone()
        if user and password == user[3]:
            CTkMessagebox(message="Dispatcher login successful",
                          icon="check",
                          option_1="Thanks")
            dispatcher_window()
        else:
            CTkMessagebox(title="Error",
                          message="Invalid data entered for Dispatcher",
                          icon="cancel")
    elif user_type == "Client":
        cursor.execute("SELECT * FROM Client WHERE c_email=?", (email,))
        user = cursor.fetchone()
        if user and password == user[4]:
            CTkMessagebox(message="Client login successful",
                          icon="check",
                          option_1="Thanks")
            client_window()
        else:
            CTkMessagebox(title="Error",
                          message="Invalid data entered for Client",
                          icon="cancel")
