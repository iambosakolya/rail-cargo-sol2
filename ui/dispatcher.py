import sqlite3
import customtkinter
from CTkToolTip import *
import customtkinter as ctk
from customtkinter import *

from modules.crud.create import create_contract
from modules.crud.delete import delete_contract
from modules.crud.delete import confirm_delete_d
from modules.crud.delete import delete_client
from modules.crud.read import contracts_window
from modules.crud.update import find_dispatcher
from modules.crud.update import modifying_contract
from modules.crud.archive import show_archive_dialog

from database.database_setup import cursor, conn
from database.queries import find_clients
from database.queries import find_contracts_d
from database.queries import find_contracts_date
from database.queries import find_contracts_week
from database.queries import find_contracts_dispatcher
from database.queries import find_max_contracts
from database.queries import find_max_payment
from database.queries import find_dispatchers
from database.queries import find_dispatchers_comments

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


def dispatcher_window(user, dispatcher_id):
    app = CTk()
    app.title("Dispatcher window")

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

    # right frame
    CTkLabel(master=right_frame, text="You are logged as a dispatcher",
             text_color="#000000", anchor="w",
             justify="center",
             font=("Hanson", 20)).place(relx=0, rely=0, anchor="w", x=30, y=100)

    CTkLabel(master=right_frame, text="You have\nthe ability to view:",
             text_color="#000000", anchor="w",
             justify="left",
             font=("Hanson", 15)).place(relx=0, rely=0, anchor="w", x=315, y=190)

    #query section 1
    req_frame1 = ctk.CTkFrame(master=right_frame, fg_color="#D0C7DF", width=450, height=95)
    req_frame1.place(relx=0, rely=0, anchor="w", x=30, y=50)

    first_btn = ctk.CTkButton(master=req_frame1, text="Contracts\nby dispatcher",
                              **btn_style2, command=find_contracts_d)
    first_btn.pack(side="left", padx=10, pady=10)
    tooltip_1 = CTkToolTip(first_btn, message="Вибір з декількох таблиць із сортуванням"
                                              "\nCписок контрактів, які були створені заданим диспетчером")


    second_btn = ctk.CTkButton(master=req_frame1, text="Search clients\nby a letter",
                               **btn_style2, command=find_clients)
    second_btn.pack(side="left", padx=10, pady=10)
    tooltip_2 = CTkToolTip(second_btn, message="Завдання умови відбору з використанням предиката LІKE"
                                               "\nЗнайти всіх клієнтів, чиє прізвище починається на задану букву")


    third_btn = ctk.CTkButton(master=req_frame1, text="Contracts\nby date",
                              **btn_style2, command=find_contracts_date)
    third_btn.pack(side="left", padx=10, pady=10)
    tooltip_3 = CTkToolTip(third_btn, message="Завдання умови відбору з використанням предиката BETWEEN"
                                              "\nСписок контрактів, які були згенеровані в заданий період")

    result_textbox = ctk.CTkTextbox(master=right_frame, width=270, height=470, wrap="word")
    result_textbox.place(relx=0, rely=0, anchor="w", x=30, y=380)

    #query section 2
    req_frame3 = ctk.CTkFrame(master=right_frame, fg_color="#D0C7DF",
                              width=80, height=550)
    req_frame3.place(relx=0, rely=0, anchor="w", x=330, y=435)

    fourth_btn = ctk.CTkButton(master=req_frame3, text="Contract counter\nfor the week",
                               **btn_style2, command=lambda: find_contracts_week(result_textbox))
    fourth_btn.pack(side="top", padx=10, pady=10)
    tooltip_4 = CTkToolTip(fourth_btn, message="Агрегатна функція без угруповання"
                                               "\nCкільки контрактів було "
                                               "за останній тиждень")

    fifth_btn = ctk.CTkButton(master=req_frame3, text="Contract counter"
                                                      "\nby dispatcher",
                               **btn_style2, command=lambda: find_contracts_dispatcher(result_textbox))
    fifth_btn.pack(side="top", padx=10, pady=12)
    tooltip_5 = CTkToolTip(fifth_btn, message="Агрегатна функція з угрупованням"
                                              "\nCкільки контрактів було укладено"
                                              " кожним диспетчером")


    sixth_btn = ctk.CTkButton(master=req_frame3, text="Max contracts "
                                                      "\nby dispatcher",
                              **btn_style2, command=lambda: find_max_contracts(result_textbox))
    sixth_btn.pack(side="top", padx=10, pady=12)
    tooltip_6 = CTkToolTip(sixth_btn, message="Використання предиката ALL або ANY"
                                              "\nХто з диспетчерів уклав найбільшу "
                                              "кількість контрактів")


    seventh_btn = ctk.CTkButton(master=req_frame3, text="Top paying client"
                                                        "\nby cargo type",
                                width=150,**btn_style2,
                                command=lambda: find_max_payment(result_textbox))
    seventh_btn.pack(side="top", padx=10, pady=12)
    tooltip_7 = CTkToolTip(seventh_btn, message="Корельований підзапит"
                                                "\nЗнайти клієнтів, які зробили найбільші оплати "
                                                "для відповідного типу вантажу.")


    eighth_btn = ctk.CTkButton(master=req_frame3, text="Dispatchers with "
                                                       "\nno contracts",
                               **btn_style2,
                               command=lambda: find_dispatchers(result_textbox))
    eighth_btn.pack(side="top", padx=10, pady=12)
    tooltip_8 = CTkToolTip(eighth_btn, message="Запит на заперечення"
                                               "\nЗапит реалізувати у трьох варіантах: з використанням"
                                               "LEFT JOІN, предиката ІN і предиката EXІSTS;"
                                               "\nХто з диспетчерів не укладав контракти на цьому тижні?")


    ninth_btn = ctk.CTkButton(master=req_frame3, text="Dispatchers and"
                                                      "\ncontract status",
                              **btn_style2,
                              command=lambda: find_dispatchers_comments(result_textbox))
    ninth_btn.pack(side="top", padx=10, pady=12)
    tooltip_9 = CTkToolTip(ninth_btn, message="Операція об'єднання UNІON із включенням коментарю в кожен рядок"
                                              "\nСписок усіх диспетчерів з коментарем "
                                              "\n«Має максимальну кількість заключених контрактів»,"
                                              "\n«Має в цей час заключених контрактів»,"
                                              "\n«Має n заклюених контрактів»")

    # left frame --> buttons
    info_btn = CTkButton(master=left_frame, text="Change my info",
                         **btn_style, command=lambda: find_dispatcher(user[0]))
    info_btn.pack(anchor="w", pady=(40, 5), padx=(30, 0))


    c_btn = CTkButton(master=left_frame, text="New contract",
                      **btn_style, command=lambda: create_contract())
    c_btn.pack(anchor="w", pady=(40, 5), padx=(30, 0))


    list_btn = CTkButton(master=left_frame, text="All contracts",
                         **btn_style, command=contracts_window)
    list_btn.pack(anchor="w", pady=(40, 5), padx=(30, 0))


    up_btn = CTkButton(master=left_frame, text="Delete contract",
                       **btn_style, command=delete_contract)
    up_btn.pack(anchor="w", pady=(40, 5), padx=(30, 0))


    add_btn = CTkButton(master=left_frame, text="Update contract",
                        **btn_style, command=modifying_contract)
    add_btn.pack(anchor="w", pady=(40, 5), padx=(30, 0))


    deld_btn = CTkButton(master=left_frame, text="Deactivate \ndispatcher account",
                         **btn_style, command=lambda: confirm_delete_d(user[0]))
    deld_btn.pack(anchor="w", pady=(40, 5), padx=(30, 0))


    delc_btn = CTkButton(master=left_frame, text="Deactivate \nclient account",
                         **btn_style, command=delete_client)
    delc_btn.pack(anchor="w", pady=(40, 5), padx=(30, 0))

    arch_btn = CTkButton(master=left_frame, text="Contract archive",
                         command=lambda: show_archive_dialog(cursor, conn),
                         **btn_style)
    arch_btn.pack(anchor="w", pady=(40, 5), padx=(30, 0))

    app.mainloop()
