import math


class ROW:
    def __init__(self, the, cells):
        self.cells = cells
        self.the = the

    def d2h(self, data,d,n):
        d, n = 0, 0
        for col in data.cols.y:
            n += 1
            d += abs(col.heaven - col.norm(self.cells[col.at])) ** 2
        return (d ** 0.5) / (n ** 0.5)



    # def likes(self, datas):
    #     n, nHypotheses = 0, 0
    #     for data in datas:
    #         n += len(data.rows)
    #         nHypotheses += 1

    #     most, out = None, None
    #     for k, data in enumerate(datas):
    #         tmp = self.like(data, n, nHypotheses)
    #         if most is None or tmp > most:
    #             most, out = tmp, k
    #     return out, most

    # def like(self, data, n, nHypotheses):
    #     prior = (len(data.rows) + the.k) / (n + the.k * nHypotheses)
    #     out = math.log(prior)

    #     for col in data.cols.x:
    #         v = self.cells[col.at]
    #         if v != "?":
    #             inc = col.like(v, prior)
    #             out += math.log(inc)

    #     return math.exp(1) ** out
