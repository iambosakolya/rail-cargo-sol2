class RailCargoSol:
    def __init__(self, city_location, company_name):
        self.city_location = city_location
        self.company_name = company_name

    def set_city_location(self, city_location):
        self.city_location = city_location

    def set_company_name(self, company_name):
        self.company_name = company_name

    def get_city_location(self):
        return self.city_location

    def get_company_name(self):
        return self.company_name

    def __str__(self):
        return f"{self.company_name}, {self.city_location}"

