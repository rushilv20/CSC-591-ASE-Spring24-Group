class RULE:
    def __init__(self, ranges, the):
        self.parts = {}
        self.the = the
        self.scored = 0
        rule = self
    
        for range_ in ranges:
            t = rule.parts.get(range_.txt, [])
            t.append(range_)
            rule.parts[range_.txt] = t
    
    def _or(self, ranges, row):
        x = row.cells[ranges[0].at]
        if x == "?":
            return True
        for range_ in ranges:
            #print(range_.x, type(range_.x))
            lo, hi = range_.x['lo'], range_.x['hi']
            if lo == hi and lo == x or lo <= x < hi:
                return True
        return False

    def _and(self, row):
        for _, ranges in self.parts.items():
            if not self._or(ranges, row):
                return False
        return True

    def selects(self, rows):
        t = []
        for r in rows:
            if self._and(r):
                t.append(r)
        return t
    
    def selectss(self, rowss):
        t = {}
        for y, rows in rowss.items():
            t[y] = len(self.selects(rows))
        return t

    def _show_less(self, t, ready=False):
        if not ready:
            t.sort(key=lambda x: x.x['lo'])

        i, u = 0, []
        while i < len(t):
            a = t[i]
            if i < len(t) - 1:
                if a.x['hi'] == t[i + 1].x['lo']:
                    a = a.merge(t[i + 1]) 
                    i += 1
            u.append(a)
            i += 1

        return t if len(u) == len(t) else self._show_less(u, ready=True)
    
    def show(self, ands=None):
        #print("inside show")
        if ands is None:
            ands = []
        #print(self.parts.items())
        for _, ranges in self.parts.items():
            #print(ranges)
            ors = self._show_less(ranges)
            at = None
            for i, range_ in enumerate(ors):
                at = range_.at
                ors[i] = range_.show()
            ands.append(" or ".join(ors))
        return " and ".join(ands)


    