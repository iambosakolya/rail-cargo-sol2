from customtkinter import CTk, CTkImage, CTkFrame, CTkLabel, CTkComboBox, CTkEntry, CTkButton
#from tkinter import messagebox
from PIL import Image
from database import register, login

def create_ui():
    app = CTk()
    app.title("Rail cargo solutions")
    app.geometry("750x650")
    app.resizable(0, 0)

    # Відкриття зображень
    side_img_data = Image.open("images/side-img.png")
    email_icon_data = Image.open("images/email-icon.png")
    password_icon_data = Image.open("images/password-icon.png")
    pib_icon_data = Image.open("images/pib-icon.png")
    phone_icon_data = Image.open("images/phone-icon.png")

    # Створення об'єктів зображень CTkImage
    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(350, 650))
    email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(25, 25))
    password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(25, 25))
    pib_icon = CTkImage(dark_image=pib_icon_data, light_image=pib_icon_data, size=(25, 25))
    phone_icon = CTkImage(dark_image=phone_icon_data, light_image=phone_icon_data, size=(25, 25))

    # Створення основного фрейму
    frame = CTkFrame(master=app, width=350, height=650, fg_color="#ffffff")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="left")

    # Лейбли, ентрі, кнопки зі зміненими розмірами та розташуванням
    CTkLabel(master=frame, text="", image=side_img).pack(expand=True, side="left")

    frame_right = CTkFrame(master=app, width=450, height=650, fg_color="#ffffff")
    frame_right.pack_propagate(0)
    frame_right.pack(expand=True, side="right")

    CTkLabel(master=frame_right, text="Welcome back!",
             text_color="#601E88", anchor="w",
             justify="left",
             font=("Arial Bold", 32)).pack(anchor="w", pady=(50, 5), padx=(50, 0))

    CTkLabel(master=frame_right,
             text="Sign in to your account",
             text_color="#7E7E7E", anchor="w",
             justify="left",
             font=("Arial Bold", 16)).pack(anchor="w", padx=(50, 0))

    user_type_label = CTkLabel(master=frame_right,
                               text="User type:",
                               text_color="#601E88", anchor="w",
                               justify="left",
                               font=("Arial Bold", 16))
    user_type_label.pack(anchor="w", pady=(20, 0), padx=(50, 0))

    user_type_combo = CTkComboBox(master=frame_right,
                                  values=["Dispatcher", "Client"],
                                  font=("Arial Bold", 16))
    user_type_combo.pack(anchor="w", pady=(10, 0), padx=(60, 0))

    name_label = CTkLabel(master=frame_right, text="PIB:",
                          text_color="#601E88", anchor="w",
                          justify="left",
                          font=("Arial Bold", 19),
                          image=pib_icon, compound="left")
    name_label.pack(anchor="w", pady=(18, 0), padx=(50, 0))

    name_entry = CTkEntry(master=frame_right, width=300,
                          fg_color="#EEEEEE",
                          border_color="#601E88",
                          border_width=1,
                          text_color="#000000")
    name_entry.pack(anchor="w", padx=(50, 0))

    phone_label = CTkLabel(master=frame_right, text="Phone number:",
                           text_color="#601E88", anchor="w",
                           justify="left",
                           font=("Arial Bold", 19),
                           image=phone_icon, compound="left")
    phone_label.pack(anchor="w", pady=(18, 0), padx=(50, 0))

    phone_entry = CTkEntry(master=frame_right, width=300,
                           fg_color="#EEEEEE",
                           border_color="#601E88",
                           border_width=1,
                           text_color="#000000")
    phone_entry.pack(anchor="w", padx=(50, 0))

    CTkLabel(master=frame_right, text="Email:",
             text_color="#601E88",
             anchor="w", justify="left",
             font=("Arial Bold", 19),
             image=email_icon, compound="left").pack(anchor="w", pady=(18, 0), padx=(50, 0))

    email_entry = CTkEntry(master=frame_right, width=300,
                           fg_color="#EEEEEE",
                           border_color="#601E88",
                           border_width=1,
                           text_color="#000000")
    email_entry.pack(anchor="w", padx=(50, 0))

    CTkLabel(master=frame_right, text="Password:",
             text_color="#601E88", anchor="w",
             justify="left", font=("Arial Bold", 19),
             image=password_icon, compound="left").pack(anchor="w", pady=(15, 0), padx=(50, 0))

    password_entry = CTkEntry(master=frame_right,
                              width=300, fg_color="#EEEEEE",
                              border_color="#601E88", border_width=1, text_color="#000000", show="*")
    password_entry.pack(anchor="w", padx=(50, 0))

    CTkButton(master=frame_right, text="Register",
              fg_color="#601E88", hover_color="#E44982",
              font=("Arial Bold", 17),
              text_color="#ffffff", width=300, command=register).pack(anchor="w", pady=(40, 0), padx=(50, 0))

    CTkButton(master=frame_right, text="Log in",
              fg_color="#601E88", hover_color="#E44982",
              font=("Arial Bold", 17),
              text_color="#ffffff", width=300, command=login).pack(anchor="w", pady=(10, 0), padx=(50, 0))

    app.mainloop()
