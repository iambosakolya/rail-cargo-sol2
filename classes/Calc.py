from classes.Tariff import Tariff


class Calc:
    def __init__(self, price, distance, payment_date, duration, cargo_type, weight):
        self.price = price
        self.distance = distance
        self.payment_date = payment_date
        self.duration = duration
        self.cargo_type = cargo_type
        self.weight = weight

    def calculate_price(self):
        # the logic to calculate price based on distance and weight
        tariff = Tariff(self.distance, self.weight)
        self.price = tariff.get_tariff()

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def set_distance(self, distance):
        self.distance = distance

    def set_duration(self, duration):
        self.duration = duration

    def set_type(self, cargo_type):
        self.cargo_type = cargo_type

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
