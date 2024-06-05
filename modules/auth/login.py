from CTkMessagebox import CTkMessagebox
from database.database_setup import cursor
from ui.client import client_window
from ui.dispatcher import dispatcher_window

# Import the globals module correctly
import globals


def login(email_entry, password_entry, phone_entry, user_type_combo):
    # Access the globals module's attributes correctly
    user_type = user_type_combo.get()
    email = email_entry.get()
    password = password_entry.get()
    phone_number = phone_entry.get()

    if user_type == "Dispatcher":
        cursor.execute("SELECT * FROM Dispatcher WHERE d_email=?", (email,))
        user = cursor.fetchone()
        if user and password == user[3]:
            dispatcher_id = user[0]
            d_pib = user[1]
            globals.logged_in_dispatcher_id = dispatcher_id
            globals.logged_in_d_pib = d_pib
            CTkMessagebox(message="Dispatcher login successful", icon="check", option_1="Thanks")
            dispatcher_window(user, dispatcher_id)
        else:
            CTkMessagebox(title="Error", message="Invalid data entered for Dispatcher", icon="cancel")
    elif user_type == "Client":
        cursor.execute("SELECT * FROM Client WHERE c_email=?", (email,))
        user = cursor.fetchone()
        if user and password == user[4]:
            CTkMessagebox(message="Client login successful", icon="check", option_1="Thanks")
            client_window(user)
        else:
            CTkMessagebox(title="Error", message="Invalid data entered for Client", icon="cancel")
