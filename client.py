import customtkinter
from customtkinter import *


def client_window():
    app = CTk()
    app.title("Client window")
    app.geometry("750x650")
    app.resizable(0, 0)

    screen_frame = CTkFrame(master=app, width=750, height=650, fg_color="#8876A7")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    CTkLabel(master=screen_frame, text="Client window",
             text_color="#000000", anchor="w",
             justify="center",
             font=("Hanson", 30)).pack(anchor="w", pady=(50, 5), padx=(50, 0))

    app.mainloop()
