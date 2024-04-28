class Tariff:
    def __init__(self, distance, arr_st, cargo_type):
        self.distance = distance
        self.arr_st = arr_st
        self.cargo_type = cargo_type

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance

    def set_type(self, cargo_type):
        self.cargo_type = cargo_type

    def get_cargo_type(self):
        return self.cargo_type
