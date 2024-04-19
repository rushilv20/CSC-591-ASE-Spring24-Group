from num import NUM
from sym import SYM
import re

class Cols:

    def __init__(self, the, row):
        self.names = row
        self.all = []
        self.x = []
        self.y = []
        self.klass = None
        self.the = the

        for index, name in enumerate(row.cells):
            col = NUM(self.the, name, index) if re.match("^[A-Z]", name) else SYM(self.the, name, index)
            self.all.append(col)

            if not name.endswith("X"):
                if name.endswith("!"):
                    self.klass = col

                if re.search("[!+-]$", name):
                    self.y.append(col)
                else:
                    self.x.append(col)

    def add(self, row):
        for columns in [self.x, self.y]:
            # print(columns)
            for col in columns:
                col.add(row.cells[col.at])
        return row
                    

    def __repr__(self):
        return f"Cols(names={self.names})"