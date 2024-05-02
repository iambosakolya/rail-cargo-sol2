import customtkinter
from customtkinter import *
from classes.Contract import Contract
from classes.CargoType import CargoType
from database import cursor, conn
from tkinter import messagebox


def create(dep_st, arr_st, price, pib_c):
    new_contract = Contract(None, dep_st, arr_st, price, pib_c, None, None, None)

    cursor.execute('''
        INSERT INTO Contract (dep_date, arr_date, price, pib_c) 
        VALUES (?, ?, ?, ?)''',
        (new_contract.dep_st, new_contract.arr_st,
         new_contract.price, new_contract.pib_c))

    conn.commit()
    conn.close()

#def save_contract():

def create_contract():
    global screen_frame
    window_number = 1
    contract_window = CTk()
    contract_window.title(f"New contract-{window_number}")
    contract_window.geometry("600x500")
    contract_window.resizable(0, 0)

    x = (contract_window.winfo_screenwidth() - contract_window.winfo_reqwidth()) / 2
    y = (contract_window.winfo_screenheight() - contract_window.winfo_reqheight()) / 2
    contract_window.geometry("+%d+%d" % (x, y))

    screen_frame = CTkFrame(master=contract_window, width=850, height=750, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    def next_step():
        nonlocal window_number
        window_number += 1
        show_current_step()

    def show_current_step():
        global screen_frame
        screen_frame.destroy()
        screen_frame = CTkFrame(master=contract_window, width=850, height=750, fg_color="#897E9B")
        screen_frame.pack_propagate(0)
        screen_frame.pack(expand=True, fill="both")

        if window_number == 1:

            # cargo`s name
            type_label = CTkLabel(master=screen_frame, text="Choose your cargo type:",
                                  text_color="#000000", anchor="w",
                                  justify="left",
                                  font=("Arial Rounded MT Bold", 15))
            type_label.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

            cargo_types_input = input("Enter cargo types separated by commas: ")
            cargo_types_list = [t.strip() for t in cargo_types_input.split(",")]

            type_combobox = CTkComboBox(master=screen_frame, values=cargo_types_list, width=250)
            type_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=45)

            # ADD BUTTON - separate window
            add_btn1 = CTkButton(master=screen_frame, text="Add",
                                fg_color="#000000", hover_color="#4F2346",
                                font=("Arial Rounded MT Bold", 13),
                                width=40, text_color="#ffffff")
            add_btn1.place(relx=0, rely=0.1, anchor="w", x=300, y=45)
            # ADD BUTTON - separate window

            # cargo`s dimension
            type_label1 = CTkLabel(master=screen_frame, text="Choose allowed dimensions:",
                                   text_color="#000000", anchor="w",
                                   justify="left",
                                   font=("Arial Rounded MT Bold", 15))
            type_label1.place(relx=0, rely=0.1, anchor="w", x=30, y=95)

            dimensions_input = input("Enter dimensions separated by commas: ")
            dim_list = [d.strip() for d in dimensions_input.split(",")]

            dim_combobox = CTkComboBox(master=screen_frame, values=dim_list, width=250)
            dim_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=135)

            # ADD BUTTON - separate window
            add_btn2 = CTkButton(master=screen_frame, text="Add",
                                fg_color="#000000", hover_color="#4F2346",
                                font=("Arial Rounded MT Bold", 13),
                                width=40, text_color="#ffffff")
            add_btn2.place(relx=0, rely=0.1, anchor="w", x=300, y=135)
            # ADD BUTTON - separate window

            # cargo`s description
            description_input = input("Enter description: ")
            type_label2 = CTkLabel(master=screen_frame, text="Add description (if necessary):",
                                   text_color="#000000", anchor="w",
                                   justify="left",
                                   font=("Arial Rounded MT Bold", 15))
            type_label2.place(relx=0, rely=0.1, anchor="w", x=30, y=185)

            type_entry = CTkEntry(master=screen_frame,
                                  width=350, height=50,
                                  fg_color="#EEEEEE",
                                  border_color="#601E88",
                                  border_width=2,
                                  text_color="#000000")
            type_entry.insert(0, description_input)
            type_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=225)

            # cargo`s weight
            weight_label = CTkLabel(master=screen_frame, text="Enter weight:(kg)",
                                    text_color="#000000", anchor="w",
                                    justify="left",
                                    font=("Arial Rounded MT Bold", 15))
            weight_label.place(relx=0, rely=0.1, anchor="w", x=420, y=5)

            weight_input = CTkEntry(master=screen_frame,
                                    width=150, height=30,
                                    fg_color="#EEEEEE",
                                    border_color="#601E88",
                                    border_width=2,
                                    text_color="#000000")
            weight_input.place(relx=0, rely=0.1, anchor="w", x=420, y=45)

            # cargo`s quantity
            quantity_label = CTkLabel(master=screen_frame, text="Enter quantity:",
                                      text_color="#000000", anchor="w",
                                      justify="left",
                                      font=("Arial Rounded MT Bold", 15))
            quantity_label.place(relx=0, rely=0.1, anchor="w", x=420, y=95)

            quantity_input = CTkEntry(master=screen_frame,
                                      width=150, height=30,
                                      fg_color="#EEEEEE",
                                      border_color="#601E88",
                                      border_width=2,
                                      text_color="#000000")
            quantity_input.place(relx=0, rely=0.1, anchor="w", x=420, y=135)

            # buttons
            check_btn = CTkButton(master=screen_frame, text="Check availability",
                                  fg_color="#000000", hover_color="#4F2346",
                                  font=("Arial Rounded MT Bold", 13), text_color="#ffffff")
            check_btn.place(relx=0, rely=0.1, anchor="w", x=30, y=300)

            next_btn = CTkButton(master=screen_frame, text="Next step",
                                 fg_color="#000000", hover_color="#4F2346",
                                 font=("Arial Rounded MT Bold", 13), text_color="#ffffff",
                                 command=next_step)
            next_btn.place(relx=0, rely=0.1, anchor="w", x=420, y=400)

            cargo_type_obj = CargoType(cargo_types_list, dim_list,
                                       weight_input.get(), quantity_input.get(), description_input)



        elif window_number == 2:
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
                                 command=next_step)
            next_btn.place(relx=0, rely=0.1, anchor="w", x=420, y=400)

        elif window_number == 3:
            next_btn = CTkButton(master=screen_frame, text="Next step",
                                 fg_color="#000000", hover_color="#4F2346",
                                 font=("Arial Rounded MT Bold", 13), text_color="#ffffff",
                                 command=next_step)
            next_btn.place(relx=0, rely=0.1, anchor="w", x=420, y=400)

        elif window_number == 4:
            save_btn = CTkButton(master=screen_frame, text="Save contract",
                                 fg_color="#000000", hover_color="#4F2346",
                                 font=("Arial Rounded MT Bold", 13), text_color="#ffffff")
                                 #command=save_contract)
            save_btn.place(relx=0, rely=0.1, anchor="w", x=320, y=320)

    show_current_step()

    contract_window.mainloop()

def dispatcher_window():
    app = CTk()
    app.title("Dispatcher window")
    app.geometry("750x650")
    app.resizable(0, 0)

    right_frame = CTkFrame(master=app, width=550, height=650, fg_color="#897E9B")
    right_frame.pack_propagate(0)
    right_frame.pack(expand=True, side="right")

    CTkLabel(master=right_frame, text="").pack(expand=True, side="right")

    left_frame = CTkFrame(master=app, width=200, height=650, fg_color="#FFFFFF")
    left_frame.pack_propagate(0)
    left_frame.pack(expand=True, side="left")

    CTkLabel(master=right_frame, text="You are logged as a dispatcher",
             text_color="#000000", anchor="w",
             justify="center",
             font=("Arial Rounded MT Bold", 25)).place(relx=0, rely=0, anchor="w", x=90, y=30)

    c_btn = CTkButton(master=left_frame, text="New contract",
             fg_color="#000000", hover_color="#4F2346",
             font=("Arial Rounded MT Bold", 13), text_color="#ffffff",
             command=lambda: create_contract())
    c_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))

    up_btn = CTkButton(master=left_frame, text="Update contract",
                      fg_color="#000000", hover_color="#4F2346",
                      font=("Arial Rounded MT Bold", 13), text_color="#ffffff")
    up_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))

    del_btn = CTkButton(master=left_frame, text="Delete contract",
                       fg_color="#000000", hover_color="#4F2346",
                       font=("Arial Rounded MT Bold", 13), text_color="#ffffff")
    del_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))

    add_btn = CTkButton(master=left_frame, text="Add new....",
                        fg_color="#000000", hover_color="#4F2346",
                        font=("Arial Rounded MT Bold", 13), text_color="#ffffff")
    add_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))

    app.mainloop()
