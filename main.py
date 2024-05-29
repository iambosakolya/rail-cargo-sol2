import re
import PIL
from PIL import Image

import customtkinter
from customtkinter import *
from CTkMessagebox import CTkMessagebox

import database
from database import cursor, conn

from client import client_window
from dispatcher import dispatcher_window

from classes.Users import Dispatcher, Client

label_style = {
    "text_color": "#601E88",
    "anchor": "w",
    "justify": "left",
    "font": ("Arial Rounded MT Bold", 15)}
btn_style = {
    "fg_color": "#601E88",
    "hover_color": "#E44982",
    "text_color": "#ffffff",
    "font": ("Arial Rounded MT Bold", 17)}
entry_style = {
    "fg_color": "#EEEEEE",
    "border_color": "#601E88",
    "border_width": 1,
    "text_color": "#000000"}

def register():
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
        #     CTkMessagebox(message="Invalid email format!", icon="cancel", option_1="OK")
        #     return
        #
        # if len(c_password) < 8:
        #     CTkMessagebox(message="Password should contain at least 8 characters!", icon="cancel", option_1="OK")
        #     return
        #
        # if len(c_phone_number) < 10 or not c_phone_number.isdigit():
        #     CTkMessagebox(message="Phone number should contain at least 10 digits!", icon="cancel", option_1="OK")
        #     return
        #
        # cursor.execute("SELECT * FROM Client WHERE c_email = ? OR c_phone_number = ?", (c_email, c_phone_number))
        # existing_client = cursor.fetchone()
        # if existing_client:
        #     CTkMessagebox(message="User with this email or phone number already exists!", icon="cancel", option_1="OK")
        # else:
        #     client = Client(c_pib, c_email, c_password, c_phone_number)
        #     cursor.execute("INSERT INTO Client (c_pib, c_email, c_password, c_phone_number) VALUES (?, ?, ?, ?)",
        #                    (client.get_c_pib(),
        #                     client.get_c_email(),
        #                     client.get_c_password(),
        #                     client.get_с_phone_num()))
        #     CTkMessagebox(message="Registration successful!", icon="check", option_1="Thanks")
    conn.commit()

def login():
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

app = CTk()
app.title("Rail cargo solutions")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

app_width = 750
app_height = 650

x_position = (screen_width - app_width) // 2
y_position = (screen_height - app_height) // 2
app.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
app.resizable(0, 0)

side_img_data = Image.open("images/side-img.png")
email_icon_data = Image.open("images/email-icon.png")
password_icon_data = Image.open("images/password-icon.png")
pib_icon_data = Image.open("images/pib-icon.png")
phone_icon_data = Image.open("images/phone-icon.png")


side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(350, 650))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(25, 25))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(25, 25))
pib_icon = CTkImage(dark_image=pib_icon_data, light_image=pib_icon_data, size=(25, 25))
phone_icon = CTkImage(dark_image=phone_icon_data, light_image=phone_icon_data, size=(25, 25))


frame = CTkFrame(master=app, width=350, height=650, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="left")

CTkLabel(master=frame, text="", image=side_img).pack(expand=True, side="left")

frame_right = CTkFrame(master=app, width=450, height=650, fg_color="#ffffff")
frame_right.pack_propagate(0)
frame_right.pack(expand=True, side="right")


CTkLabel(master=frame_right, text="Welcome back!",text_color="#601E88",anchor="w",
         justify="left", font=("Arial Rounded MT Bold", 32)).pack(anchor="w", pady=(50, 5), padx=(50, 0))


CTkLabel(master=frame_right, text="Sign in to your account", text_color="#7E7E7E", anchor="w",
         justify="left", font=("Arial Rounded MT Bold", 16)).pack(anchor="w", padx=(50, 0))


user_type = CTkLabel(master=frame_right, text="User type:", **label_style)
user_type.pack(anchor="w", pady=(20, 0), padx=(50, 0))


user_type_combo = CTkComboBox(master=frame_right, values=["Dispatcher", "Client"],
                                  font=("Arial Rounded MT Bold", 14))
user_type_combo.pack(anchor="w", pady=(10, 0), padx=(60, 0))


name_label = CTkLabel(master=frame_right, text="PIB:", **label_style,
                          image=pib_icon, compound="left")
name_label.pack(anchor="w", pady=(18, 0), padx=(50, 0))


name_entry = CTkEntry(master=frame_right, width=300, **entry_style)
name_entry.pack(anchor="w", padx=(50, 0))


phone_label = CTkLabel(master=frame_right, text="Phone number(+38):", **label_style,
                           image=phone_icon, compound="left")
phone_label.pack(anchor="w", pady=(18, 0), padx=(50, 0))


phone_entry = CTkEntry(master=frame_right, width=300, **entry_style)
phone_entry.pack(anchor="w", padx=(50, 0))


CTkLabel(master=frame_right, text="Email:",  **label_style,
             image=email_icon, compound="left").pack(anchor="w", pady=(18, 0), padx=(50, 0))

email_entry = CTkEntry(master=frame_right, width=300, **entry_style)
email_entry.pack(anchor="w", padx=(50, 0))


CTkLabel(master=frame_right, text="Password:",  **label_style,
             image=password_icon, compound="left").pack(anchor="w", pady=(15, 0), padx=(50, 0))

password_entry = CTkEntry(master=frame_right,
                          **entry_style, width=300, show="*")
password_entry.pack(anchor="w", padx=(50, 0))


register_button = CTkButton(master=frame_right, text="Register", **btn_style,
                            width=300, command=register)
register_button.pack(anchor="w", pady=(40, 0), padx=(50, 0))


CTkButton(master=frame_right, text="Log in",  **btn_style,
          width=300, command=login).pack(anchor="w", pady=(10, 0), padx=(50, 0))

app.mainloop()
