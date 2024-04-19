from Utility import Utility
from rule import RULE as Rule
class RULES:
    def __init__(self, ranges, goal, rowss, the):
        self.goal = goal
        self.util = Utility(the)
        self.the = the
        self.rowss = rowss
        self.LIKE = 0
        self.HATE = 0
        self.sorted = []
        self.likeHate()
        for range_ in ranges:
            range_.scored = self.score(range_.y)
        self.sorted = self.top(self.func_try(self.top(ranges)))

    def likeHate(self):
        for y, rows in self.rowss.items():
            if y == self.goal:
                self.LIKE += len(rows)
            else:
                self.HATE += len(rows)

    def score(self, t):
        return self.util.score(t, self.goal, self.LIKE, self.HATE)
    
    def func_try(self,ranges):
        u = []
        for subset in self.util.powerset(ranges):
            if len(subset) > 0:
                rule = Rule.RULE(subset,self.the)
                rule.scored = self.score(rule.selectss(self.rowss))
                if rule.scored > 0.01:
                    u.append(rule)
        return u
    
    def top(self, t):
        t.sort(key=lambda x: x.scored, reverse=True)
        u = []
        # print("Cut = ", self.the.Cut)
        for x in t:
            # print(x.scored)
            # print(t[0].scored)
            if float(x.scored) >= float(t[0].scored) * float(self.the.Cut):
                u.append(x)
        return u[:self.the.Beam]
