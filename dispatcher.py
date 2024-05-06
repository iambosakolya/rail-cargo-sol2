import customtkinter
from CTkToolTip import *
from customtkinter import *
from database import cursor, conn
from classes.Contract import Contract
from classes.CargoType import CargoType
from CTkMessagebox import CTkMessagebox

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

def insert_type(name, description, dimensions):
    try:
        cursor.execute("INSERT INTO CargoType (name, description, dimensions) VALUES (?, ?, ?)", (name, description, dimensions))
        conn.commit()
        CTkMessagebox(message="Info saved!",
                      icon="check", option_1="Ok")
    except sqlite3.Error as e:
        conn.rollback()
        CTkMessagebox(title="Error", message="Type info is not saved", icon="cancel")

def insert_cargo(cargo_type_id, quantity, weight):
    cursor.execute("SELECT COUNT(*) FROM CargoType WHERE cargo_type_id = ?", (cargo_type_id,))
    count = cursor.fetchone()[0]
    if count == 0:
        CTkMessagebox(title="Error", message="cargo_type_id does not exist in the CargoType table", icon="cancel")
        return
    cursor.execute("INSERT INTO Cargo (cargo_type_id, quantity, weight) VALUES (?, ?, ?)", (cargo_type_id, quantity, weight))
    conn.commit()

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

        def cargo_type_check(cargo_instance):
            if cargo_instance.isCargoType():
                CTkMessagebox(message="Cargo type is available",icon="check", option_1="Thanks")
            else:
                CTkMessagebox(title="Error", message="This cargo type is not available!", icon="cancel")

        if window_number == 1:
            # cargo`s name
            type_label = CTkLabel(master=screen_frame, text="Choose your cargo type:",
                                  text_color="#000000", anchor="w",
                                  justify="left",
                                  font=("Arial Rounded MT Bold", 15))
            type_label.place(relx=0, rely=0.1, anchor="w", x=30, y=5)


            type_combobox = CTkComboBox(master=screen_frame, values=['   ', 'Freight', 'Coal', 'Grains', 'Steel', 'Lumber',
                                                                     'Oil', 'Chemicals', 'Machinery',
                                                                     'Automobiles', 'Containers', 'Livestock',
                                                                     'Cement', 'Fertilizer', 'Papers'], width=250)

            type_combobox.place(relx=0, rely=0.1, anchor="w", x=30, y=45)

            add_label = CTkLabel(master=screen_frame, text="Or enter new type:",
                                 text_color="#000000", anchor="w",
                                 justify="left",
                                 font=("Arial Rounded MT Bold", 15))
            add_label.place(relx=0, rely=0.1, anchor="w", x=420, y=5)

            type_entry = CTkEntry(master=screen_frame, width=140)
            type_entry.place(relx=0, rely=0.1, anchor="w", x=420, y=45)

            # ADD BUTTON - adding new type
            def new_type():
                new_cargo_type = type_entry.get().strip()
                if new_cargo_type == "":
                    return
                if not new_cargo_type[0].isupper():
                    tooltip_add.configure(message="Please enter the new cargo type with a capital letter!")
                    return
                existing_cargo_types = type_combobox.cget('values')
                new_cargo_type = type_entry.get()
                existing_cargo_types.append(new_cargo_type)
                type_combobox.configure(values=existing_cargo_types)

            add_btn1 = CTkButton(master=screen_frame, text="Add",
                                 fg_color="#000000", hover_color="#4F2346",
                                 font=("Arial Rounded MT Bold", 13),
                                 width=40, text_color="#ffffff",
                                 command=new_type)
            add_btn1.place(relx=0, rely=0.1, anchor="w", x=350, y=45)

            tooltip_add = CTkToolTip(add_btn1, message="Please enter the new cargo type "
                                                       "\nwith a capital letter and in plural!")
            # ADD BUTTON - adding new type


            # adding data to table "cargo types"
            def save_cargo():
                # save cargo type data
                name = type_combobox.get().strip()
                description = desc_entry.get()
                dimensions = dim_entry.get()
                insert_type(name, description, dimensions)

                # save cargo data
                selected_type = type_combobox.get()
                quantity = quantity_input.get()
                weight = weight_input.get()
                cursor.execute("SELECT cargo_type_id FROM CargoType WHERE name = ?", (selected_type,))
                result = cursor.fetchone()

                if result is None:
                    CTkMessagebox(title="Error", message="Selected cargo type not found", icon="cancel")
                    return

                cargo_type_id = result[0]
                insert_cargo(cargo_type_id, quantity, weight)

            save = CTkButton(master=screen_frame, text="Save type",
                                  fg_color="#000000", hover_color="#4F2346",
                                  font=("Arial Rounded MT Bold", 13), width=90,
                                  text_color="#ffffff" ,command=save_cargo)
            save.place(relx=0, rely=0.1, anchor="w", x=200, y=300)
            # adding data to table "cargo types"

            # cargo`s dimension
            type_label1 = CTkLabel(master=screen_frame, text="Enter dimensions:",
                                   text_color="#000000", anchor="w",
                                   justify="left",
                                   font=("Arial Rounded MT Bold", 15))
            type_label1.place(relx=0, rely=0.1, anchor="w", x=30, y=95)

            dim_entry = CTkEntry(master=screen_frame,
                                      width=150, height=30,
                                      fg_color="#EEEEEE",
                                      border_color="#601E88",
                                      border_width=2,
                                      text_color="#000000")
            dim_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=135)

            # cargo`s description
            type_label2 = CTkLabel(master=screen_frame, text="Add description (if necessary):",
                                   text_color="#000000", anchor="w",
                                   justify="left",
                                   font=("Arial Rounded MT Bold", 15))
            type_label2.place(relx=0, rely=0.1, anchor="w", x=30, y=185)

            desc_entry = CTkEntry(master=screen_frame,
                                  width=350, height=50,
                                  fg_color="#EEEEEE",
                                  border_color="#601E88",
                                  border_width=2,
                                  text_color="#000000")
            desc_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=225)

            # cargo`s weight
            weight_label = CTkLabel(master=screen_frame, text="Enter weight:(kg)",
                                    text_color="#000000", anchor="w",
                                    justify="left",
                                    font=("Arial Rounded MT Bold", 15))
            weight_label.place(relx=0, rely=0.1, anchor="w", x=420, y=185)

            weight_input = CTkEntry(master=screen_frame,
                                    width=150, height=30,
                                    fg_color="#EEEEEE",
                                    border_color="#601E88",
                                    border_width=2,
                                    text_color="#000000")
            weight_input.place(relx=0, rely=0.1, anchor="w", x=420, y=225)

            # cargo`s quantity
            quantity_label = CTkLabel(master=screen_frame, text="Enter quantity:",
                                      text_color="#000000", anchor="w",
                                      justify="left",
                                      font=("Arial Rounded MT Bold", 15))
            quantity_label.place(relx=0, rely=0.1, anchor="w", x=420, y=265)

            quantity_input = CTkEntry(master=screen_frame,
                                      width=150, height=30,
                                      fg_color="#EEEEEE",
                                      border_color="#601E88",
                                      border_width=2,
                                      text_color="#000000")
            quantity_input.place(relx=0, rely=0.1, anchor="w", x=420, y=295)

            # buttons
            check_btn = CTkButton(master=screen_frame, text="Check availability",
                                  fg_color="#000000", hover_color="#4F2346",
                                  font=("Arial Rounded MT Bold", 13), text_color="#ffffff",
                                  command=lambda: cargo_type_check(CargoType(type_combobox.get(),
                                                                             dim_entry.get(), weight_input.get(),
                                                                             quantity_input.get(), desc_entry.get())))
            check_btn.place(relx=0, rely=0.1, anchor="w", x=30, y=300)

            next_btn = CTkButton(master=screen_frame, text="Next step",
                                 fg_color="#000000", hover_color="#4F2346",
                                 font=("Arial Rounded MT Bold", 13), text_color="#ffffff",
                                 command=next_step)
            next_btn.place(relx=0, rely=0.1, anchor="w", x=420, y=400)


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
