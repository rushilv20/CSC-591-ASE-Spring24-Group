from util import Utility
from rows import ROW
from cols import Cols as COLS
from node import NODE
import random

# ----------------------------------------------------------------------------
# Data Class

is_debug = False

class DATA:
    def __init__(self, the, src, fun=None):
        self.rows = []
        self.cols = None
        self.the = the
        self.util = Utility(the)
        self.adds(src, fun)
        # print("Construting..")

    def adds(self, src, fun=None):
        if isinstance(src, str):
            # Here the _ is just because pairs returns two values.
            for x in self.util.l_csv(file=src):
                # print(x)
                self.add(x, fun)
        else:
            # for attr in dir(src):
            #     print("obj.%s = %r" % (attr, getattr(src, attr)))
            ## also did some debugging here.
            for x in (src or []):
                self.add(x, fun)
            # self.add(src, fun)
        return self

    def add(self, t, fun=None):
        # Made changes to the following block of code
        # print("Before", t)
        # if t is None:
        #     return 0
        if hasattr(t, 'cells'):
            row = t
        else:
            row = ROW(self.the, t)
        # print("After", row)
        # row = ROW(t) if type(t) is list else t.cells
        # row = t if t.cells else ROW(t)  Check line 182 might be different.
        # print(self.cols)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
            # print(self.rows)
        else:
            self.cols = COLS(self.the, row)

    def mid(self, cols=None):
        u = []
        for col in cols or self.cols.all:
            u.append(col.mid())
        return ROW(self.the, u)

    def div(self, cols=None):
        u = []
        for col in cols or self.cols.all:
            u.append(col.div())
        return ROW(self.the, u)
    
    def small(self):
        u = []
        for col in self.cols.all:
            u.append(col.small())
        return ROW(self.the, u)
    
    def stats(self, cols=None, fun=None, ndivs=None):
        u = {".N": len(self.rows)}
        # print(self.rows)
        columns_to_iterate = getattr(self.cols, cols or "y", [])
        for col in columns_to_iterate:
            value = getattr(type(col), fun or "mid")(col)
            #print("Value = " , value)
            u[col.txt] = self.util.rnd(value, ndivs)
            # print(value)
            # u[col.txt] = round(value,2)
        return u
    
    def clone(self, rows=None):
        new = DATA(self.the, [self.cols.names])
        new.cols.names = self.cols.names
        for row in rows or []:
            new.add(row)
        return new
    
    def gate(self, budget0, budget, some):
        stats = []
        bests = []
        rows = self.util.shuffle(self.rows)
        # print(self.rows)
        lite = rows[:budget0]
        dark = rows[budget0:]
        for i in range(budget):
            best, rest = self.bestRest(lite, len(lite)**some)
            todo, selected = self.split(best, rest, lite, dark)
            stats.append(selected.mid())
            bests.append(best.rows[0])
            lite.append(dark.pop(todo))
        return stats, bests
    
    def split(self, best, rest, lite_rows, dark_rows):
        selected = DATA(self.the, [self.cols.names])
        max_val = 1E30
        out = 1
        # print(dark_rows)
        for i, row in enumerate(dark_rows):
            b = row.like(best, len(lite_rows), 2)
            r = row.like(rest, len(lite_rows), 2)
            if b > r:
                selected.add(row)
            tmp = abs(b + r) / abs(b - r + 1E-300)
            if tmp > max_val:
                out, max_val = i, tmp
        return out, selected
    
    def bestRest(self, rows, want):
        rows.sort(key=lambda a: a.d2h(self))
        # rows.sort(key=lambda a: a.d2h(self))
        # best = [self.cols['names']]
        # rest = [self.cols['names']]
        best = [self.cols.names]
        rest = [self.cols.names]
        for i, row in enumerate(rows):
            if i <= want:
                best.append(row)
            else:
                rest.append(row)
        return DATA(self.the, best), DATA(self.the, rest)
    
    def farapart(self, rows, sortp=None, a=None, b=None):
        far = int(len(rows) * self.the.Far) // 1
        evals = 1 if a else 2
        a = a or random.choice(rows).neighbors(self, rows)[far]
        b = a.neighbors(self, rows)[far]
        if sortp and b.d2h(self) < a.d2h(self):
            a, b = b, a
        return a, b, a.dist(b, self), evals

    def half(self, rows, sortp, before):
        """
        as_ = The better side, bs  = The worse side
        a   = the better point, b  = The worse point
        C   = distance from a to b
        """
        some = self.util.many(rows, min(self.the.Half, len(rows)))
        a, b, C, evals = self.farapart(some, sortp, before)
        def dist(row1, row2):
            return row1.dist(row2, self)
        def project(r):
            return (dist(r, a)**2 + C**2 - dist(r, b)**2) / (2 * C)

        as_, bs = [], []
        for n, row in enumerate(self.util.keysort(rows, project)):
            if n <= (len(rows) // 2 - 1):
                as_.append(row)
            else:
                bs.append(row)

        return as_, bs, a, b, C, dist(a, bs[0]), evals

    def tree(self, sortp):
        evals = 0

        def _tree(data, above=None):
            nonlocal evals
            node = NODE(data)
            if len(data.rows) > 2 * len(self.rows) ** 0.5:
                lefts, rights, node.left, node.right, node.C, node.cut, evals1 = self.half(data.rows, sortp, above)
                evals = evals + evals1
                node.lefts = _tree(self.clone(lefts), node.left)
                node.rights = _tree(self.clone(rights), node.right)
            return node

        return _tree(self), evals

    def branch(self, stop=None):
        evals = 1
        rest = []
        if not stop:
            stop = (2 * (len(self.rows)) ** 0.5)

        def _branch(data, above=None, left=None, lefts=None, rights=None):
            nonlocal evals
            if len(data.rows) > stop:
                # as_, bs, a, b, C, dist(a, bs[0]), evals
                lefts, rights, left, _, _, _, _ = self.half(data.rows, True, above)
                evals += 1
                rest.extend(rights)
                return _branch(data.clone(lefts), left)
            else:
                return self.clone(data.rows), self.clone(rest), evals
        return _branch(self)

#data = DATA(src='../data/auto93.csv')

#print(data.stats())