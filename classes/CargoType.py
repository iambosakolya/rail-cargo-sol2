class CargoType:
    cargo_types = []

    def __init__(self, cargo_type):
        self.cargo_type = cargo_type

    def set_type(self, cargo_type):
        self.cargo_type = cargo_type

    def get_cargo_type(self):
        return self.cargo_type

    @classmethod
    def add_future_type(cls, cargo_type):
        cls.cargo_types.append(cargo_type)
