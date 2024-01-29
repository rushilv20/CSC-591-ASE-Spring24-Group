import math
import re
import sys
import ast, fileinput, random

class Utility:
    def __init__(self):
        pass
    
    def csv(self, file="-"):
        with file.FileInput (None if file=="-" else file) as src:
            for line in src: 
                #convert all the values to empty string
                line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)

                if line: 
                    yield [self.coerce(x) for x in line.split(",")]

    def coerce(self, s):
        try:
            return ast.literal_eval(s)
        except Exception: return s.strip() #when s is already a string


    def rounded(n, ndecs=None):
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