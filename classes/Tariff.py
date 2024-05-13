
class Tariff:
    def __init__(self, distance, weight):
        self.distance = distance
        self.weight = weight

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance

    def set_weight(self, weight):
        self.weight = weight

    def get_weight(self):
        return self.weight

    def get_tariff(self):
        price_per_km = 2  # $1 per km
        base_price = 50  # ₴50 base price
        total_price = base_price + (self.distance * price_per_km)
        return total_price
