class Calc:
    def __init__(self, contract_id, price, distance, term, cargo_type):
        self.contract_id = contract_id
        self.price = price
        self.distance = distance
        self.term = term
        self.cargo_type = cargo_type

    def set_contract_id(self, contract_id):
        self.contract_id = contract_id

    def set_price(self, price):
        self.price = price

    def set_distance(self, distance):
        self.distance = distance

    def set_term(self, term):
        self.term = term

    def set_type(self, cargo_type):
        self.cargo_type = cargo_type

    def get_contract_id(self):
        return self.contract_id

    def get_price(self):
        return self.price

    def get_distance(self):
        return self.distance

    def get_term(self):
        return self.term

    def get_cargo_type(self):
        return self.cargo_type
