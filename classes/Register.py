class Register:
    def __init__(self, contract_obj, map_obj, calc_obj, list_obj):
        self.contract_obj = contract_obj
        self.map_obj = map_obj
        self.calc_obj = calc_obj
        self.list_obj = list_obj

    def get_contract_id(self):
        return self.contract_obj.get_contract_id()

    def set_contract_id(self, contract_id):
        self.contract_obj.set_contract_id(contract_id)

    def check_station(self):
        return self.map_obj.is_station()

    def calculate_price(self):
        self.calc_obj.calculate_price()
        return self.calc_obj.get_price()

    def load_contracts(self):
        self.list_obj.load_contracts_from_db()

    def add_contract(self, contract_info):
        self.list_obj.add_contract(contract_info)

    def delete_contract(self, contract_info):
        self.list_obj.delete_contract_from_db(contract_info)
