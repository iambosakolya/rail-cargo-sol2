class Map:
    def __init__(self, dep_st, arr_st):
        self.dep_st = dep_st
        self.arr_st = arr_st

    def set_dep_st(self, dep_st):
        self.dep_st = dep_st

    def set_arr_st(self, arr_st):
        self.arr_st = arr_st

    def get_dep_st(self):
        return self.dep_st

    def get_arr_st(self):
        return self.arr_st
