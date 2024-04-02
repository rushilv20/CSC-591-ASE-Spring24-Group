from util import coerce,copy

class RULE:
    def __init__(self, ranges,the):
        self.parts = {}
        self.scored = 0
        self.the=the
        rule=self
        for range in ranges:
            k=rule.parts.get(range.txt, [])
            k.append(range)
            rule.parts[range.txt] = k
        # print(rule.parts)

    def _or(self, ranges, row):
        
        x = row.cells[ranges[0].at-1]
        if x == "?":
            return True
        for range in ranges:
            
            lo, hi = range.x['lo'], range.x['hi']
            # x, lo, hi = coerce(x), coerce(lo), coerce(hi)

            if (lo == hi and lo == x) or (lo <= x < hi):
                return True
        return False

    def _and(self, row):
        for ranges in self.parts.values():
            if not self._or(ranges, row):
                return False
        return True

    def selects(self, rows):
        selected = []
        for r in rows:
            if self._and(r):
                # print("Hi")
                selected.append(r)
        return selected

    def selectss(self, rowss):
        result = {}
        for y, rows in rowss.items():
            result[y] = len(self.selects(rows))
        return result

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
    
    def show(self,ands=None):
        if ands is None:
            ands = []
        # print(self.parts)
        # print(list(self.parts.values()))
        for ranges in self.parts.values():
            # print(ranges)
            ors = self._show_less(ranges)
            at = None
            # print("ors: ", ors)
            for i, range in enumerate(ors):
                # print(type(range))
                at = range.at
                ors[i] = range.show()
                # print(ors)
            ands.append(" or ".join(ors))
        return " and ".join(ands)
      
