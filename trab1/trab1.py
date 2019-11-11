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
import numpy as np
import tabulate

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
    (   'Hill Climbing',           # heuristic name
        hc.hill_Climbing,          # heuristic function
        [[]],                      # hiperparameters
        []),                       # test parameters
    # Beam Search
    (   'Beam Search',             # heuristic name
        bs.beam_Search,            # heuristic function
        [[10, 25, 50, 100]],       # number of branches
        [10]),                     # test parameters
    # Simulated Annealing
    (   'Simulated Annealing',     # heuristic name
        sa.sim_Annealing,          # heuristic function
        [[500, 100, 50],           # initial temperature
        [0.95, 0.85, 0.7],         # alpha value
        [350, 500]],               # number of iterations
        [500, 0.95, 500]),         # test parameters
    # GRASP
    (   'GRASP',                   # heuristic name
        gr.grasp,                  # heuristic function
        [[50, 100, 200, 350, 500], # number of iteration
        [2, 5, 10, 15]],           # number of best elements
        [500, 15]),                # test parameters
    # Genetic
    (   'Genetic',                 # heuristic name
        ge.genetic,                # heuristic function
        [[10, 20, 30],             # population size
        [0.75, 0.85,0.95],         # crossover rate
        [0.10, 0.20, 0.30]],       # mutation rate
        [30, 0.95, 0.3])           # test parameters
]

# Returns a list with all possible configurations of the parameters in parList:
def build_Parameters(parList):
    return [list(x) for x in product(*parList)]

# normalize a list of numbers:
def normalize(l):
    m = max(l)
    return [x/m for x in l]

# select the bests hiperparameters configurations:
def take_Best_Configurations(par, res, norm, tim):
    bestResults = [] # list with 10 best hiperparameters configuration
    bestTimes = []   # execution times of the 10 best hiperparameters configuration
    spars = []       # the 10 best hiperparameters converted to string
    hpNormResults = list(zip_longest(*norm)) # agrouping parameter by problem
    hpTimes = list(zip_longest(*tim))        # agrouping execution times by problem
    avarages = [mean(x) for x in hpNormResults] # calculating avarage of each configuration
    i = avarages.index(max(avarages))
    testPar = par[i] # best hiperparameter configuration
    for _ in range(10): # taking 10 best configurations
        i = avarages.index(max(avarages))
        if avarages[i] == 0:
            break
        bestResults.append(hpNormResults[i])
        bestTimes.append(hpTimes[i])
        spars.append(str(par[i]))
        avarages[i] = 0
    return testPar, bestResults, bestTimes, spars

# generate and save a boxplot in a file:
def genarate_Boxplot(tableName,data,xTickLabels,yLabel,xLabel):
    plt.rc('font', size=6) # setting figure configuration
    fig = plt.figure()  # creating a new figure
    fig.set_size_inches(8, 6) # setting figure size
    # genarating boxplot
    bp = sns.boxplot(data=data,showmeans=True)
    bp.set(xlabel=xLabel,ylabel=yLabel)
    bp.set_xticklabels(xTickLabels)
    plt.setp(bp.get_xticklabels(), rotation=45)
    plt.savefig('./figs/'+tableName+'.png') # saving figure in a PNG file

# train algorithm:
def train():
    testParameters = []
    for h in HEURISTICS: # for each metaheuristic
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
                r.append(bp.state_Value(ans,OBJs)) # saving result
                t.append(end-start)                # saving execution time
            n = normalize(r) # normalizing results
            results.append(r.copy())     # saving problem results
            normResults.append(n.copy()) # saving problem normalized results
            execTimes.append(t.copy())   # saving problem execution time
        testPar, bestResults, bestTimes, xTickLabels = take_Best_Configurations(parameters, results, normResults, execTimes)
        testParameters.append(testPar.copy())
        # saving best parameter in a file:
        with open('Results.txt', 'a') as file:
            file.write(funcName+': '+str(testPar)+'\n')
        # printing boxplots:
        genarate_Boxplot(funcName+'_-_Valores', bestResults, xTickLabels, 'Valor Normalizado', 'Melhores Hiperparâmetros')
        genarate_Boxplot(funcName+'_-_Tempo_de_Execução', bestTimes, xTickLabels, 'Tempo (segundos)', 'Melhores Hiperparâmetros')
    return testParameters

# normalize the i-elements of every list in a list of lists of numbers:
def crossNormalize(l):
    lx = list(zip_longest(*l))
    normx = [normalize(x) for x in lx]
    norm = list(zip_longest(*normx))
    return norm

# creates a LaTeX formated table and save it on a file:
def generateLatexTable(pars,headers,fileName,zipPar=True):
    tabulate.LATEX_ESCAPE_RULES={}
    table = []
    if zipPar:
        l = list(zip_longest(*pars))
    else:
        l = pars
    for i in l:
        table.append(i)
    latexTable = tabulate.tabulate(table, headers=headers, tablefmt='latex')
    with open('dados/'+fileName+'.txt', 'w') as file:
        file.write(latexTable)
    return

# rank a list of numbers:
def rank(l):
    tam = len(l)
    sort = sorted(l,reverse=True)
    r = [] # auxiliar that agrupates repeted values
    ranked = [] # ranks in crescent order
    unsortRanked = [0]*tam # ranks in original l list's order
    positions = [] # auxiliar that keeps the original index of the ranked values
    # grouping repeted values:
    for i in range(tam):
        if i > 0 and sort[i] == sort[i-1]:
            (r[len(r)-1]).append(i+1)
        else:
            r.append( [i+1] )
    # building rank where equal values get (sum of ranks ocuped by this values / number of values):
    for x in r:
        ranked = ranked + ([mean(x)]*len(x))
    # building unsortRanked:
    for i in range(tam):
        unsortRanked[i] = ranked[sort.index(l[i])]
    nl = np.array(l)
    # mapping ranked values:
    for i in sort:
        ii = np.where(nl == i)[0]
        positions = positions + list(ii)
    positions =  list(dict.fromkeys(positions))
    mapRanked = [(ranked[i],positions[i]) for i in range(tam)]
    return mapRanked, unsortRanked

# makes the avarage of the ranks of the results list and save it on a file:
def avgRank(results):
    # making list of ranks:
    ranks = []
    for l in list(zip_longest(*results)):
        _, r = rank(l)
        ranks.append(r)
    # calculating avarage of the ranks:
    means = []
    for r in list(zip_longest(*ranks)):
        means.append(mean(r))
    # printing rank as table on file
    table = [ [means[i],HEURISTICS[i][0]] for i in range(len(means)) ]
    table = sorted(table)
    headers = ['Colocação','Meta-heurística']
    name = 'Rank Absoluto'
    generateLatexTable(table,headers,name,False)

# make the rank of a list of the normalized avarages and save it on a file:
def normRank(normAvr):
    ranks, _ = rank(normAvr)
    table = [ [x,HEURISTICS[i][0]] for (x,i) in ranks ]
    headers = ['Colocação','Meta-heurística']
    name = 'Rank Normalizado'
    generateLatexTable(table,headers,name,False)

# test algorithm:
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
    # saving boxplots:
    genarate_Boxplot(' Teste - Valores', normResults, names, 'Valor', 'Meta-Heurística')
    genarate_Boxplot(' Teste - Tempo de Execução', execTimes, names, 'Tempo (segundos)', 'Meta-Heurística')
    headers = ['Meta-heurística','Média Absoluta','Desvio Padrão Absoluto','Média Normalizada','Desvio Padrão Normalizado','Média do Tempo de Execução','Desvio Padrão do Tempo de Execução']
    # saving table:
    generateLatexTable([names,avr,sdv,normAvr,normSdv,timeAvr,timeSdv],headers,'Tabela')
    # making and saving ranks:
    avgRank(results)
    normRank(normAvr)

train()
test()
