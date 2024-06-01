import re
import sqlite3
import database.database_setup
from datetime import datetime
import customtkinter
import customtkinter as ctk
from customtkinter import *
from database.database_setup import cursor, conn

label_style = {
    "text_color": "#000000",
    "anchor": "w",
    "justify": "left",
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

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

tables = [
    'Client', 'Dispatcher', 'Itinerary', 'Payment',
    'CargoType', 'Cargo', 'Contract', 'Contracts']
current_table_index = 0

def display_tables(table_name, text_box):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    text_box.configure(state='normal')
    text_box.delete(1.0, END)
    text_box.insert(END, f"Table: {table_name}\n")
    text_box.insert(END, " | ".join(columns) + "\n")
    text_box.insert(END, "-" * 100 + "\n")
    for row in rows:
        text_box.insert(END, " | ".join(map(str, row)) + "\n")
    text_box.configure(state='disabled')

def next_table(text_box):
    global current_table_index
    current_table_index = (current_table_index + 1) % len(tables)
    display_tables(tables[current_table_index], text_box)

def previous_table(text_box):
    global current_table_index
    current_table_index = (current_table_index - 1) % len(tables)
    display_tables(tables[current_table_index], text_box)

def contracts_window():
    contracts_window = ctk.CTk()
    contracts_window.title("Contracts")

    screen_width = contracts_window.winfo_screenwidth()
    screen_height = contracts_window.winfo_screenheight()

    app_width = 500
    app_height = 400

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    contracts_window.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    contracts_window.resizable(0, 0)

    screen_frame = ctk.CTkFrame(master=contracts_window, width=850, height=750, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    text_box = ctk.CTkTextbox(master=screen_frame, wrap="none")
    text_box.pack(expand=True, fill="both")

    button_frame = ctk.CTkFrame(master=screen_frame, fg_color="#FFFFFF")
    button_frame.pack(pady=10)

    prev_button = ctk.CTkButton(master=button_frame, text="Previous", height=40,
                                command=lambda: previous_table(text_box),
                                fg_color="#FFFFFF", hover_color="#897E9B",
                                text_color="#000000", font=("Arial Rounded MT Bold", 13))
    prev_button.pack(side="left", padx=10)

    next_button = ctk.CTkButton(master=button_frame, text="Next", height=40,
                                command=lambda: next_table(text_box),
                                fg_color="#FFFFFF",
                                hover_color="#897E9B", text_color="#000000",
                                font=("Arial Rounded MT Bold", 13))
    next_button.pack(side="left", padx=10)

    display_tables(tables[current_table_index], text_box)
    contracts_window.mainloop()
