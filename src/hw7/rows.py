import math

import sys
from util import coerce
class ROW:
    def __init__(self, the, cells):
        self.cells = cells
        self.the = the

    
    def likes(self, datas):
        n, nHypotheses = 0, 0
        for k, data in datas.items():
            n += len(data.rows)
            nHypotheses += 1

        most, out = None, None
        for k, data in datas.items():
            tmp = self.like(data, n, nHypotheses)
            if most is None or tmp > most:
                most, out = tmp, k
        return out, most

    def like(self, data, n, nHypotheses):
        # print(data.rows, self.the.k)
        prior = (len(data.rows) + self.the.k) / (n + self.the.k * nHypotheses)
        out = math.log(prior)

        for col in data.cols.x:
            v = self.cells[col.at]
            if v != "?":
                inc = col.like(v, prior)
                # out += math.log(inc)
                try:
                    out += math.log(inc)
                except ValueError:
                    return 0.0
                
        return math.exp(1) ** out

    def d2h(self, data):
        d, n = 0, 0
        for col in data.cols.y:
            n += 1
            d += abs(col.heaven - col.norm(self.cells[col.at])) ** 2
        return math.sqrt(d) / math.sqrt(n)
    
    #addition for homework 5
    def dist(self, other, data):
        d, n, p = 0, 0, 2
        for col in data.cols.x.values():
            n += 1
            d += col.dist(coerce(self.cells[col.at-1]), coerce(other.cells[col.at-1])) ** p
           
        return (d / n) ** (1 / p)
    
    def neighbors(self, data, rows=None):
        if rows is None:
            rows = data.rows
        return sorted(rows, key=lambda row: self.dist(row, data))