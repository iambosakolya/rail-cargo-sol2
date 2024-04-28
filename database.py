import sqlite3
import bcrypt
from classes.Users import Dispatcher, Client

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Client (
            client_id INTEGER PRIMARY KEY,
            c_pib TEXT,
            c_email TEXT,
            c_password TEXT,
            c_phone_number TEXT
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

def register():
    user_type = user_type_combo.get()
    if user_type == "Dispatcher":
        d_pib = name_entry.get()
        d_email = email_entry.get()
        d_password = bcrypt.hashpw(password_entry.get().encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        d_phone_number = phone_entry.get()
        dispatcher = Dispatcher(d_pib, d_email, d_password, d_phone_number)

        cursor.execute("INSERT INTO Dispatcher (d_pib, d_email, d_password, d_phone_number) VALUES (?, ?, ?, ?)",
                       (dispatcher.get_d_pib(),
                        dispatcher.get_d_email(),
                        dispatcher.get_d_password(),
                        dispatcher.get_cabinet()))

    elif user_type == "Client":
        c_pib = name_entry.get()
        c_email = email_entry.get()
        c_password = bcrypt.hashpw(password_entry.get().encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        c_phone_number = phone_entry.get()
        client = Client(c_pib, c_email, c_password, c_phone_number)

        cursor.execute("INSERT INTO Client (c_pib, c_email, c_password, c_phone_number) VALUES (?, ?, ?, ?)",
                       (client.get_c_pib(),
                        client.get_c_email(),
                        client.get_c_password(),
                        client.get_phone_num()))

    conn.commit()
    messagebox.showinfo("Registration", "Registration Successful!")

def login():
    user_type = user_type_combo.get()
    email = email_entry.get()
    password = password_entry.get()
    phone_number = phone_entry.get()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    if user_type == "Dispatcher":
        cursor.execute("SELECT * FROM Dispatcher WHERE d_email=?", (email,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            messagebox.showinfo("Login", "Dispatcher Login Successful!")
        else:
            messagebox.showerror("Login Error", "Invalid email or password")
    elif user_type == "Client":
        cursor.execute("SELECT * FROM Client WHERE c_email=?", (email,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            messagebox.showinfo("Login", "Client Login Successful!")
        else:
            messagebox.showerror("Login Error", "Invalid email or password")
