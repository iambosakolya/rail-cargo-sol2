from CTkMessagebox import CTkMessagebox
import customtkinter

class CargoType:
    def __init__(self, cargo_types, description, dimensions, quantity, weight):
        self.cargo_types = cargo_types
        self.description = description
        self.dimensions = dimensions
        self.quantity = quantity
        self.weight = weight
        self.unavailable_cargo_types = [
            'Foods',
            'Livestock',
            'Minerals',
            'Explosives',
            'Radioactives',
            'Toxics',
            'Perishables',
            'Firearms',
            'Ammunition',
            'Chemicals',
            'Narcotics',
            'Poisons',
            'Waste materials',
            'Liquids',
            'Gases',
        ]

    def set_type(self, cargo_types):
        self.cargo_types = cargo_types

    def get_cargo_types(self):
        return self.cargo_types


    def set_dimensions(self, dimensions):
        self.dimensions = dimension

    def get_dimensions(self):
        return self.dimensions

    def set_weight(self, weight):
        self.weight = weight

    def get_weight(self):
        return self.weight

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

    def isCargoType(self):
        cargo_type = self.get_cargo_types()
        if cargo_type in self.unavailable_cargo_types:
            CTkMessagebox(title="Error", message="This cargo type is not available!", icon="cancel")
            return False
        else:
            return True