class Dispatcher:
    def __init__(self, d_pib, experience, cabinet):
        self.d_pib = d_pib
        self.experience = experience
        self.cabinet = cabinet

    def set_d_pib(self, d_pib):
        self.d_pib = d_pib

    def set_experience(self, experience):
        self.experience = experience

    def set_cabinet(self, cabinet):
        self.cabinet = cabinet

    def get_d_pib(self):
        return self.d_pib

    def get_experience(self):
        return self.experience

    def get_cabinet(self):
        return self.cabinet


class Client:
    def __init__(self, c_pib, phone_num, address):
        self.c_pib = c_pib
        self.phone_num = phone_num
        self.address = address

    def set_name(self, c_pib):
        self.c_pib = c_pib

    def set_phone_num(self, phone_num):
        self.phone_num = phone_num

    def set_address(self, address):
        self.address = address

    def get_c_pib(self):
        return self.c_pib

    def get_phone_num(self):
        return self.phone_num

    def get_address(self):
        return self.address

