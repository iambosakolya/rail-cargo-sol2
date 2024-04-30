import customtkinter
from customtkinter import *
from classes.Contract import Contract
from database import cursor, conn
from tkinter import messagebox

current_window = 1

def create(dep_st, arr_st, price, pib_c):
    new_contract = Contract(None, dep_st, arr_st, price, pib_c, None, None, None)

    cursor.execute('''
        INSERT INTO Contract (dep_date, arr_date, price, pib_c) 
        VALUES (?, ?, ?, ?)''',
        (new_contract.dep_st, new_contract.arr_st,
         new_contract.price, new_contract.pib_c))

    conn.commit()
    conn.close()

def next_window():
    global current_window
    current_window += 1
    if current_window > 4:
        current_window = 1
    create_contract(current_window)

#def save_contract():

def create_contract(window_number):
    contract_window = CTk()
    contract_window.title(f"New сontract-{window_number}")
    contract_window.geometry("500x400")
    contract_window.resizable(0, 0)

    x = (contract_window.winfo_screenwidth() - contract_window.winfo_reqwidth()) / 2
    y = (contract_window.winfo_screenheight() - contract_window.winfo_reqheight()) / 2
    contract_window.geometry("+%d+%d" % (x, y))

    screen_frame = CTkFrame(master=contract_window, width=850, height=750, fg_color="#8876A7")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    if window_number == 1:
        type_label = CTkLabel(master=screen_frame, text="Enter cargo type:",
                              text_color="#000000", anchor="w",
                              justify="left",
                              font=("Arial Rounded MT Bold", 15))
        type_label.pack(anchor="w", pady=(18, 0), padx=(50, 0))

        type_entry = CTkEntry(master=screen_frame, width=350,
                              fg_color="#EEEEEE",
                              border_color="#601E88",
                              border_width=2,
                              text_color="#000000")
        type_entry.pack(anchor="w", padx=(50, 0))

        # add combobox -> "the most common cargo types chosen by our customers"

        next_btn = CTkButton(master=screen_frame, text="Next step",
                             fg_color="#000000", hover_color="#4F2346",
                             font=("Arial Rounded MT Bold", 13), text_color="#ffffff",
                             command=next_window)
        next_btn.pack(anchor="w", pady=(50, 5), padx=(50, 0))


    if window_number == 2:
        dep_label = CTkLabel(master=screen_frame, text="Departure station:",
                             text_color="#000000", anchor="w",
                             justify="left",
                             font=("Arial Rounded MT Bold", 15))
        dep_label.pack(anchor="w", pady=(18, 0), padx=(50, 0))

        dep_entry = CTkEntry(master=screen_frame, width=300,
                             fg_color="#EEEEEE",
                             border_color="#601E88",
                             border_width=1,
                             text_color="#000000")
        dep_entry.pack(anchor="w", padx=(50, 0))

        arr_label = CTkLabel(master=screen_frame, text="Arrival station:",
                             text_color="#000000", anchor="w",
                             justify="left",
                             font=("Arial Rounded MT Bold", 15))
        arr_label.pack(anchor="w", pady=(32, 0), padx=(50, 0))

        arr_entry = CTkEntry(master=screen_frame, width=300,
                             fg_color="#EEEEEE",
                             border_color="#601E88",
                             border_width=1,
                             text_color="#000000")
        arr_entry.pack(anchor="w", padx=(55, 0))

        next_btn = CTkButton(master=screen_frame, text="Next step",
                             fg_color="#000000", hover_color="#4F2346",
                             font=("Arial Rounded MT Bold", 13), text_color="#ffffff",
                             command=next_window)
        next_btn.pack(anchor="w", pady=(50, 5), padx=(50, 0))


    if window_number == 3:
        next_btn = CTkButton(master=screen_frame, text="Next step",
                             fg_color="#000000", hover_color="#4F2346",
                             font=("Arial Rounded MT Bold", 13), text_color="#ffffff",
                             command=next_window)
        next_btn.pack(anchor="w", pady=(50, 5), padx=(50, 0))


    if window_number == 4:
        save_btn = CTkButton(master=screen_frame, text="Save contract",
                             fg_color="#000000", hover_color="#4F2346",
                             font=("Arial Rounded MT Bold", 13), text_color="#ffffff")
                             #command=save_contract)
        save_btn.pack(anchor="w", pady=(50, 5), padx=(50, 0))

    contract_window.mainloop()

def dispatcher_window():
    app = CTk()
    app.title("Dispatcher window")
    app.geometry("750x650")
    app.resizable(0, 0)

    screen_frame = CTkFrame(master=app, width=850, height=750, fg_color="#8876A7")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    CTkLabel(master=screen_frame, text="You are logged as a dispatcher",
             text_color="#000000", anchor="w",
             justify="center",
             font=("Hanson", 17)).pack(anchor="w", pady=(5, 5), padx=(180, 0))

    c_btn = CTkButton(master=screen_frame, text="New contract",
             fg_color="#000000", hover_color="#4F2346",
             font=("Arial Rounded MT Bold", 13), text_color="#ffffff",
             command=lambda: create_contract(current_window))
    c_btn.pack(anchor="w", pady=(50, 5), padx=(50, 0))

    app.mainloop()
