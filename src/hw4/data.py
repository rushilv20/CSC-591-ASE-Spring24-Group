import math
import csv
from sym import SYM
from rows import ROW
from cols import COLS
from util import Utility


class Data:
    def __init__(self, the, src, fun=None):
        self.rows = []
        self.cols = None
        self.the = the
        self.util = Utility()
        self.adds(src, fun)

    def adds(self, src, fun=None):
        if isinstance(src, str):
            for s in self.util.csv(file=src):
                self.add(s, fun)
        else: 
            for x in (src or []):
                self.add(x, fun)
        return self
    
    def add(self, t, fun=None):
        if hasattr(t, 'cells'):
            row = t
        else:
            row = ROW(self.the, t)

        #print(self.cols)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)

    def mid(self, cols=None):
        arr = []
        for col in cols or self.cols.all:
            arr.append(col.mid())
        return ROW(self.the, arr)

    def div(self, cols=None):
        arr = []
        for col in cols or self.cols.all:
            arr.append(col.div())
        return ROW(self.the, arr)

    def small(self):
        arr = []
        for col in self.cols.all:
            arr.append(col.small())
        return ROW(self.the, arr)

    def stats(self, cols=None, fun=None, ndivs=None):
        arr = {".N": len(self.rows)}
        columns_to_iterate = getattr(self.cols, cols or "y", [])
        #print (columns_to_iterate)

        for col in columns_to_iterate:
            value = getattr(type(col), fun or "mid")(col)
            arr[col.txt] = round(value, 2)
        return arr

    def clone(self, rows=None):
        new = Data(self.the)
        new.cols.names = self.cols.names
        for row in rows or []:
            new.add(row)
        return new

    def gate(self, budget0, budget, some):
        stats = []
        bests = []
        rows = self.util.shuffle(self.rows)
        lite = rows[:budget0]
        dark = rows[budget0:]
        
        for i in range(1, budget+1):
            best, rest = self.bestRest(lite, len(lite)**some)
            todo, selected = self.split(best, rest, lite, dark)
            stats[i] = selected.mid()
            bests[i] = best.rows[0]
            lite.append(dark.pop(todo))
        
        return stats, bests

    def split(self, best, rest, lite_rows, dark_rows):
        selected = Data(self.the, self.cols.names)
        max_val = 1E30
        out = 1
        
        for i, row in enumerate(dark_rows):
            b = row.like(best, len(lite_rows), 2)
            r = row.like(rest, len(lite_rows), 2)
            if b > r:
                selected.add(row)
            tmp = abs(b + r) / abs(b - r + 1E-300)
            if tmp > max_val:
                out, max_val = i, tmp
        
        return out, selected
    


    def bestRest(self, rows, wanted):
        rows.sort(key=lambda a: a.d2h(self))
        best = [self.cols['names']]
        rest = [self.cols['names']]
        
        for i, row in enumerate(rows):
            if i <= wanted:
                best.append(row)
            else:
                rest.append(row)
        
        return Data(self.the, best), Data(self.the, rest)
def rep_rows(t, rows):
    rows = copy(rows)
    for j, s in enumerate(rows[-1]):
        rows[0][j] += (":" + s)

    del rows[-1]

    for n, row in enumerate(rows):
        if n == 0:
            row.append("thingX")
        else:
            u = t['rows'][len(t['rows']) - n]
            row.append(u[-1])
    return Data(rows)

def rep_cols(cols):
    cols = copy(cols)

    for column in cols:
        column[len(column) - 1] = str(column[0]) + ':' + str(column[len(column) - 1])

        for j in range(1, len(column)):
            column[j - 1] = column[j]

        column.pop()

    cols.insert(0, [helper(i + 1) for i in range(len(cols[0]))])
    cols[0][len(cols[0]) - 1] = "thingX"
    return Data(cols)

def rep_place(data):
    n = 20
    g = [[''] * n for _ in range(n)]
    maxy = 0
    print("")
    for r, row in enumerate(data.rows):
        c = chr(64 + r + 1)
        print(c, row.cells[-1])
        x, y = int(row.x * n), int(row.y * n)
        maxy = max(maxy, y)
        g[y][x] = c
    print("")
    for y in range(0, maxy):
        frmt = "{:>3}" * len(g[y])

        print("{" + frmt.format(*g[y]) + "}")

def rep_grid(sFile):
    t = do_file(sFile)
    rows = rep_rows(t, transpose(t['cols']))
    cols = rep_cols(t['cols'])
    show(rows.cluster())
    show(cols.cluster())
    rep_place(rows)


