from num import NUM
from sym import SYM
from data import Data
from learn import learn
import random, math
from util import Utility

class TestSuite:
    def __init__(self, the) -> None:
        self.the = the
        self.util = Utility()

        self.all = [self.test_sym_1, self.test_sym_2, self.test_sym_3, self.test_num_1, self.test_num_2, self.test_num_3]
        self.num = [self.test_num_1, self.test_num_2, self.test_num_3]
        self.sym = [self.test_sym_1, self.test_sym_2, self.test_sym_3]

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

        d = Data(self.the, "../data/auto93.csv")

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

    def run_num_tests(self):
        for test in self.num:
            test()

    def run_sym_tests(self):
        for test in self.sym:
            test()

    def run_all_tests(self):
        for test in self.all:
            test()
