class Node:
    def __init__(self, data):
        self.here = data
        self.lefts = None
        self.rights = None

    def walk(self, fun, depth=0):
        fun(self, depth, not (self.lefts or self.rights))
        if self.lefts:
            self.lefts.walk(fun, depth + 1)
        if self.rights:
            self.rights.walk(fun, depth + 1)

    def show(self):
        def d2h(data):
            return round(data.mid().d2h(self.here), ndigits=2)

        max_depth = 0

        def _show(node, depth, leafp):
            nonlocal max_depth
            cells_list = [round(cell, 2) for cell in node.here.mid().cells]
            post = (str(round(d2h(node.here), 2)) + "\t" + str(cells_list)) if leafp else ""
            max_depth = max(max_depth, depth)
            print(('|.. ' * depth) + post)

        self.walk(_show)
        print("")
        cells_list = [round(cell, 2) for cell in self.here.mid().cells]
        print(("    " * max_depth) + f"{d2h(self.here)}\t{cells_list}")
        print(("    " * max_depth) + "_\t" + str(self.here.cols.names.cells))