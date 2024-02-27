import math


class SYM:
    def __init__(self, the, s=None, n=None):
        self.txt = s if s else " "
        self.at = n if n else 0
        self.n = 0
        self.has = {}
        self.mode = None
        self.most = 0
        self.the = the

    def add(self, x):
        if x != "?":
            self.n += 1
            self.has[x] = 1 + self.has.get(x, 0)
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def mid(self):
        return self.mode

    def div(self):
        e = 0
        for v in self.has.values():
            e += -v / self.n * math.log2(v / self.n)
        return e

    def small(self, small):
        return 0

    def like(self, x, prior):
        if(self.n + self.the.m == 0):
            return 0
        else:
            return ((self.has.get(x, 0) or 0) + self.the.m * prior) / (self.n + self.the.m)
        
#addition of homework 5
#     function SYM:dist(x,y)
#   return  (x=="?" and y=="?" and 1) or (x==y and 0 or 1) end
    def dist(self, x, y):
        return 1 if x == "?" and y == "?" else 0 if x == y else 1

#function SYM:bin(x) return x end
    def bin(self,x):
        return x