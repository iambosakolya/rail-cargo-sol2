from customtkinter import *
import sqlite3
from tkinter import *
from PIL import Image
from tkinter import messagebox
from classes.Users import Dispatcher, Client
from client import client_window
from dispatcher import dispatcher_window

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Client (
        client_id INTEGER PRIMARY KEY,
        c_pib TEXT,
        c_phone_number TEXT,
        c_email TEXT,
        c_password TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dispatcher (
        dispatcher_id INTEGER PRIMARY KEY,
        d_pib TEXT,
        d_email TEXT,
        d_password TEXT,
        d_phone_number TEXT
    )
''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Train (
#         train_id INTEGER PRIMARY KEY,
#         num_of_wagons INTEGER,
#         condition TEXT,
#         year_of_manufacture INTEGER
#     )
# ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Itinerary (
        itinerary_id INTEGER PRIMARY KEY,
        departure_station TEXT,
        arrival_station TEXT,
        route_length REAL,
        duration REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Payment (
        payment_id INTEGER PRIMARY KEY,
        payment_amount REAL,
        payment_datetime TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS CargoType (
        cargo_type_id INTEGER PRIMARY KEY,
        cargo_name TEXT,
        description TEXT,
        dimensions TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cargo (
        cargo_id INTEGER PRIMARY KEY,
        cargo_type_id INTEGER,
        quantity INTEGER,
        weight REAL,
        FOREIGN KEY (cargo_type_id) REFERENCES CargoType(cargo_type_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Contract (
        contract_id INTEGER PRIMARY KEY,
        conclusion_date TEXT,
        client_id INTEGER,
        dispatcher_id INTEGER,
        cargo_id INTEGER,
        payment_id INTEGER,
        itinerary_id INTEGER,
        FOREIGN KEY (client_id) REFERENCES Client(client_id),
        FOREIGN KEY (payment_id) REFERENCES Payment(payment_id),
        FOREIGN KEY (dispatcher_id) REFERENCES Dispatcher(dispatcher_id),
        FOREIGN KEY (cargo_id) REFERENCES Cargo(cargo_id),
        FOREIGN KEY (itinerary_id) REFERENCES Itinerary(itinerary_id)
        )
    ''')

def register():
    user_type = user_type_combo.get()
    if user_type == "Dispatcher":
        d_pib = name_entry.get()
        d_email = email_entry.get()
        d_password = password_entry.get()
        d_phone_number = phone_entry.get()
        dispatcher = Dispatcher(d_pib, d_email, d_password, d_phone_number)

        cursor.execute("INSERT INTO Dispatcher (d_pib, d_email, d_password, d_phone_number) VALUES (?, ?, ?, ?)",
                       (dispatcher.get_d_pib(),
                        dispatcher.get_d_email(),
                        dispatcher.get_d_password(),
                        dispatcher.get_d_phone_number()))

    elif user_type == "Client":
        c_pib = name_entry.get()
        c_email = email_entry.get()
        c_password = password_entry.get()
        c_phone_number = phone_entry.get()
        client = Client(c_pib, c_email, c_password, c_phone_number)

        cursor.execute("INSERT INTO Client (c_pib, c_email, c_password, c_phone_number) VALUES (?, ?, ?, ?)",
                       (client.get_c_pib(),
                        client.get_c_email(),
                        client.get_c_password(),
                        client.get_с_phone_num()))

    conn.commit()
    messagebox.showinfo("Registration", "Registration Successful!")

def login():
    user_type = user_type_combo.get()
    email = email_entry.get()
    password = password_entry.get()
    phone_number = phone_entry.get()

    if user_type == "Dispatcher":
        cursor.execute("SELECT * FROM Dispatcher WHERE d_email=?", (email,))
        user = cursor.fetchone()
        if user and password == user[3]:
            messagebox.showinfo("Login", "Dispatcher Login Successful!")
            dispatcher_window()
        else:
            messagebox.showerror("Login Error", "Invalid email or password")
    elif user_type == "Client":
        cursor.execute("SELECT * FROM Client WHERE c_email=?", (email,))
        user = cursor.fetchone()
        if user and password == user[3]:
            messagebox.showinfo("Login", "Client Login Successful!")
            client_window()
        else:
            messagebox.showerror("Login Error", "Invalid email or password")


app = CTk()
app.title("Rail cargo solutions")
app.geometry("750x650")
app.resizable(0, 0)

# Відкриття зображень
side_img_data = Image.open("images/side-img.png")
email_icon_data = Image.open("images/email-icon.png")
password_icon_data = Image.open("images/password-icon.png")
pib_icon_data = Image.open("images/pib-icon.png")
phone_icon_data = Image.open("images/phone-icon.png")

# Створення об'єктів зображень CTkImage
side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(350, 650))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(25, 25))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(25, 25))
pib_icon = CTkImage(dark_image=pib_icon_data, light_image=pib_icon_data, size=(25, 25))
phone_icon = CTkImage(dark_image=phone_icon_data, light_image=phone_icon_data, size=(25, 25))

# Створення основного фрейму
frame = CTkFrame(master=app, width=350, height=650, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="left")

CTkLabel(master=frame, text="", image=side_img).pack(expand=True, side="left")

frame_right = CTkFrame(master=app, width=450, height=650, fg_color="#ffffff")
frame_right.pack_propagate(0)
frame_right.pack(expand=True, side="right")

CTkLabel(master=frame_right, text="Welcome back!",
         text_color="#601E88", anchor="w",
         justify="left",
         font=("Arial Bold", 32)).pack(anchor="w", pady=(50, 5), padx=(50, 0))

CTkLabel(master=frame_right,
         text="Sign in to your account",
         text_color="#7E7E7E", anchor="w",
         justify="left",
         font=("Arial Bold", 16)).pack(anchor="w", padx=(50, 0))

user_type_label = CTkLabel(master=frame_right,
                           text="User type:",
                           text_color="#601E88", anchor="w",
                           justify="left",
                           font=("Arial Bold", 16))
user_type_label.pack(anchor="w", pady=(20, 0), padx=(50, 0))

user_type_combo = CTkComboBox(master=frame_right,
                               values=["Dispatcher", "Client"],
                               font=("Arial Bold", 14))
user_type_combo.pack(anchor="w", pady=(10, 0), padx=(60, 0))

name_label = CTkLabel(master=frame_right, text="PIB:",
                      text_color="#601E88", anchor="w",
                      justify="left",
                      font=("Arial Bold", 15),
                      image=pib_icon, compound="left")
name_label.pack(anchor="w", pady=(18, 0), padx=(50, 0))

name_entry = CTkEntry(master=frame_right, width=300,
                      fg_color="#EEEEEE",
                      border_color="#601E88",
                      border_width=1,
                      text_color="#000000")
name_entry.pack(anchor="w", padx=(50, 0))

phone_label = CTkLabel(master=frame_right, text="Phone number:",
                        text_color="#601E88", anchor="w",
                        justify="left",
                        font=("Arial Bold", 15),
                        image=phone_icon, compound="left")
phone_label.pack(anchor="w", pady=(18, 0), padx=(50, 0))

phone_entry = CTkEntry(master=frame_right, width=300,
                        fg_color="#EEEEEE",
                        border_color="#601E88",
                        border_width=1,
                        text_color="#000000")
phone_entry.pack(anchor="w", padx=(50, 0))

CTkLabel(master=frame_right, text="Email:",
         text_color="#601E88",
         anchor="w", justify="left",
         font=("Arial Bold", 15),
         image=email_icon, compound="left").pack(anchor="w", pady=(18, 0), padx=(50, 0))

email_entry = CTkEntry(master=frame_right, width=300,
                       fg_color="#EEEEEE",
                       border_color="#601E88",
                       border_width=1,
                       text_color="#000000")
email_entry.pack(anchor="w", padx=(50, 0))

CTkLabel(master=frame_right, text="Password:",
         text_color="#601E88", anchor="w",
         justify="left", font=("Arial Bold", 15),
         image=password_icon, compound="left").pack(anchor="w", pady=(15, 0), padx=(50, 0))

password_entry = CTkEntry(master=frame_right,
                          width=300, fg_color="#EEEEEE",
                          border_color="#601E88", border_width=1, text_color="#000000", show="*")
password_entry.pack(anchor="w", padx=(50, 0))

CTkButton(master=frame_right, text="Register",
          fg_color="#601E88", hover_color="#E44982",
          font=("Arial Bold", 17),
          text_color="#ffffff", width=300, command=register).pack(anchor="w", pady=(40, 0), padx=(50, 0))

CTkButton(master=frame_right, text="Log in",
          fg_color="#601E88", hover_color="#E44982",
          font=("Arial Bold", 17),
          text_color="#ffffff", width=300, command=login).pack(anchor="w", pady=(10, 0), padx=(50, 0))

app.mainloop()
