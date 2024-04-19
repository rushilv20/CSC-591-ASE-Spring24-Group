import math
class ROW:
    def __init__(self, the, cells):
        self.cells = cells
        self.the = the
    
    #likes()
    def likes(self, datas):
        n, nHypotheses = 0, 0
        most = None
        for k, data in datas.items():
            n += len(data.rows)
            nHypotheses += 1
        for k, data in datas.items():
            tmp = self.like(data, n, nHypotheses)
            if most is None or tmp > most:
                most, out = tmp, k
        return out, most
    
    #like()

    def like(self, data, n, nHypotheses):
        prior = (len(data.rows) + self.the.k) / (n + self.the.k * nHypotheses)
        out = math.log(prior)
        for col in data.cols.x:
            v = self.cells[col.at]
            if v != "?":
                inc = col.like(v, prior)
                # print(inc)
                try:
                    out += math.log(inc)
                except ValueError:
                    return 0.0

        return math.exp(1) ** out

    """
    function ROW:d2h(data, d, n)
      d, n = 0, 0
      for _, col in pairs(data.cols.y) do
          n = n + 1
          d = d + math.abs(col.heaven - col:norm(self.cells[col.at])) ^ 2 end
      return d ^ .5 / n ^ .5 end
    """
    def d2h(self, data):
        d = 0
        n = 0
        for col in data.cols.y:
            n += 1
            d += abs(col.heaven - col.norm(self.cells[col.at])) ** 2
        return (d ** 0.5) / (n ** 0.5)
    
    # dist
    def dist(self, other, data):
        d, n, p = 0, 0, self.the.p
        for col in data.cols.x:
            # print(d, col.dist(self.cells[col.at], other.cells[col.at]) ** p )
            # print(col, self.cells[col.at], other.cells[col.at] )
            n += 1
            d += col.dist(self.cells[col.at], other.cells[col.at]) ** p
        return (d / n) ** (1 / p)

    # neighbors
    def neighbors(self, data, rows=None):
        return sorted(rows or data.rows, key=lambda row: self.dist(row, data))