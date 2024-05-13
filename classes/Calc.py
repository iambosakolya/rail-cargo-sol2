from classes.Tariff import Tariff


class Calc:
    def __init__(self, price, distance, duration, cargo_type, weight):
        self.price = price
        self.distance = distance
        self.duration = duration
        self.cargo_type = cargo_type
        self.weight = weight

    # def set_contract_id(self, contract_id):
    #     self.contract_id = contract_id

    def set_price(self, price):
        self.price = price

    def set_distance(self, distance):
        self.distance = distance

    def set_duration(self, duration):
        self.duration = duration

    def set_type(self, cargo_type):
        self.cargo_type = cargo_type

    # def get_contract_id(self):
    #     return self.contract_id

    def get_price(self):
        return self.price

    def get_distance(self):
        return self.distance

    def get_duration(self):
        return self.duration

    def get_cargo_type(self):
        return self.cargo_type

    def set_weight(self, weight):
        self.weight = weight

    def get_weight(self):
        return self.weight

    def calculate_price(self):
        # Implement the logic to calculate price based on distance and weight
        # For example:
        tariff = Tariff(self.distance, self.weight)
        self.price = tariff.get_tariff()
