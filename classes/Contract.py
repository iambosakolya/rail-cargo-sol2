
class Contract:
    def __init__(self, contract_id, dep_st, arr_st, price,
                 pib_c, map_obj, tariff_obj, calc_obj):
        self.contract_id = contract_id
        self.dep_st = dep_st
        self.arr_st = arr_st
        self.price = price
        self.pib_c = pib_c
        self.map = map_obj
        self.tariff = tariff_obj
        self.calc = calc_obj

    def set_contract_id(self, contract_id):
        self.contract_id = contract_id

    def set_dep_st(self, dep_st):
        self.dep_st = dep_st

    def set_arr_st(self, arr_st):
        self.arr_st = arr_st

    def set_price(self, price):
        self.price = price

    def set_pib_c(self, pib_c):
        self.pib_c = pib_c

    def get_contract_id(self):
        return self.contract_id

    def get_dep_st(self):
        return self.dep_st

    def get_arr_st(self):
        return self.arr_st

    def get_price(self):
        return self.price

    def get_pib_c(self):
        return self.pib_c
