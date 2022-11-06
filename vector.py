class Vector(list):
    def __add__(self, other):
        lst = []
        for indx, i in enumerate(self):
            lst.append(i + other[indx])
        return lst
    def __sub__(self, other):
        lst = []
        for indx, i in enumerate(self):
            lst.append(i - other[indx])
        return lst
    def __mul__(self, __n: SupportsIndex) -> list[_T]:
        return super().__mul__(__n)
