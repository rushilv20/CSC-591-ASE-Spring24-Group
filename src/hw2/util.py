import math
import re
import sys


def coerce(s1):
    def fun(s2):
        if s2 == "nil":
            return None
        else:
            return s2.lower() == "true" or (s2.lower() != "false" and s2)
    try:
        return float(s1)
    except:
        return fun(re.match(r'^\s*(.*\S)', s1).group(1))

def cells(s):
    return [coerce(s1) for s1 in re.findall("([^,]+)", s)]

#other one, recheck with Siddhi
def cells(s):
    t = []
    for s1 in s.split(","):
        t.append(coerce(s1))
    return t

def csv(src):
    i, src = 0, src if src == "-" else open(src)

    def read_line():
        nonlocal i
        s = src.readline()
        if s:
            i += 1
            return i, cells(s)
        else:
            src.close()

    return read_line

def settings(s):
    t = {}
    dir = {}
    options = re.findall(r'-(\w+)\s+--(\w+)\s+.*=\s*(\S+)', s)
    
    for option in options:
        short_form, full_form, default_value = option
        t[full_form] = coerce(default_value)
        dir[short_form] = full_form
    
    return [t, dir]

def rounded(n, ndecs=None):
    if type(n) == str:
        return n
    if math.floor(n) == n:
        return n
    mul = 10**(ndecs or 2)
    return math.floor(n * mul + 0.5) / mul

def cli(t, opt_dir):
    options = sys.argv[1:]
    opt_dict = {}

    if("--help" in options or "-h" in options):
        t["help"]=True
        return t

    for i in range(0, len(options), 2):
        opt_dict[options[i]] = options[i+1]

    for opt,val in opt_dict.items():
        if opt.startswith('--'):
            t[opt[2:]] = coerce(val)
        elif opt.startswith('-'):
            t[opt_dir[opt[1:]]] = coerce(val)

    return t