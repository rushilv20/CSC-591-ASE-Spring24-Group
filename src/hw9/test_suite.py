from sym import SYM 
from num import NUM 
from data import DATA
from range import RANGE
from learn import learn
from rule import RULE
from rules import RULES
from stats import SAMPLE, eg0
import copy
import stats
import re
import random
import math
from util import Utility
from datetime import datetime

class Tests():
    def __init__(self, the) -> None:
        ## Getting all the variables from the arguments.
        self.the = the
        self.util = Utility(the)
        
        self.all = [self.test_sym_1, self.test_sym_2, self.test_sym_3, self.test_num_1, self.test_num_2, self.test_num_3]
        self.num = [self.test_num_1, self.test_num_2, self.test_num_3]
        self.sym = [self.test_sym_1, self.test_sym_2, self.test_sym_3]
        pass
    
    ## Local Functions
    
    def _ranges(self, cols, rowss):
        t = []
        for col in cols:
            for range in self._ranges1(col, rowss):
                t.append(range)
        return t
    
    def _ranges1(self, col, rowss):
        out = {}
        nrows = 0
        for y, rows in rowss.items():
            nrows += len(rows)
            for row in rows:
                x = row.cells[col.at]
                if x != "?":
                    bin = col.bin(x)
                    if bin not in out:
                        out[bin] = RANGE(self.the, col.at, col.txt, x)
                    out[bin].add(x, y)
        out = list(out.values())
        out.sort(key=lambda a: a.x['lo'])
        return out if hasattr(col, 'has') else self._mergeds(out, nrows / self.the.bins)
    
    def _mergeds(self, ranges, tooFew):
        i, t = 0, []
        while i < len(ranges):
            a = ranges[i]
            if i < len(ranges) - 1:
                both = a.merged(ranges[i+1], tooFew)
                if both:
                    a = both
                    i += 1
            t.append(a)
            i += 1
        if len(t) < len(ranges):
            return self._mergeds(t, tooFew)
        for i in range(1, len(t)):
            t[i].x['lo'] = t[i-1].x['hi']
        t[0].x['lo'] = -math.inf
        t[-1].x['hi'] = math.inf
        return t
    
    ## Test Cases
    def reset_to_default_seed(self):
        random.seed(self.the.seed)
    
    def test_sym_1(self):
        s = SYM(self.the)
        for x in [4, 4, 3, 3, 5, 3, 3]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("Python SYM Test1 Passed:", 1.37 < e < 1.38 and mode == 3) 
        print("   - Values Calulated: ", mode, e)

    def test_sym_2(self):
        s = SYM(self.the)
        for x in [1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("Python SYM Test2 Passed:", 2.20 < e < 2.25 and mode == 2)
        print("   - Values Calulated: ", mode, e)
        
    def test_sym_3(self):
        s = SYM(self.the)
        for x in [1, 2, 2, 2, 3, 3, 1, 3, 3, 1]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("Python SYM Test2 Passed:", 1.47 < e < 1.65 and mode == 3)
        print("   - Values Calulated: ", mode, e)

    def test_num_1(self):
        e = NUM(self.the)
        for _ in range(1000):
            e.add(random.normalvariate(5, 1))
        mu, sd = e.mid(), e.div()
        print("Python NUM Test1 Passed:", 4.7 < mu < 5.1 and 1 < sd < 1.05)
        print("   - Values Calulated: ", round(mu, 3), round(sd, 3))

    def test_num_2(self):
        e = NUM(self.the)
        for _ in range(1000):
            e.add(random.normalvariate(15, 3))
        mu, sd = e.mid(), e.div()
        print("Python NUM Test2 Passed:", 14.7 < mu < 15.2 and 2.9 < sd < 3.05)
        print("   - Values Calulated: ", round(mu, 3), round(sd, 3))
    
    def test_num_3(self):
        e = NUM(self.the)
        for _ in range(1000):
            e.add(random.normalvariate(10, 2))
        mu, sd = e.mid(), e.div()
        print("Python NUM Test2 Passed:", 9.8 < mu < 10.2 and 1.9 < sd < 2.4)
        print("   - Values Calulated: ", round(mu, 3), round(sd, 3))
    
    def test_eg_stats(self):
        data = DATA(self.the, "../data/auto93.csv")
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
        data = DATA(self.the, self.the.file, lambda data, t: learn(data, t, wme, self.the))
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
                data = DATA(self.the, "../data/soybean.csv", lambda data, t: learn(data, t, wme, self.the))
                print("%5.2f\t%s\t%s" % (wme['acc'] / wme['tries'], k, m))
        
    def test_gate(self):
        self.reset_to_default_seed()
        budget0 = 4
        budget = 10
        some = 0.5

        d = DATA(self.the, "../data/auto93.csv")

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

    def test_gate20(self):
        debug = False

        budget0 = 4
        budget = 10
        some = 0.5
        # A list that store the output of each steps
        output_message_list = [[] for _ in range(6)]

        test_case_n = 20
        for _ in range(test_case_n):
            seed_value = random.randint(0, 100000)
            random.seed(seed_value)

            if debug:
                print("seed = {0}".format(seed_value))

            d = DATA(self.the, "../data/auto93.csv")
            d.rows = self.util.shuffle(d.rows)

            # Step 1: Top 6
            top_count_n = 6
            top6_row_y_data = []
            for row_data in d.rows[:top_count_n]:
                y_data = []
                for y_field in d.cols.y:
                    y_data.append(row_data.cells[y_field.at])
                top6_row_y_data.append(y_data)
            output_message = "1. top6 {0}".format(top6_row_y_data)
            output_message_list[0].append(output_message)

            # Step 2: Top 50
            top_count_n = 50
            top50_row_y_data = []
            for row_data in d.rows[:top_count_n]:
                y_data = []
                for y_field in d.cols.y:
                    y_data.append(row_data.cells[y_field.at])
                top50_row_y_data.append(y_data)
            output_message = "2. top50 {0}".format(top50_row_y_data)
            output_message_list[1].append(output_message)


            # Step 3: Most
            d.rows.sort(key=lambda a: a.d2h(d))
            most_result = []
            for y_field in d.cols.y:
                most_result.append(d.rows[0].cells[y_field.at])
            output_message_list[2].append("3. most: {0}".format(most_result))

            d.rows = self.util.shuffle(d.rows)
            lite = self.util.slice(d.rows, 0, budget0)
            dark = self.util.slice(d.rows, budget0 + 1)

            stats = []
            bests = []
            for i in range(budget):
                best, rest = d.bestRest(lite, len(lite)**some)
                todo, selected = d.split(best, rest, lite, dark)
                stats.append(selected.mid())
                bests.append(best.rows[0])

                random_d = DATA(self.the, [d.cols.names])
                for row in random.sample(dark, budget0 + 1):
                    random_d.add(row)

                # Step 4
                random_result = []
                for y_field in d.cols.y:
                    rounded_number = round(random_d.mid().cells[y_field.at], 2)
                    random_result.append(rounded_number)
                output_message_list[3].append("4. rand: {0}".format(random_result))


                # Step 5
                mid_result = []
                for y_field in d.cols.y:
                    rounded_number = round(selected.mid().cells[y_field.at], 2)
                    mid_result.append(rounded_number)
                output_message_list[4].append("5. mid: {0}".format(mid_result))


                # Step 6
                top_result = []
                for y_field in d.cols.y:
                    rounded_number = round(best.rows[0].cells[y_field.at], 2)
                    top_result.append(rounded_number)
                output_message_list[5].append("6. top: {0}".format(top_result))

                lite.append(dark.pop(todo))

        # Sort output message
        for step in range(6):
            output_message_list[step].sort()
            for line in output_message_list[step]:
                print("{0}".format(line))
            print("")

    def test_dist(self):
        d = DATA(self.the, "../data/auto93.csv")
        r1 = d.rows[0]  # In Python, indices start from 0
        rows = r1.neighbors(d)
        for i, row in enumerate(rows):
            if i % 30 == 0:
                print(i + 1, "     ", str(row.cells), "     ", round(row.dist(r1, d), 2))

    def test_far(self):
        d = DATA(self.the, "../data/auto93.csv")
        a, b, C, _ = d.farapart(d.rows)
        print(str(a.cells), str(b.cells), round(C, 2))
        print("far1: ", str(a.cells))
        print("far2: ", str(b.cells))
        print("distance = ", C)

    def test_half(self):
        self.reset_to_default_seed()
        print("seed = {0}".format(self.the.seed))

        d = DATA(self.the, "../data/auto93.csv")
        sortp, above = None, None
        lefts, rights, left, right, C, cut, evals = d.half(d.rows, sortp, above)
        print("|lefts| = {0}".format(len(lefts)))
        print("|rights| = {0}".format(len(rights)))
        print("lefts: {0}".format(str(left.cells)))
        print("rights: {0}".format(str(right.cells)))
        print("C = {0}".format(C))
        print("cut = {0}".format(cut))

    def test_tree(self):
        self.reset_to_default_seed()
        d = DATA(self.the, "../data/auto93.csv")
        tree, evals = d.tree(True)
        tree.show()
        print("evals: {0}".format(evals))

    def test_branch(self):
        self.reset_to_default_seed()
        d = DATA(self.the, "../data/auto93.csv")
        best, rest, evals = d.branch()
        best_data = [round(cell, 2) for cell in best.mid().cells]
        print("Best: {0}".format(best_data))
        rest_data = [round(cell, 2) for cell in rest.mid().cells]
        print("Rest: {0}".format(rest_data))
        print("evals: {0}".format(evals))

    def test_doubletap(self):
        self.reset_to_default_seed()
        d = DATA(self.the, "../data/auto93.csv")
        best1, rest, evals1 = d.branch(32)
        best2, _, evals2 = best1.branch(4)

        best_data = [round(cell, 2) for cell in best2.mid().cells]
        mid_data = [round(cell, 2) for cell in rest.mid().cells]
        print("{0}\t\t{1}".format(best_data, mid_data))
        print(evals1 + evals2)

    def test_detail(self):

        def format_value(value):
            if value == int(value):
                return f'{int(value)}'
            else:
                return f'{value:.2f}'.rstrip('0').rstrip('.')

        self.reset_to_default_seed()
        smo_repeat_time = 20
        self.the.file = "../data/auto93.csv"

        d = DATA(self.the, self.the.file)

        self.reset_to_default_seed()
        print("date : {0}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        print("file : {0}".format(self.the.file))
        print("repeats : {0}".format(smo_repeat_time))
        print("seed : {0}".format(self.the.seed))
        print("rows : {0}".format(len(d.rows)))
        print("cols : {0}".format(len(d.cols.names.cells)))

        titles = [str(cell) for cell in d.cols.names.cells]

        separator = '   '
        title_str = separator.join(f'{title:<10}' for title in titles)
        print(f"names                      \t{title_str}\tD2h-")

        # mid
        mid_values = [round(cell, 2) for cell in d.mid().cells]
        mid_values.append(d.mid().d2h(d))
        value_str = separator.join(f'{format_value(value):<10}' for value in mid_values)
        print(f"mid                        \t{value_str}")

        # div
        # Calculate the standard deviation of all d2h
        d2h_values = [row.d2h(d) for row in d.rows]
        mean = sum(d2h_values) / len(d2h_values)
        squared_diffs = [(x - mean) ** 2 for x in d2h_values]
        mean_squared_diff = sum(squared_diffs) / len(squared_diffs)
        standard_deviation = (mean_squared_diff) ** 0.5

        div_values = [round(cell, 2) for cell in d.div().cells]
        div_values.append(round(standard_deviation, 2))
        value_str = separator.join(f'{format_value(value):<10}' for value in div_values)
        print(f"div                        \t{value_str}")

        # smo with budget 9
        print("#")

        smo9_top_result = []

        budget0 = 4
        budget = 9
        some = 0.5
        for _ in range(smo_repeat_time):
            d.rows = self.util.shuffle(d.rows)

            lite = self.util.slice(d.rows, 0, budget0)
            dark = self.util.slice(d.rows, budget0 + 1)

            stats = []
            bests = []
            for i in range(budget):
                best, rest = d.bestRest(lite, len(lite)**some)
                todo, selected = d.split(best, rest, lite, dark)
                stats.append(selected.mid())
                bests.append(best.rows[0])

                lite.append(dark.pop(todo))

            top_result = [round(cell, 2) for cell in best.rows[0].cells]
            top_result.append(best.rows[0].d2h(d))

            mid_result = [round(cell, 2) for cell in selected.mid().cells]
            mid_result.append(selected.mid().d2h(d))

            smo9_top_result.append(top_result)

        smo9_top_result = sorted(smo9_top_result, key=lambda x: x[-1])

        for i in range(smo_repeat_time):
            value_str = separator.join(f'{format_value(value):<10}' for value in smo9_top_result[i])
            print(f"smo9                        \t{value_str}")

        # Random 50 
        print("#")
        random_50_result = []

        for _ in range(smo_repeat_time):
            d.rows = self.util.shuffle(d.rows)

            random_50_row = d.rows[:50]
            random_50_row.sort(key=lambda a: a.d2h(d))

            best_in_random_50_row = [round(cell, 2) for cell in random_50_row[0].cells]
            best_in_random_50_row.append(random_50_row[0].d2h(d))

            random_50_result.append(best_in_random_50_row)

        random_50_result = sorted(random_50_result, key=lambda x: x[-1])
        for i in range(smo_repeat_time):
            value_str = separator.join(f'{format_value(value):<10}' for value in random_50_result[i])
            print(f"any50                        \t{value_str}")

        # Ceiling: Absolute best result
        print("#")
        d.rows.sort(key=lambda a: a.d2h(d))

        absolute_best_result = [round(cell, 2) for cell in d.rows[0].cells]
        absolute_best_result.append(d.rows[0].d2h(d))
        value_str = separator.join(f'{format_value(value):<10}' for value in absolute_best_result)
        print(f"100%                        \t{value_str}")

    """
    bonr:
         using the acquire function you've been using all along ((b+r)/(b-r))

    RandN:
         20 times, pull 90% of the data, sort by d2h, then report the top one.
    """


    def _get_best_d2h_with_rand(self, data, n):
        tmp_rows = copy.deepcopy(data.rows)
        random.shuffle(tmp_rows)
        top_n_rows = tmp_rows[:n]
        sorted_d2h_list = [row.d2h(data) for row in top_n_rows]
        sorted_d2h_list.sort()
        return sorted_d2h_list[0]

    def test_stats(self):
        self.reset_to_default_seed()
        smo_repeat_time = 20
        self.the.file = "../data/auto93.csv"

        d = DATA(self.the, self.the.file)

        print("date : {0}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        print("file : {0}".format(self.the.file))
        print("repeats : {0}".format(smo_repeat_time))
        print("seed : {0}".format(self.the.seed))
        print("rows : {0}".format(len(d.rows)))
        print("cols : {0}".format(len(d.cols.names.cells)))

        # Best
        sorted_d = sorted(d.rows, key=lambda a: a.d2h(d))
        print("best : {0}".format(round(sorted_d[0].d2h(d), 2)))

        # Tiny
        d2h_values = [row.d2h(d) for row in d.rows]
        mean = sum(d2h_values) / len(d2h_values)
        squared_diffs = [(x - mean) ** 2 for x in d2h_values]
        mean_squared_diff = sum(squared_diffs) / len(squared_diffs)
        standard_deviation = (mean_squared_diff) ** 0.5
        tiny_value = 0.35 * standard_deviation
        print("tiny : {0}".format(round(tiny_value, 2)))

        test_case = ["base", "bonr9", "rand9", "bonr15", "rand15", "bonr20", "rand20", "rand358"]
        # test_case = ["base", "bonr9", "rand9", "bonr15", "rand15", "bonr20", "rand20", "rand358", "bonr30", "bonr40", "bonr50", "bonr60"]
        test_case_n = len(test_case)

        test_case_output = ' '.join(f"#{item}" for item in test_case)
        print(test_case_output)
        print("#report{0}".format(test_case_n))

        stat_dict = {}

        # Do base first
        d = DATA(self.the, self.the.file)
        d2h_list = [round(row.d2h(d), 2) for row in d.rows]
        stat_dict["base"] = d2h_list

        for _ in range(20):
            for test_type in test_case:
                if test_type.startswith("base"):
                    continue
                elif test_type.startswith("bonr"):
                    match = re.search(r'\d+', test_type)
                    if not match:
                        continue
                    total_budget = int(match.group())

                    d2h_list = stat_dict.get(test_type, [])

                    budget0 = 4
                    budget = total_budget - budget0
                    some = 0.5

                    d = DATA(self.the, self.the.file)
                    _, bests = d.gate(budget0, budget, some)
                    bests.sort(key=lambda a: a.d2h(d))
                    d2h_list.append(round(bests[0].d2h(d), 2))

                    stat_dict[test_type] = d2h_list
                elif test_type.startswith("rand"):
                    match = re.search(r'\d+', test_type)
                    if not match:
                        continue
                    budget = int(match.group())

                    d2h_list = stat_dict.get(test_type, [])

                    d = DATA(self.the, self.the.file)
                    best_d2h_in_random_rows = self._get_best_d2h_with_rand(d, budget)
                    d2h_list.append(round(best_d2h_in_random_rows, 2))
                    stat_dict[test_type] = d2h_list
                else:
                    # Unsupported type
                    continue

        slurp_list = []
        for key, item in stat_dict.items():
            slurp_list.append(stats.SAMPLE(item, key))
        eg0(slurp_list)

    # Running all the tests as per Class ##
    
    def test_bins(self):
        d = DATA(self.the, self.the.file)
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
            d = DATA(the.file)
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
        d = DATA(self.the, self.the.file)

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
        for i in self.num:
            i()
            
    def run_sym_tests(self):
        for i in self.sym:
            i()
    
    def run_all_tests(self):
        for i in self.all:
            i()
            
# test = Tests()
# print(test.test_eg_bayes())
# test.run_all_tests()
# test.test_eg_stats()