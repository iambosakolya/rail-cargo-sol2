from CTkToolTip import *
import customtkinter as ctk
from customtkinter import *

from modules.crud.update import find_client
from modules.crud.delete import confirm_delete_c
from modules.crud.read import show_contracts

from database.queries_client import display_contracts_last_week
from database.queries_client import get_user_data
from database.queries_client import get_contracts_above_weight
from database.queries_client import get_user_payments

import modules.print as print_module

import globals
from ui.style import btn_style_user, btn_style2


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

    left_frame = CTkFrame(master=app, width=200,
                          height=650, fg_color="#FFFFFF")
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
    req_frame1 = ctk.CTkFrame(master=right_frame, fg_color="#D0C7DF",
                              width=80, height=700)
    req_frame1.place(relx=0, rely=0, anchor="w", x=330, y=320)

    first_btn = ctk.CTkButton(master=req_frame1, text="My contracts\nfor the last week", **btn_style2,
                               command=lambda: display_contracts_last_week(user_id=globals.logged_in_client_id,
                                                                           result_textbox=result_textbox))
    first_btn.pack(side="top", padx=20, pady=20)
    tooltip_1 = CTkToolTip(first_btn, message="Список контрактів укладених клієнтом за останній тиждень")


    second_btn = ctk.CTkButton(master=req_frame1, text="My current account info", **btn_style2,
                               command=lambda: get_user_data(user_id=globals.logged_in_client_id,
                                                             result_textbox=result_textbox))
    second_btn.pack(side="top", padx=20, pady=20)
    tooltip_1 = CTkToolTip(second_btn, message="Список даних клієнта")


    third_btn = ctk.CTkButton(master=req_frame1, text="Contract with the\nmax weight", **btn_style2,
                              command=lambda: get_contracts_above_weight(user_id=globals.logged_in_client_id,
                                                                         result_textbox=result_textbox, weight=5))
    third_btn.pack(side="top", padx=0, pady=20)
    tooltip_3 = CTkToolTip(third_btn, message="Які з контрактів клієнта мають вагу більше ніж 5т")


    fourth_btn = ctk.CTkButton(master=req_frame1, text="My payments", **btn_style2,
                                command=lambda: get_user_payments(user_id=globals.logged_in_client_id,
                                                                  result_textbox=result_textbox))
    fourth_btn.pack(side="top", padx=20, pady=20)
    tooltip_4 = CTkToolTip(fourth_btn, message="Знайти всі оплати клієнта і вивести їх")

    #left frame
    c_btn = CTkButton(master=left_frame, text="Change my info",  **btn_style_user,
                      command=lambda: find_client(user[0]))
    c_btn.pack(anchor="w", pady=(80, 10), padx=(30, 0))


    up_btn = CTkButton(master=left_frame, text="All my contracts",  **btn_style_user,
                       command=lambda: show_contracts(user[0], result_textbox))
    up_btn.pack(anchor="w", pady=(80, 10), padx=(30, 0))

    h_btn = ctk.CTkButton(master=left_frame, text="Print my contracts",
                          command=lambda: print_module.select_contract_print(globals.logged_in_client_id),
                          **btn_style_user)
    h_btn.pack(anchor="w", pady=(80, 10), padx=(25, 0))


    add_btn = CTkButton(master=left_frame, text="Deactivate my account",  **btn_style_user,
                        command=lambda: confirm_delete_c(user[0]))
    add_btn.pack(anchor="w", pady=(80, 10), padx=(23, 0))


    app.mainloop()
