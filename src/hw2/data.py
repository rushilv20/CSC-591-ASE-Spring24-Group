import math
import csv
from sym import SYM
from rows import ROW
from cols import COLS
from util import UTIL


class Data:
    def __init__(self, src, fun):
        self.rows = []
        self.cols = None

        if type(src) == "string":
            with open(src, 'r') as file:
                for x in csv.reader(file):
                    self.add(x, fun)
        else:
            for x in src or []:
                self.add(x, fun)

    def add(self, t=None, fun=None):
        row = ROW(t) if type(t) == list else t
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)

    def mid(self, cols=None):
        u = [col.mid() for col in (cols or self.cols.all)]
        return ROW(u)

    def div(self, cols=None):
        u = [col.div() for col in (cols or self.cols.all)]
        return ROW(u)

    def stats(self, fun=None, ndivs=None):
        u = {".N": len(self.rows)}
        for col in self.cols.all:
            if(isinstance(col, SYM)):
                u[col.txt] = col.mid()
            else:
                u[col.txt] = UTIL.rounded(col.mid())
        return u
