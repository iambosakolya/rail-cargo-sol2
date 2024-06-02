import customtkinter
import customtkinter as ctk
from customtkinter import *
from database.database_setup import cursor, conn

from modules.crud.update import find_client
from modules.crud.delete import delete_client

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

def client_window():
    app = CTk()
    app.title("Client window")

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    app_width = 750
    app_height = 650

    x_position = (screen_width - app_width) // 2
    y_position = (screen_height - app_height) // 2

    app.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    app.resizable(0, 0)

    right_frame = CTkFrame(master=app, width=550, height=650, fg_color="#897E9B")
    right_frame.pack_propagate(0)
    right_frame.pack(expand=True, side="right")

    CTkLabel(master=right_frame, text="").pack(expand=True, side="right")

    left_frame = CTkFrame(master=app, width=200, height=650, fg_color="#FFFFFF")
    left_frame.pack_propagate(0)
    left_frame.pack(expand=True, side="left")

    CTkLabel(master=right_frame, text="You are logged as a client",
             text_color="#000000", anchor="w",
             justify="center",
             font=("Hanson", 20)).place(relx=0, rely=0, anchor="w", x=80, y=50)

    result_textbox = ctk.CTkTextbox(master=right_frame, width=270, height=470, wrap="word")
    result_textbox.place(relx=0, rely=0, anchor="w", x=30, y=380)


    c_btn = CTkButton(master=left_frame, text="Change my info", **btn_style,
                      command=find_client)
    c_btn.pack(anchor="w", pady=(70, 5), padx=(30, 0))


    up_btn = CTkButton(master=left_frame, text="My contracts", **btn_style)
    up_btn.pack(anchor="w", pady=(70, 5), padx=(30, 0))


    del_btn = CTkButton(master=left_frame, text="Update my contract", **btn_style)
    del_btn.pack(anchor="w", pady=(70, 5), padx=(30, 0))


    history_btn = CTkButton(master=left_frame, text="View my order history", **btn_style)
    history_btn.pack(anchor="w", pady=(70, 5), padx=(27, 0))


    add_btn = CTkButton(master=left_frame, text="Deactivate my account", **btn_style,
                        command=delete_client)
    add_btn.pack(anchor="w", pady=(70, 5), padx=(25, 0))

    app.mainloop()
