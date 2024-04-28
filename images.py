

def load_images():
    side_img_data = Image.open("images/side-img.png")
    email_icon_data = Image.open("images/email-icon.png")
    password_icon_data = Image.open("images/password-icon.png")

    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(350, 650))
    email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(25, 25))
    password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(25, 25))

    return side_img, email_icon, password_icon
