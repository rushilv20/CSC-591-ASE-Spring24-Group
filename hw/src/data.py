import math
import csv


class Data:
    def __init__(self, src, fun):
        self.rows = []
        self.cols = None
        self.adds(src, fun)

    def adds(self, src, fun):
        if type(src) == "string":
            for x in csv.reader(src.splitlines()):
                self.add(x, fun)
        else:
            for x in src or []:
                self.add(x, fun)

    def add(self, t, fu)
