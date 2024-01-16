import math
import re
import sys


class UTIL:
    def coerce(self, s1):
        def fun(s2):
            if s2 == "nil":
                return None
            else:
                return s2.lower() == "true" or (s2.lower() != "false" and s2)
        try:
            return float(s1)
        except:
            return fun(re.match(r'^\s*(.*\S)', s1).group(1))

    def cells(self, s):
        return [self.coerce(s1) for s1 in re.findall("([^,]+)", s)]

    def csv(self, src):
        i, src = 0, src if src == "-" else open(src)

        def read_line():
            nonlocal i
            s = src.readline()
            if s:
                i += 1
                return i, self.cells(s)
            else:
                src.close()

        return read_line

    def rounded(self, n, ndecs=None):
        if type(n) == str:
            return n
        if math.floor(n) == n:
            return n
        mult = 10**(ndecs or 2)
        return math.floor(n * mult + 0.5) / mult
