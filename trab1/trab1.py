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
from statistics import mean, stdev

# Train problems (T, [(vi,ti)])
TRAIN = [
    # P1
    (   19,
        [(1,3),(4,6),(5,7)],
        'P1'),
    # P3
    (   58,
        [(1,3),(4,6),(5,7),(3,4)],
        'P3'),
    # P4
    (   58,
        [(1,3),(4,6),(5,7),(3,4),(8,10),(4,8),(3,5),(6,9)],
        'P4'),
    # P6
    (   58,
        [(1,3),(4,6),(5,7),(3,4),(8,10),(4,8),(3,5),(6,9),(2,1)],
        'P6'),
    # P8
    (   120,
        [(1,2),(2,3),(4,5),(5,10),(14,15),(15,20),(24,25),(29,30),(50,50)],
        'P8'),
    # P9
    (   120,
        [(1,2),(2,3),(3,5),(7,10),(10,15),(13,20),(24,25),(29,30),(50,50)],
        'P9'),
    # P11
    (   120,
        [(24,25),(29,30),(50,50)],
        'P11'),
    # P14
    (   138,
        [(1,3),(4,6),(5,7),(3,4),(2,6),(2,3),(6,8),(1,2),(2,3),(3,5),(7,10),(10,15),(13,20),(24,25),(29,30),(50,50)],
        'P14'),
    # P17
    (   13890000,
        [(1,3),(4,6),(5,7),(3,4),(2,6),(2,3),(6,8),(1,2),(3,5),(7,10),(10,15),(13,20),(24,25),(29,37)],
        'P17'),
    # P20
    (   45678901,
        [(1,3),(4,6),(5,7),(3,4),(2,6),(1,2),(3,5),(7,10),(10,15),(13,20),(15,20)],
        'P20')
]

# Test problems (T, [(vi,ti)])
TEST = [
    # P2
    (   192,
        [(1,3),(4,6),(5,7)],
        'P2'),
    # P5
    (   287,
        [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10)],
        'P5'),
    # P7
    (   120,
        [(1,2),(2,3),(4,5),(5,10),(14,15),(13,20),(24,25),(29,30),(50,50)],
        'P7'),
    # P10
    (   1240,
        [(1,2),(2,3),(3,5),(7,10),(10,15),(13,20),(24,25),(29,30),(50,50)],
        'P10'),
    # P12
    (   104,
        [(25,26),(29,30),(49,50)],
        'P12'),
    # P13
    (   138,
        [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8)],
        'P13'),
    # P15
    (   13890,
        [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2), (2,3), (3,5), (7,10), (10,15), (13,20), (24,25),(29,30), (50,50)],
        'P15'),
    # P16
    (   13890,
        [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2),(3,5),(7,10),(10,15),(13,20),(24,25),(29,37)],
        'P16'),
    # P18
    (   190000,
        [(1,3),(4,6),(5,7)],
        'P18'),
    # P19
    (   4567,
        [(1,3),(4,6),(5,7),(3,4),(2,6),(1,2),(3,5),(7,10),(10,15),(13,20),(15,20)],
        'P19')
]

HEURISTICS = [
    # Hill Climbing
    (   'Hill Climbing',
        hc.hill_Climbing,
        [[]],
        []),                       # test parameters
    # Beam Search
    (   'Beam Search',
        bs.beam_Search,
        [[10, 25, 50, 100]],       # number of branches
        [10]),                     # test parameters
    # Simulated Annealing
    (   'Simulated Annealing',
        sa.sim_Annealing,
        [[500, 100, 50],           # initial temperature
        [0.95, 0.85, 0.7],         # alpha value
        [350, 500]],               # number of iterations
        [500, 0.95, 500]),         # test parameters
    # GRASP
    (   'GRASP',
        gr.grasp,
        [[50, 100, 200, 350, 500], # number of iteration
        [2, 5, 10, 15]],           # number of best elements
        []),                       # test parameters
    # Genetic
    (   'Genetic',
        ge.genetic,
        [[10, 20, 30],             # population size
        [0.75, 0.85,0.95],         # crossover rate
        [0.10, 0.20, 0.30]],       # mutation rate
        [20, 0.75, 0.3])           # test parameters
]

# Returns a list with all possible configurations of the paremeters in parList:
def build_Parameters(parList):
    return [list(x) for x in product(*parList)]
    # for x in product(*parList):
    #     yield list(x)

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
    plt.rc('font', size=6)
    fig = plt.figure()
    fig.set_size_inches(8, 6)
    bp = sns.boxplot(data=data,showmeans=True)
    bp.set(xlabel=xLabel,ylabel=yLabel)
    bp.set_xticklabels(xTickLabels)
    plt.setp(bp.get_xticklabels(), rotation=45)
    plt.savefig('./figs/'+tableName+'.png')

def train():
    testParameters = []
    for h in HEURISTICS[4:]: # for each metaheuristic
        funcName = h[0]
        func = h[1]
        parList = h[2]
        parameters = build_Parameters(parList)
        results = []     # heuristics results
        normResults = [] # heuristics normalized results
        execTimes = []   # heuristics execution times
        for p in TRAIN: # for each train problem
            T = p[0]
            OBJs = p[1]
            r = [] # problem results
            n = [] # problem normalized results
            t = [] # problem execution time
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
        with open('Results.txt', 'a') as file:
            file.write(funcName+': '+str(testPar)+'\n')
        genarate_Boxplot(funcName+' - Valores', bestResults, xTickLabels, 'Valor Normalizado', 'Melhores Hiperparâmetros')
        genarate_Boxplot(funcName+' - Tempo de Execução', bestTimes, xTickLabels, 'Tempo (segundos)', 'Melhores Hiperparâmetros')
    return testParameters

def crossNormalize(l):
    lx = list(zip_longest(*l))
    normx = [normalize(x) for x in lx]
    norm = list(zip_longest(*normx))
    return norm

def generateLatexTable(names,avr,sdv,normavr,normsdv,timeavg,timesdv):
    return

def rank(l):
    tam = len(l)
    sort = sorted(l,reverse=True)
    r = []
    for i in range(tam):
        if i > 0 and sort[i] == sort[i-1]:
            (r[len(r)-1]).append(i+1)
        else:
            r.append( [i+1] )
    ranked = [] # NEED TO BE SOME KIND OF TUPLE!!
    for x in r:
        ranked = ranked + ([mean(x)]*len(x))
    ranked = [(ranked[i],l.index(sort[i])) for i in range(tam)]
    unsortRanked = [0]*tam
    for i in range(tam):
        unsortRanked[i] = ranked[sort.index(l[i])]
    return ranked, unsortRanked

def avgRank():
    return

def normRank():
    return

def test():
    results = []     # heuristics results
    normResults = [] # heuristics normalized results
    execTimes = []   # heuristics execution times
    avr = []         # heuristics avarages
    sdv = []         # heuristics standard deviations
    normAvr = []     # normalized heuristics avarages
    normSdv = []     # normalized heuristics standard deviations
    timeAvr = []     # heuristics execution times avarages
    timeSdv = []     # heuristics execution times standard deviations
    for h in HEURISTICS: # for each metaheuristic
        funcName = h[0]
        func = h[1]
        par = h[3]       
        r = [] # problens results
        t = [] # problens execution time
        for p in TEST:   # for each test problem
            T = p[0]
            OBJs = p[1]
            start = time()
            ans = func(T,OBJs, 300,*par)
            end = time()
            r.append(bp.state_Value(ans,OBJs))
            t.append(end-start)
        results.append(r.copy())
        execTimes.append(t.copy())
        avr.append(mean(r))
        sdv.append(stdev(r))
        timeAvr.append(mean(t))
        timeSdv.append(stdev(t))
    names = [x[0] for x in HEURISTICS]
    normResults = crossNormalize(results) # normalizing problens results
    normAvr = [mean(x) for x in normResults]
    normSdv = [stdev(x) for x in normResults]

    genarate_Boxplot(funcName+' Teste - Valores', normResults, names, 'Valor', 'Meta-Heurística')
    genarate_Boxplot(funcName+' Teste - Tempo de Execução', execTimes, names, 'Tempo (segundos)', 'Meta-Heurística')
    generateLatexTable(names,avr,sdv,normAvr,normSdv,timeAvr,timeSdv)


# print(train())
# l = [7,4,7,12,7]
# print(rank(l))

# par = build_Parameters(HEURISTICS[4][2])
# prob = TRAIN[7]
# for c in par:
#     ans = ge.genetic(prob[0],prob[1],120,*c)
#     print(bp.state_Size(ans,prob[1]), bp.state_Value(ans,prob[1]))

