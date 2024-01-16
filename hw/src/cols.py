import math


class COLS:
    def __init__(self):
        self.x, self.y, self.all = [], [], []
        self.klass, self.col = None, None

    def new(self, row):
        for at, txt in enumerate(row.cells):
            col = (NUM if txt[0].isalpha()
                   and txt[0].isupper() else SYM)(txt, at)
            self.all.append(col)

            if not txt.endswith("X"):
                if txt.endswith("!"):
                    self.klass = col
                (self.y if txt.endswith("!") or txt.endswith("+")
                 or txt.endswith("-") else self.x)[at] = col

        # check this with Ratish
        self.names = row.cells

    def add(self, row):
        for cols in [self.x, self.y]:
            for col in cols:
                col.add(row.cells[col.at])
        return row
