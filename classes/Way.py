class Way:
    def __init__(self, distance, term):
        self.distance = distance
        self.term = term

    def set_distance(self, distance):
        self.distance = distance

    def set_term(self, term):
        self.term = term

    def get_distance(self):
        return self.distance

    def get_term(self):
        return self.term
