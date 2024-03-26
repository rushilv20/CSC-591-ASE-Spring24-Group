import math
from num import NUM
from sym import SYM
import re

class COLS:
    def __init__(self, row):
        self.x, self.y, self.all = [], [], []
        self.klass, self.col = None, None
        self.names = row.cells

        for idx, name in enumerate(row.cells):
            col = NUM(name, idx) if re.match("^[A-Z]", name) else SYM(name, idx)
            self.all.append(col)

            if not name.endswith("X"):
                if name.endswith("!"):
                    self.klass = col

                #updated to simpler code
                if re.search("[!+-]$", name):
                    self.y.append(col)
                else:
                    self.x.append(col)

    def add(self, row):
        for cols in [self.x, self.y]:
            for col in cols:
                col.add(row.cells[col.at])

    def __repr__(self):
        return f"Cols(names={self.names})"