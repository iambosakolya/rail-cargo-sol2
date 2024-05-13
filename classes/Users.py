class Dispatcher:
    def __init__(self, d_pib, d_email, d_password, d_phone_number):
        self.d_pib = d_pib
        self.d_email = d_email
        self.d_password = d_password
        self.d_phone_number = d_phone_number

    def set_d_pib(self, d_pib):
        self.d_pib = d_pib

    def set_d_password(self, d_password):
        self.d_password = d_password

    def set_d_(self, d_email):
        self.d_email = d_email

    def set_d_phone_number(self, d_phone_number):
        self.d_phone_number = d_phone_number

    def get_d_pib(self):
        return self.d_pib

    def get_d_email(self):
        return self.d_email

    def get_d_password(self):
        return self.d_password

    def get_d_phone_number(self):
        return self.d_phone_number


class Client:
    def __init__(self, c_pib, c_email, c_password, с_phone_number):
        self.c_pib = c_pib
        self.c_email = c_email
        self.c_password = c_password
        self.с_phone_number = с_phone_number

    def set_name(self, c_pib):
        self.c_pib = c_pib

    def set_с_phone_number(self, с_phone_number):
        self.с_phone_number = с_phone_number

    def set_c_email(self, c_email):
        self.c_email = c_email

    def set_c_password(self, c_password):
        self.c_password = c_password

    def get_c_pib(self):
        return self.c_pib

    def get_с_phone_num(self):
        return self.с_phone_number

    def get_c_email(self):
        return self.c_email

    def get_c_password(self):
        return self.c_password


