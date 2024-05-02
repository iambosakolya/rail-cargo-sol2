class CargoType:
    def __init__(self, cargo_types, description, dimensions, quantity, weight):
        self.cargo_types = cargo_types
        self.description = description
        self.dimensions = dimensions
        self.quantity = quantity
        self.weight = weight

    def set_type(self, cargo_types):
        self.cargo_types = cargo_types

    def get_cargo_types(self):
        return self.cargo_types


    def get_dimensions(self):
        return self.dimensions

    def set_dimensions(self, dimensions):
        self.dimensions = dimensions


    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description


    def set_quantity(self, quantity):
        self.description = quantity

    def get_quantity(self):
        return self.quantity