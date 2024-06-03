import customtkinter
import customtkinter as ctk
from customtkinter import *
from database.database_setup import cursor, conn

from modules.crud.update import find_client
from modules.crud.update import modifying_contract
from modules.crud.delete import confirm_delete_c
from modules.crud.read import show_contracts


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

btn_style2 = {
    "fg_color": "#897E9B",
    "hover_color": "#ffffff",
    "text_color": "#000000",
    "font": ("Arial Rounded MT Bold", 13)}

entry_style = {
    "fg_color": "#EEEEEE",
    "border_color": "#601E88",
    "border_width": 1,
    "text_color": "#000000"}


def client_window(user):
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

    CTkLabel(master=right_frame, text="You have\nthe ability to view:",
             text_color="#000000", anchor="w",
             justify="left",
             font=("Hanson", 15)).place(relx=0, rely=0, anchor="w", x=315, y=150)

    result_textbox = ctk.CTkTextbox(master=right_frame, width=270, height=500, wrap="word")
    result_textbox.place(relx=0, rely=0, anchor="w", x=30, y=340)

    # query section 1
    req_frame3 = ctk.CTkFrame(master=right_frame, fg_color="#D0C7DF",
                              width=80, height=550)
    req_frame3.place(relx=0, rely=0, anchor="w", x=330, y=415)

    fourth_btn = ctk.CTkButton(master=req_frame3, text="1",
                               **btn_style2)
    fourth_btn.pack(side="top", padx=10, pady=20)

    fifth_btn = ctk.CTkButton(master=req_frame3, text="2",
                              **btn_style2)
    fifth_btn.pack(side="top", padx=10, pady=20)

    sixth_btn = ctk.CTkButton(master=req_frame3, text="3",
                              **btn_style2)
    sixth_btn.pack(side="top", padx=10, pady=20)

    seventh_btn = ctk.CTkButton(master=req_frame3, text="4",
                                width=150, **btn_style2)
    seventh_btn.pack(side="top", padx=10, pady=20)

    eighth_btn = ctk.CTkButton(master=req_frame3, text="5",
                               **btn_style2)
    eighth_btn.pack(side="top", padx=10, pady=20)


    #left frame
    c_btn = CTkButton(master=left_frame, text="Change my info", **btn_style,
                      command=lambda: find_client(user[0]))
    c_btn.pack(anchor="w", pady=(80, 10), padx=(30, 0))


    up_btn = CTkButton(master=left_frame, text="My contracts", **btn_style,
                       command=lambda: show_contracts(user[0], result_textbox))
    up_btn.pack(anchor="w", pady=(80, 10), padx=(30, 0))


    add_btn = CTkButton(master=left_frame, text="Deactivate my account", **btn_style,
                        command=lambda: confirm_delete_c(user[0]))
    add_btn.pack(anchor="w", pady=(80, 10), padx=(25, 0))

    app.mainloop()
