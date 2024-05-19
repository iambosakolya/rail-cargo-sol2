
class Contract:
    def __init__(self, contract_id, concl_date, pib_c, c_phone_number, c_email,
                 pib_d, cargo_obj, map_obj, calc_obj):
        self.contract_id = contract_id
        self.concl_date = concl_date
        self.c_email = c_email
        self.pib_d = pib_d
        self.pib_c = pib_c
        self.c_phone_number = c_phone_number
        self.map_obj = map_obj
        self.calc_obj = calc_obj
        self.cargo_obj = cargo_obj

    def get_contract_id(self):
        return self.contract_id

    def set_contract_id(self, contract_id):
        self.contract_id = contract_id

    def set_concl_date(self, concl_date):
        self.concl_date = concl_date

    def set_arr_st(self, c_email):
        self.c_email = c_email

    def set_pib_d(self, pib_d):
        self.pib_d = pib_d

    def set_pib_c(self, pib_c):
        self.pib_c = pib_c

    def get_concl_date(self):
        return self.concl_date

    def get_c_email(self):
        return self.c_email

    def get_pib_d(self):
        return self.pib_d

    def get_pib_c(self):
        return self.pib_c
