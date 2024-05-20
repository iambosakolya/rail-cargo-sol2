elif window_number == 2:


def find_connection():
    dep_station = dep_entry.get()
    arr_station = arr_entry.get()

    if dep_station and dep_station[0].islower():
        CTkMessagebox(message="Please enter the departure station with a capital letter!", icon="cancel")
        return
    if arr_station and arr_station[0].islower():
        CTkMessagebox(message="Please enter the arrival station with a capital letter!", icon="cancel")
        return

    map_obj = Map(dep_station, arr_station, 0, 0)
    is_connection, distance, duration = map_obj.is_station()

    if is_connection:
        message = f"Railway connection exists!\nDistance: {distance} km\nDuration: {duration} hours"
        CTkMessagebox(message=message, icon="check", option_1="Ok")
        result_text.delete("1.0", "end")
        result_text.insert("1.0", message)
        save_btn.configure(state="normal")
    else:
        CTkMessagebox(title="Error", message="Railway connection doesn't exist", icon="cancel")
        save_btn.configure(state="disabled")

def save_route():
    dep_station = dep_entry.get()
    arr_station = arr_entry.get()

    map = Map(dep_station, arr_station, 0, 0)
    is_connection, distance, duration = map.is_station()

    if is_connection:
        cursor.execute(
            "INSERT INTO Itinerary (departure_station, arrival_station, route_length, duration) VALUES (?, ?, ?, ?)",
            (dep_station, arr_station, distance, duration))
        conn.commit()
        CTkMessagebox(message="Route saved successfully!", icon="info", option_1="Ok")
    else:
        CTkMessagebox(title="Error", message="Cannot save route. Railway connection doesn't exist",
                      icon="cancel")


label1 = CTkLabel(master=screen_frame,
                  text="Enter the stations and check if the railway connection exists:",
                  text_color="#000000", anchor="w", justify="left", font=("Arial Rounded MT Bold", 17))
label1.place(relx=0, rely=0.1, anchor="w", x=30, y=5)

label2 = CTkLabel(master=screen_frame,
                  text="Reminder:\nSystem works only with ukrainian cities.\nBegin with capital letter.",
                  text_color="#CCCCCC", anchor="w", justify="left", font=("Arial Rounded MT Bold", 14))
label2.place(relx=0, rely=0.1, anchor="w", x=30, y=60)

dep_label = CTkLabel(master=screen_frame, text="Departure station:", **label_style)
dep_label.place(relx=0, rely=0.1, anchor="w", x=30, y=130)

dep_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
dep_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=160)

arr_label = CTkLabel(master=screen_frame, text="Arrival station:", **label_style)
arr_label.place(relx=0, rely=0.1, anchor="w", x=30, y=190)

arr_entry = CTkEntry(master=screen_frame, width=300, **entry_style)
arr_entry.place(relx=0, rely=0.1, anchor="w", x=30, y=220)

result_text = CTkTextbox(master=screen_frame, width=180, height=200)
result_text.place(relx=0, rely=0.1, anchor="w", x=370, y=170)

# buttons
check_btn1 = CTkButton(master=screen_frame, text="Check availability", **btn_style,
                       command=find_connection).place(relx=0, rely=0.1, anchor="w", x=30, y=320)

save_btn = CTkButton(master=screen_frame, text="Save route", width=90, **btn_style,
                     command=save_route, state="disabled")
save_btn.place(relx=0, rely=0.1, anchor="w", x=200, y=320)

reminder = CTkLabel(master=screen_frame, text="Dont forget to save the route!:",
                    text_color="#CCCCCC", anchor="w", justify="left", font=("Arial Rounded MT Bold", 14))
reminder.place(relx=0, rely=0.1, anchor="w", x=200, y=350)

next_btn = CTkButton(master=screen_frame, text="Next step", **btn_style,
                     command=next_step).place(relx=0, rely=0.1, anchor="w", x=420, y=400)