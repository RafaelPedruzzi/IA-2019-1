## -------------------------------------------------------- ##
#   Trab 1 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem         as bp
import hillClimbing       as hc
import beamSearch         as bs
import simulatedAnnealing as sa
import grasp              as gr
import genetic            as ge

from itertools import product, zip_longest
from time import time
import seaborn as sns
import matplotlib.pyplot as plt

# Train problems (T, [(vi,ti)])
TRAIN = [
    # P1
    (   19,
        [(1,3),(4,6),(5,7)]),
    # P3
    (   58,
        [(1,3),(4,6),(5,7),(3,4)]),
    # P4
    (   58,
        [(1,3),(4,6),(5,7),(3,4),(8,10),(4,8),(3,5),(6,9)]),
    # P6
    (   58,
        [(1,3),(4,6),(5,7),(3,4),(8,10),(4,8),(3,5),(6,9),(2,1)]),
    # P8
    (   120,
        [(1,2),(2,3),(4,5),(5,10),(14,15),(15,20),(24,25),(29,30),(50,50)]),
    # P9
    (   120,
        [(1,2),(2,3),(3,5),(7,10),(10,15),(13,20),(24,25),(29,30),(50,50)]),
    # P11
    (   120,
        [(24,25),(29,30),(50,50)]),
    # P14
    (   138,
        [(1,3),(4,6),(5,7),(3,4),(2,6),(2,3),(6,8),(1,2),(2,3),(3,5),(7,10),(10,15),(13,20),(24,25),(29,30),(50,50)]),
    # P17
    (   13890000,
        [(1,3),(4,6),(5,7),(3,4),(2,6),(2,3),(6,8),(1,2),(3,5),(7,10),(10,15),(13,20),(24,25),(29,37)]),
    # P20
    (   45678901,
        [(1,3),(4,6),(5,7),(3,4),(2,6),(1,2),(3,5),(7,10),(10,15),(13,20),(15,20)])
]

# Test problems (T, [(vi,ti)])
TEST = [
    # P2
    (   192,
        [(1,3),(4,6),(5,7)]),
    # P5
    (   287,
        [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10)]),
    # P7
    (   120,
        [(1,2),(2,3),(4,5),(5,10),(14,15),(13,20),(24,25),(29,30),(50,50)]),
    # P10
    (   1240,
        [(1,2),(2,3),(3,5),(7,10),(10,15),(13,20),(24,25),(29,30),(50,50)]),
    # P12
    (   104,
        [(25,26),(29,30),(49,50)]),
    # P13
    (   138,
        [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8)]),
    # P15
    (   13890,
        [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2), (2,3), (3,5), (7,10), (10,15), (13,20), (24,25),(29,30), (50,50)]),
    # P16
    (   13890,
        [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2),(3,5),(7,10),(10,15),(13,20),(24,25),(29,37)]),
    # P18
    (   190000,
        [(1,3),(4,6),(5,7)]),
    # P19
    (   4567,
        [(1,3),(4,6),(5,7),(3,4),(2,6),(1,2),(3,5),(7,10),(10,15),(13,20),(15,20)])
]

# Used metaheuristics
HNAMES = ['Hill Climbing','Beam Search','Simulated Annealing','GRASP','Genetic']

HEURISTICS = [
    # Hill Climbing
    (   'Hill Climbing',
        hc.hill_Climbing,
        [[]],),
    # Beam Search
    (   'Beam Search',
        bs.beam_Search,
        [[10, 25, 50, 100]]),      # number of branches
    # Simulated Annealing
    (   'Simulated Annealing',
        sa.sim_Annealing,
        [[500, 100, 50],           # initial temperature
        [0.95, 0.85, 0.7],         # alpha value
        [350, 500]]),              # number of iterations
    # GRASP
    (   'GRASP',
        gr.grasp,
        [[50, 100, 200, 350, 500], # number of iteration
        [2, 5, 10, 15]]),          # number of best elements
    # Genetic
    (   'Genetic',
        ge.genetic,
        [[10, 20, 30],             # population size
        [50, 100, 200, 350, 500],  # number of iterations
        [0.75, 0.85,0.95],         # crossover rate
        [0.10, 0.20, 0.30]])       # mutation rate
]

# TEST_PARAM = [
#     # Beam Search
#     [10],      # number of branches
#     # Simulated Annealing
#     [,          # initial temperature
#      ,          # alpha value
#      ],         # number of iterations
#     # GRASP
#     [,          # number of iteration
#      ],         # number of best elements
#     # Genetic
#         [,      # population size
#          ,      # number of iterations
#          ,      # crossover rate
#          ]      # mutation rate
# ]

# Returns a list with all possible configurations of the paremeters in parList:
def build_Parameters(parList):
    return [list(x) for x in product(*parList)]

def normalize(l):
    m = max(l)
    return [x/m for x in l]

def take_Best_Configurations(par, res, norm, tim):
    bestResults = []
    bestTimes = []
    spars = []
    # hpResults = list(zip_longest(*res))
    hpNormResults = list(zip_longest(*norm))
    hpTimes = list(zip_longest(*tim))
    avarages = [sum(x)/len(x) for x in hpNormResults]
    i = avarages.index(max(avarages))
    testPar = par[i]
    for _ in range(10):
        i = avarages.index(max(avarages))
        if avarages[i] == 0:
            break
        bestResults.append(hpNormResults[i])
        bestTimes.append(hpTimes[i])
        spars.append(str(par[i]))
        avarages[i] = 0
    return testPar, bestResults, bestTimes, spars

def genarate_Boxplot(tableName,data,xTickLabels,yLabel,xLabel):
    # fig, bplot = plt.subplots()
    # bplot.set_title(tableName)
    # bplot.set_xlabel(xLabel)
    # bplot.set_ylabel(yLabel)
    # black_Diamond = dict(markerfacecolor='k',marker='d')
    # bplot.boxplot(y, flierprops=black_Diamond)
    # # bplot.set_xticklabels(x)
    # plt.savefig('./figs/'+tableName+'.png')

    # print(tableName+':\n', data)

    plt.figure()
    bp = sns.boxplot(data=data,showmeans=True)
    bp.set(xlabel=xLabel,ylabel=yLabel)
    bp.set_xticklabels(xTickLabels)
    plt.savefig('./figs/'+tableName+'.png')

def train():
    testParameters = []
    # hBestResults = []
    # hBestTimes = []
    for h in HEURISTICS[1:]: # for each metaheuristic
        funcName = h[0]
        func = h[1]
        parList = h[2]
        parameters = build_Parameters(parList)
        results = []     # heuristics results
        normResults = [] # heuristics normalized results
        execTimes = []   # heuristics execution times
        for p in TRAIN: # for each problem
            T = p[0]
            OBJs = p[1]
            r = [] # problem results
            n = [] # problem normalazed results
            t = [] # problem exec time
            for c in parameters: # for each configuration of hiperparameters
                start = time()
                ans = func(T,OBJs, 120,*c)
                end = time()
                r.append(bp.state_Value(ans,OBJs))
                t.append(end-start)
            n = normalize(r)
            results.append(r.copy())
            normResults.append(n.copy())
            execTimes.append(t.copy())
        testPar, bestResults, bestTimes, xTickLabels = take_Best_Configurations(parameters, results, normResults, execTimes)
        testParameters.append(testPar.copy())
        print(testPar)
        # hBestResults.append(bestResults.copy())
        # hBestTimes.append(bestTimes.copy())
        genarate_Boxplot(funcName+' - Valores', bestResults, xTickLabels, 'Valor Normalizado', 'Melhores Hiperparâmetros')
        genarate_Boxplot(funcName+' - Tempo de Execução', bestTimes, xTickLabels, 'Tempo (segundos)', 'Melhores Hiperparâmetros')
    return testParameters

# print(build_Parameters(HEURISTICS[2][1]))
# print(normalize([1,2,3]))
# print(take_Best_Configurations([[1,2,3],[2,3,4],[3,4,5],[4,5,6],[5,6,7]],[[1,1,5],[1,2,5],[1,2,5],[2,2,5],[1,1,5]],[[0.1,0.01,0.5],[0.1,0.2,0.05],[0.4,0.8,0.5],[0.2,0.2,0.54],[0.7,0.1,0.9]]))
# genarate_Boxplot('Resultados Alcançados',['Beam Search','GRASP','Simulated Annealing'],[[2,4,5,7,5,4],[5,6,5],[1,10,9,35,21,2,3,8]])

print(train())

# def test():
