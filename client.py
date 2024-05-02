import customtkinter
from customtkinter import *


def client_window():
    app = CTk()
    app.title("Client window")
    app.geometry("750x650")
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
             font=("Arial Rounded MT Bold", 25)).place(relx=0, rely=0.1, anchor="w", x=150, y=30)


    app.mainloop()
