import math
from util import coerce
class NUM:
    cohen = 0.35
    def __init__(self, s=None, n=None):
        self.txt = s or " "
        self.at = n or 0
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.hi = float("-inf")
        self.lo = float("inf")
        self.heaven = 0 if s and s.endswith("-") else 1

    def add(self, x):
        if not x == "?":
            self.n += 1
            d = x - self.mu
            self.mu += d / self.n
            self.m2 += d * (x - self.mu)
            self.lo = min(x, self.lo)
            self.hi = max(x, self.hi)

    def mid(self):
        return self.mu

    def div(self):
        return 0 if self.n < 2 else (self.m2 / (self.n - 1))**0.5
    
    def small (self):
        return self.cohen * self.div()
    
    def norm (self, x):
        return x if x == "?" else (x - self.lo) / (self.hi - self.lo + 1E-30)

    def like(self, x, _):
        mu, sd = self.mid(), (self.div() + 1E-30)
        num = 2.718 ** (-0.5 * (x - mu) ** 2 / (sd ** 2))
        denum = (sd * 2.5 + 1E-30)
        return num / denum
    
#addition for homework5
#--distance

    def dist(self, x, y):
        if x == "?" and y == "?":
            return 1
        x, y = self.norm(x), self.norm(y)
        if x == "?":
            x = 1 if y < 0.5 else 0
        if y == "?":
            y = 1 if x < 0.5 else 0
        return abs(x - y)
    
#function NUM:bin(x,     tmp)
#   tmp = (self.hi - self.lo) / (the.bins - 1)
#   return self.hi == self.lo and 1 or math.floor(x / tmp + .5) * tmp end
#--bin

    def bin(self, x):
        tmp = (self.hi - self.lo) / (the.bins - 1)
        return 1 if self.hi == self.lo else math.floor(x / tmp + 0.5) * tmp