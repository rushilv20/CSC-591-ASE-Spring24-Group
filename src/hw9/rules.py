from util import Utility
from rule import RULE

class RULES:
    def __init__(self, ranges, goal, rowss, the):
        self.sorted = []
        self.goal = goal
        self.rowss = rowss
        self.LIKE = 0
        self.HATE = 0
        
        self.the = the
        self.utility = Utility(the)
        self.likeHate()

        for range in ranges:
            range.scored = self.score(range.y)
        self.sorted = self.top(self._try(self.top(ranges)))

    def likeHate(self):
        for y, rows in self.rowss.items():
            if y == self.goal:
                self.LIKE += len(rows)
            else:
                self.HATE += len(rows)

    def score(self, t):
        return self.utility.score(t, self.goal, self.LIKE, self.HATE)

    def _try(self, ranges):
        u = []
        for subset in self.utility.powerset(ranges):
            if len(subset) > 0:
                rule = RULE(subset)
                rule.scored = self.score(rule.selectss(self.rowss))
                if rule.scored > 0.01:
                    u.append(rule)
        return u

    def top(self, t, the):
        t.sort(key=lambda x: x.scored, reverse=True)
        u = []
        for x in t:
            if float(x.scored) >= float(t[0].scored) * float(self.the.Cut):
                u.append(x)
        return u[:(self.the.Beam)]