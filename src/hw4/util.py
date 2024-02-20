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
            
def do_file(file):
    # if local X = y is present, find both the thing to replace and what to replace it with
    data = None
    with open(file, "r") as fp:
        data = fp.read()
    vars = re.match("local (.*) = (.*)\n", data)
    if vars:
        variable, value = vars.groups()
        data = data.replace(variable, value)
        data = re.sub("local .* = .*\n", "", data)
    # remove the return statement
    data = data.replace("return ", "")
    # remove newlines
    data = data.replace("\n", "")
    # replace domain= , cols= , rows=
    # change X=y to "X":y
    terms = ["domain", "cols", "rows"]
    for term in terms:
        data = re.sub("{}\s*=".format(term), '"{}":'.format(term), data)
    # replace { } with [ ]
    first, last = data.index("{"), data.rindex("}")
    data = data[first + 1:last].replace("{", "[").replace("}", "]")
    data = "{" + data + "}"

    # replace ' with "
    data = data.replace("'", '"')
    json_obj = json.loads(data)
    return json_obj


def oo(t):
    td = t.__dict__
    td['a'] = t.__class__.__name__
    td['id'] = id(t)
    print(dict(sorted(td.items())))


def last(t):
    return t[-1]


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

def keys(self, t):
    u = [k for k in t]
    u.sort()
    return u

def many(self, t, n):
    n = n or len(t)
    return [random.choice(t) for _ in range(n)]

def keysort(self, t, fun):
    u = [{'x': x, 'y': fun(x)} for x in t]
    u.sort(key=lambda a: a['y'])
    v = [xy['x'] for xy in u]
    return v




