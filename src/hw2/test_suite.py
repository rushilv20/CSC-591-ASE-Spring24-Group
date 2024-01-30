from num import NUM
from sym import SYM
from data import Data

import random

class TestSuite:
    def __init__(self) -> None:
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

    # def test_eg_stats(self):
    #     data = Data(self.the, "../../data/auto93.csv")
    #     stats_result = data.stats()
    #     expected_result = "{'.N': 398, 'Lbs-': 2970.42, 'Acc+': 15.57, 'Mpg+': 23.84}"
    #     print("Actual Result:", str(stats_result))
    #     print("Expected Result:", expected_result)
        
    #     if str(stats_result) == expected_result:
    #         print("Test Passed!")
    #     else:
    #         print("Test Failed!")

    def run_num_tests(self):
        for test in self.num:
            test()

    def run_sym_tests(self):
        for test in self.sym:
            test()

    def run_all_tests(self):
        for test in self.all:
            test()
