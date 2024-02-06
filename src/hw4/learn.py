from data import Data

def learn(data, row, my, the):
    my['n'] += 1
    kl = row.cells[data.cols.klass.at]
    # print("Once", my['datas'])
    
    if my['n'] > 10:
        my['tries'] += 1
        if kl == row.likes(my['datas'])[0]:
           my['acc'] += 1
        else: my['acc'] = 0
    
    if not my['datas']:
        my['datas'] = {}
    
    my['datas'][kl] = my['datas'].get(kl, Data(the, [data.cols.names]))
    my['datas'][kl].add(row)

def bayes():
    wme = {'acc': 0, 'datas': [], 'tries': 0, 'n': 0}
    data = Data.new("../data/diabetes.csv")
    learn(data, lambda data, t: learn(data, t, wme))
    print(wme['acc'] / (wme['tries']))
    return wme['acc'] / (wme['tries']) > 0.72
