import customtkinter
from customtkinter import *

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
             font=("Arial Rounded MT Bold", 25)).place(relx=0, rely=0, anchor="w", x=120, y=30)


    c_btn = CTkButton(master=left_frame, text="Change my info", **btn_style)
    c_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))


    up_btn = CTkButton(master=left_frame, text="My contracts", **btn_style)
    up_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))


    del_btn = CTkButton(master=left_frame, text="Update my contract", **btn_style)
    del_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))


    add_btn = CTkButton(master=left_frame, text="Deactivate my account", **btn_style)
    add_btn.pack(anchor="w", pady=(50, 5), padx=(30, 0))

    app.mainloop()
