import json

class Map:
    def __init__(self, dep_st, arr_st, distance, duration):
        self.dep_st = dep_st
        self.arr_st = arr_st
        self.distance = distance
        self.duration = duration

    def set_dep_st(self, dep_st):
        self.dep_st = dep_st

    def set_arr_st(self, arr_st):
        self.arr_st = arr_st

    def get_dep_st(self):
        return self.dep_st

    def get_arr_st(self):
        return self.arr_st

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance

    def set_duration(self, duration):
        self.duration = duration

    def get_duration(self):
        return self.duration

    regional_centers = [
        "Kyiv", "Vinnytsia", "Lutsk", "Dnipro", "Donetsk", "Zhytomyr", "Uzhhorod", "Zaporizhzhia",
        "Ivano-Frankivsk", "Kropyvnytskyi", "Luhansk", "Lviv", "Mykolaiv", "Odesa", "Poltava",
        "Rivne", "Sumy", "Ternopil", "Kharkiv", "Kherson", "Khmelnytskyi", "Cherkasy",
        "Chernihiv", "Chernivtsi", "Simferopol"
    ]

    def is_station(self):
        with open('data/cities.json') as f:
            data = json.load(f)

        for route in data['routes']:
            if (route['source'] == self.dep_st and route['destination'] == self.arr_st) or \
                    (route['source'] == self.arr_st and route['destination'] == self.dep_st):
                return True, route['distance'], route['duration']
        return False, None, None


