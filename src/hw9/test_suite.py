from num import NUM
from sym import SYM
from data import Data
from learn import learn
import random, math
from util import Utility
import re,stats,copy
from rule import RULE
from rules import RULES
from range import RANGE
from datetime import datetime

class TestSuite:
    def __init__(self, the) -> None:
        self.the = the
        self.util = Utility()

        self.all = [self.test_sym_1, self.test_sym_2, self.test_sym_3, self.test_num_1, self.test_num_2, self.test_num_3]
        self.num = [self.test_num_1, self.test_num_2, self.test_num_3]
        self.sym = [self.test_sym_1, self.test_sym_2, self.test_sym_3]

    def ranges(self, cols,rowss):
        t=[]
        for col in cols:
            for range in self.ranges1(col,rowss):
                t.append(range)
        return t
    def ranges1(self, col,rowss):
        out={}
        nrows=0
        for y,rows in rowss.items():
            nrows+=len(rows)
            for row in rows:
                x=row.cells[col.at]
                if x!="?":
                    bin=col.bin(x)
                    if bin not in out:
                        out[bin]=RANGE(self.the,col.at,col.txt,x)
                    out[bin].add(x)
        out=list(out.values())
        out.sort(key=lambda a:a.x['lo'])
        return out if hasattr(col,'has') else self.mergeds(out,nrows/self.the.bins)

    def mergeds(self, ranges, tooFew):
        i,t=0,[]
        while i<len(ranges):
            b=ranges[i]
            if i<len(ranges)-1:
                both=b.merged(ranges[i+1],tooFew)
                if both:
                    i+=1
                    b=both
            t.append(b)
            i+=1
        if len(t)<len(ranges):
            return self.mergeds(t,tooFew)
        for i in range(1,len(t)):
            t[i].x['lo']=t[i-1].x['hi']
        t[0].x['lo']=-math.inf
        t[-1].x['hi']=math.inf
        return t

    def reset_to_default_seed(self):
        random.seed(self.the.seed)  # Resetting the seed to default value
        

    def test_sym_1(self):
        s = SYM()
        for x in [1, 2, 2, 2, 3, 3, 1, 3, 3, 1]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("SYM Test 3 Passed:", 1.47 < e < 1.65 and mode == 3)
        print("   - Values Calculated: ", mode, e)

    def test_sym_2(self):
        s = SYM()
        for x in [1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("SYM Test 2 Passed:", 2.20 < e < 2.25 and mode == 2)
        print("   - Values Calculated: ", mode, e)

    def test_sym_3(self):
        s = SYM()
        for x in [4, 4, 3, 3, 5, 3, 3]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("SYM Test 1 Passed:", 1.37 < e < 1.38 and mode == 3)
        print("   - Values Calculated: ", mode, e)
        
    def test_num_1(self):
        e = NUM()
        for _ in range(1000):
            e.add(random.normalvariate(15, 3))
        mu, sd = e.mid(), e.div()
        print("NUM Test 2 Passed:", 14.7 < mu < 15.2 and 2.9 < sd < 3.05)
        print("   - Values Calculated: ", round(mu, 3), round(sd, 3))
    
    def test_num_2(self):
        e = NUM()
        for _ in range(1000):
            e.add(random.normalvariate(5, 1))
        mu, sd = e.mid(), e.div()
        print("NUM Test 1 Passed:", 4.7 < mu < 5.1 and 1 < sd < 1.05)
        print("   - Values Calculated: ", round(mu, 3), round(sd, 3))


    def test_num_3(self):
        e = NUM()
        for _ in range(1000):
            e.add(random.normalvariate(10, 2))
        mu, sd = e.mid(), e.div()
        print("NUM Test 3 Passed:", 9.8 < mu < 10.2 and 1.9 < sd < 2.4)
        print("   - Values Calculated: ", round(mu, 3), round(sd, 3))

    def test_eg_stats(self):
        data = Data(self.the, "../../data/auto93.csv")
        stats_result = data.stats()
        expected_result = "{'.N': 398, 'Lbs-': 2970.42, 'Acc+': 15.57, 'Mpg+': 23.84}"
        print("Actual Result:", str(stats_result))
        print("Expected Result:", expected_result)
        
        if str(stats_result) == expected_result:
            print("Test Passed!")
        else:
            print("Test Failed!")
        
    def test_eg_bayes(self):
        wme = {'acc': 0, 'datas': [], 'tries': 0, 'n': 0}
        data = Data(self.the, self.the.file, lambda data, t: learn(data, t, wme, self.the))
        print("File Used :", self.the.file)
        print("Accurary :", wme['acc'] / wme['tries'] * 100, "%")
        return wme['acc'] / wme['tries'] > 0.72

    def test_km(self):
        print("#%4s\t%s\t%s" % ("acc", "k", "m"))
        
        for k in range(4):
            for m in range(4):
                self.the.k = k
                self.the.m = m
                wme = {'acc': 0, 'datas': {}, 'tries': 0, 'n': 0}
                data = Data(self.the, "../data/soybean.csv", lambda data, t: learn(data, t, wme, self.the))
                print("%5.2f\t%s\t%s" % (wme['acc'] / wme['tries'], k, m))

    def test_gate(self):
        self.reset_to_default_seed()
        budget0 = 4
        budget = 10
        some = 0.5

        d = Data(self.the, "../../data/auto93.csv")

        def sayd(row, txt):
            distance_to_heaven = self.util.rnd(row.d2h(d))
            print("{0} {1} {2}".format(str(row.cells), txt, distance_to_heaven))

        def say(row, txt):
            print("{0} {1}".format(str(row.cells), txt))

        print("{0} {1} {2}".format(str(d.cols.names.cells), "about", "d2h"))
        print("#overall")
        sayd(d.mid(), "mid")
        say(d.div(), "div")
        say(d.small(), "small=div*" + str(self.the.cohen))

        print("#generality")
        # print(d.rows)
        stats, bests = d.gate(budget0, budget, some)
        for index, stat in enumerate(stats):
            sayd(stat, index + budget0)

        print("#specifically")
        for index, best in enumerate(bests):
            sayd(best, index + budget0)

        print("#optimum")
        d.rows.sort(key=lambda a: a.d2h(d))
        sayd(d.rows[0], len(d.rows))

        print("#random")
        random_rows = self.util.shuffle(d.rows)
        print(len(random_rows), int(math.log(0.05) / math.log(1 - self.the.cohen / 6)))
        random_rows = self.util.slice(random_rows, 1, int(math.log(0.05) / math.log(1 - self.the.cohen / 6)))
        random_rows.sort(key=lambda a: a.d2h(d))
        sayd(random_rows[0], None)

    def test_dist(self):
        d=Data(self.the,"../../Data/auto93.csv")
        row1=d.rows[0]
        rows=row1.neighbor(d)
        # print("Row 1: ", row1.cells)
        for i,row in enumerate(rows):
            if i%30==0:
                print(i + 1, "     ", str(row.cells), "     ", round(row.dist(row1, d), 2))

    def test_far(self):
        d=Data(self.the,"../../Data/auto93.csv")
        a,b,C,e=d.farapart(d.rows)
        print(str(a.cells), str(b.cells), round(C, 2))
        print("far1: ", str(a.cells))
        print("far2: ", str(b.cells))
        print("distance = ", C)

    def test_half(self):
        self.reset_to_default_seed()
        print("seed = {0}".format(self.the.seed))

        d = Data(self.the, "../data/auto93.csv")
        sortp, above = None, None
        lefts, rights, left, right, C, cut, e = d.half(d.rows, sortp, above)
        print("|lefts| = {0}".format(len(lefts)))
        print("|rights| = {0}".format(len(rights)))
        print("lefts: {0}".format(str(left.cells)))
        print("rights: {0}".format(str(right.cells)))
        print("C = {0}".format(C))
        print("cut = {0}".format(cut))

    def test_branch(self):
        self.reset_to_default_seed()
        d = Data(self.the, "../data/auto93.csv")
        best, rest, e = d.branch()
        best_data = [round(cell, 2) for cell in best.mid().cells]
        print("Best: {0}".format(best_data))
        rest_data = [round(cell, 2) for cell in rest.mid().cells]
        print("Rest: {0}".format(rest_data))
        print("evals: {0}".format(e))
    
    def test_doubletap(self):
        self.reset_to_default_seed()
        d = Data(self.the, "../data/auto93.csv")
        best1, rest, evals1 = d.branch(32)
        best2, _, evals2 = best1.branch(4)

        best_data = [round(cell, 2) for cell in best2.mid().cells]
        mid_data = [round(cell, 2) for cell in rest.mid().cells]
        print("{0}\t\t{1}".format(best_data, mid_data))
        print(evals1 + evals2)

    def test_bins(self):
        d = Data(self.the, self.the.file)
        best, rest, evals = d.branch()
        LIKE = best.rows
        HATE = rest.rows[:3 * len(LIKE)]
        self.util.shuffle(HATE)

        def score(range):
            return range.score("LIKE", len(LIKE), len(HATE))

        t = []
        print("OUTPUT 1:")
        for col in d.cols.x:
            print("")
            for range in self._ranges1(col, {"LIKE": LIKE, "HATE": HATE}):
                print(str(range))
                t.append(range)

        t.sort(key=score, reverse=True)
        max_score = score(t[0])

        print("\nOUTPUT 2:")
        print("\n#scores:\n")
        for v in t[:self.the.Beam]:
            if score(v) > max_score * .1:
                print(self.util.rnd(score(v)), v)

        print({"LIKE": len(LIKE), "HATE": len(HATE)})

    def test_rules(d, rowss, the, self):
        print("inside rules")
        for xxx in range(1):
            d = Data(the.file)
            best0, rest, evals1 = d.branch(the.d)
            best, _, evals2 = best0.branch(the.D)
            print(evals1 + evals2 + the.D - 1)
            LIKE = best.rows
            HATE = Utility.slice(Utility.shuffle(rest.rows), 0, 3 * len(LIKE))
            rowss = {'LIKE': LIKE, 'HATE': HATE}
            rules_object = RULES(self._ranges(d.cols.x, rowss), "LIKE", rowss)
            sorted_rules = sorted(rules_object.sorted, key=lambda rule: rule.scored)
            for i, rule in enumerate(sorted_rules):
                result = d.clone(rule.selects(rest.rows))
                if len(result.rows) > 0:
                    result.rows.sort(key=lambda row: row.d2h(d))
                    print(
                        Utility.rnd(rule.scored),
                        Utility.rnd(result.mid().d2h(d)),
                        Utility.rnd(result.rows[0].d2h(d)),
                        Utility.l_o(result.mid().cells),
                        "\t",
                        rule.show()
                    )

    def test_rules2(self):
        #print("inside rules2")
        d = Data(self.the, self.the.file)

        tmp = self.util.shuffle(d.rows)
        train = d.clone(self.util.slice(tmp, 0, len(tmp) // 2))
        test = d.clone(self.util.slice(tmp, len(tmp) // 2, len(tmp)))
        test.rows.sort(key=lambda row: row.d2h(d))
        print("base ", self.util.rnd(test.mid().d2h(d)), self.util.rnd(test.rows[0].d2h(d)), "\n")
        test.rows = self.util.shuffle(test.rows)

        best0, rest, evals1 = train.branch(self.the.d)
        best, _, evals2 = best0.branch(self.the.D)
        print(evals1+evals2+ self.the.D-1)

        LIKE = best.rows
        HATE = self.util.slice(self.util.shuffle(rest.rows), 0, 3 * len(LIKE))
        print("LIKE " ,len(LIKE))
        print("HATE ",len(HATE))
        rowss = {'LIKE': LIKE, 'HATE': HATE}

        test.rows = self.util.shuffle(test.rows)
        #print(test.rows)
        #print(Utility.slice(test.rows, 0, evals1 + evals2 + self.the.D - 1))
        random = test.clone(self.util.slice(test.rows, 0, evals1 + evals2 + self.the.D - 1))
        random.rows.sort(key=lambda row: row.d2h(d))

        print("Score"+"\t\t\t"+"Mid Selected"+"\t\t\t\t\t\t\t"+"Rule")
        print("-----"+"\t\t\t"+"------------"+"\t\t\t\t\t\t\t"+"------")
        for i, rule in enumerate(RULES(self._ranges(train.cols.x, rowss), "LIKE", rowss, self.the).sorted):
            result = train.clone(rule.selects(test.rows))
            if len(result.rows) > 0:
                result.rows.sort(key=lambda row: row.d2h(d))
                #print(result.mid().cells)
                rounded_cells = [round(value, 2) for value in result.mid().cells]
                print(
                    self.util.rnd(rule.scored),"\t",
                    # self.util.rnd(result.mid().d2h(d)),"\t",
                    # self.util.rnd(result.rows[0].d2h(d)), "\t",
                    # self.util.rnd(random.mid().d2h(d)), "\t",
                    # self.util.rnd(random.rows[0].d2h(d)),"\t",
                    self.util.rnd(rounded_cells),
                    "\t\t\t",
                    rule.show()
                )


    def run_num_tests(self):
        for test in self.num:
            test()

    def run_sym_tests(self):
        for test in self.sym:
            test()

    def run_all_tests(self):
        for test in self.all:
            test()
