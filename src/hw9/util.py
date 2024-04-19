# ----------------------------------------------------------------------------
# Utility Class for helper functions such as csv reader, etc.
import ast
import re, fileinput
import math, random

#for mylo.py
DEFAULT_bins_VALUE= 16
DEFAULT_Beam_VALUE = 10
DEFAULT_CUT_VALUE = 0.1
DEFAULT_d_VALUE = 32
DEFAULT_D_VALUE = 4
DEFAULT_F_VALUE = 0.95
DEFAULT_Half_VALUE = 256
DEFAULT_p_VALUE = 2
DEFAULT_S_VALUE = 2


#for gate.py
DEFAULT_COHEN_VALUE = 0.35  # small effect size
DEFAULT_K_VALUE = 1  # low class frequency kludge
DEFAULT_M_VALUE = 2  # low attribute frequency kludge
DEFAULT_RANDOM_SEED = 31210  # random number seed


class Utility:
    def __init__(self, the=None) -> None:
        self.the = the
        pass

    def l_csv(self, file="-"):
        with fileinput.FileInput(None if file == "-" else file) as src:
            for line in src:
                # This regex replaces all the characters in bracket and words starting with #. with an empty string.
                line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
                # Then we feed the commma seperated data values to coerce for type conversion.
                if line: yield [self.l_coerce(x) for x in line.split(",")]

    def l_coerce(self, x):
        # literal_eval will convert the string to appropriate data type and the exception is when x is a string.
        try: return ast.literal_eval(x)
        except Exception: return x.strip()

    def rnd(self, n, ndecs=None):
        if not isinstance(n, (int, float)):
            return n
        if n.is_integer():
            return n
        mult = 10 ** (ndecs or 2)
        rounded_n = round(n * mult) / mult
        return round(rounded_n, 2)

    def shuffle(self, t):
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
    
    def many(self, t, n):
        n = n or len(t)
        return [random.choice(t) for _ in range(n)]

    def keysort(self, t, fun):
        u = [{'x': x, 'y': fun(x)} for x in t]
        u.sort(key=lambda a: a['y'])
        v = [xy['x'] for xy in u]
        return v

    def entropy(self, t):
        n = sum(t.values())
        e = sum([-v/n * math.log(v/n, 2) for v in t.values()])
        return e, n
    
    def score(self, t, goal, LIKE, HATE):
        like, hate, tiny = 0, 0, 1E-30
        #print(t.items())
        for klass, n in t.items():
            #print(klass, n)
            if klass == goal:
                like += n
            else:
                hate += n
        like, hate = like / (LIKE + tiny), hate / (HATE + tiny)
        #print(like,hate)
        if hate > like:
            return 0
        else:
            return like ** self.the.Support / (like+ tiny + hate+tiny)
        
    def powerset(self, s):
        t = [[]]
        for i in range(len(s)):
            for j in range(len(t)):
                t.append([s[i]] + t[j])
        return t
    
    def l_o(t, self, n=None):
        if isinstance(t, (int, float)):
            return str(self.rnd(t, n))
        if not isinstance(t, dict) and not isinstance(t, list):
            return str(t)
        u = []
        for k, v in t.items() if isinstance(t, dict) else enumerate(t):
            if str(k)[0] != "_":
                u.append(self.l_o(v, n))
        return "{" + ", ".join(u) + "}"