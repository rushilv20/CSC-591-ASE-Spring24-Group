import math
import re
import sys
import ast, fileinput, random

class Utility:
    def __init__(self):
        pass
    
    def csv(self, file="-"):
        with fileinput.input (None if file=="-" else file) as src:
            for line in src: 
                #convert all the values to empty string
                line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)

                if line: 
                    yield [self.coerce(x) for x in line.split(",")]

    def coerce(self, s):
        try:
            return ast.literal_eval(s)
        except Exception: return s.strip() #when s is already a string


    def round(n, ndecs=None):
        if type(n) == str:
            return n
        if math.floor(n) == n:
            return n
        mul = 10**(ndecs or 2)
        return math.floor(n * mul + 0.5) / mul

    def shuffle(t):
        u = t[:]
        random.shuffle(u)
        return u
    
    def slice(self, t, go=None, stop=None, inc=None):
        if go is not None and go < 0:
            go = len(t) + go
        if stop is not None and stop < 0:
            stop = len(t) + stop

        u = []

        if go is None:
            go = 0
        if stop is None:
            stop = len(t)
        if inc is None:
            inc = 1

        for j in range(go, stop, inc):
            u.append(t[j])

        return u
    
    def many(t, n=None):
        n = n or len(t)
        return [any(t) for _ in range(n)]
    #sorted keys
    
    def copy(self,t):
        if type(t) != dict and type(t) != list:
            return t

        u = {}
        for k, v in t.items() if isinstance(t, dict) else enumerate(t):
            u[self.copy(k)] = self.copy(v)

        return u
    
    def entropy(t):
        n = sum(t.values())
        e = 0
        for v in t.values():
            e -= (v / n) * math.log2(v / n)
        
        return e, n
    
    def any_item(t):
        return random.choice(t)

    def score(t, goal, LIKE, HATE, the):
        like, hate, tiny = 0, 0, 1E-30
        # print(t.items())
        for klass, n in t.items():
            if klass == goal:
                like += n
            else:
                hate += n
        like = like / (LIKE + tiny)
        hate = hate / (HATE + tiny)
        if hate > like:
            return 0
        else:
            return (like ** the['Support']) / (like + hate)
    
    def powerset(s):
        
        t = [[]]
        for i in range(len(s)):
            for j in range(len(t)):
                t.append([s[i]] + t[j])
        
        return t