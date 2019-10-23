## -------------------------------------------------------- ##
#   Trab 1 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   genetic.py: implements the genetic algorithm metaheuristic for the bag problem
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
import random
from math import floor
from time import time

# Objective function:
def fitness(s, T, OBJs):
    if bp.state_Verify(s, T, OBJs):
        return bp.state_Value(s, OBJs)
    return 0

# Returns the best individual in the population:
def best_in_Pop(si, T, OBJs):
    sn = 0 # best state index
    for i in range(len(si)):
        if fitness(si[i], T, OBJs) > fitness(si[sn], T, OBJs):
            sn = i
    return si[sn]

# Returns a initial population:
def init_Population(popMaxSize, OBJs):
    pop = [[0]*len(OBJs)]
    for _ in range(popMaxSize):
        s = pop[len(pop)-1].copy()
        s = mutation(s)
        if bp.state_Value(s,OBJs) == 0:
            p = random.randint(0, len(s)-1)
            s[p] += 1
        pop.append(s)
    return pop

# Crossover operation:
def crossover(s1, s2):
    cut = random.randint(1,len(s1)-1) # selecting a random cut point
    child1 = s1[:cut] + s2[cut:]
    child2 = s2[:cut] + s1[cut:]
    return child1, child2

# Mutation operation:
def mutation(s):
    for _ in range(random.randint(0, len(s)-1)): # randomly selecting the number of changes
        target = random.randint(0, len(s)-1) # randomly selecting the position to be changed
        if random.random() >= 0.5: # randomly selecting the change (increment or decrement)
            s[target] += 1
        elif s[target] > 0:
            s[target] -= 1
    return s

# Select a random individual in the given population by the roulette method:
def roulette(si, OBJs):
    probRatio = [] # roulette
    # Adding all states's values to probRatio:
    for s in si:
        probRatio.append(bp.state_Value(s, OBJs))
    # Normalizing the values:
    ratioSum = sum(probRatio)
    probRatio = [ (i/ratioSum) for i in probRatio]
    # Building the "partitions" of the roulette:
    for i in range(len(probRatio)):
        probRatio[i] = sum(probRatio[i:])
    # Selecting a random element:
    selector = random.random()
    for i in range(len(probRatio)):
        if selector >= probRatio[i]:
            s = si[i]
            break
    return s

# Generates a new population:
def generate_New_Pop(si, crossoverRate, mutationRate, T, OBJs):
    elite = best_in_Pop(si, T, OBJs)
    snew = [elite]
    while len(snew) < len(si):
        s1 = roulette(si, OBJs) # selecting a individual by the roulette method
        if random.random() < crossoverRate: # crossover operation
            s2 = roulette(si, OBJs)
            s1, s2 = crossover(s1, s2)
            snew.append(s2)
            if len(snew) >= len(si): # breaking if population is full
                break
        if random.random() < mutationRate: # mutation operation
            s1 = mutation(s1)
        snew.append(s1)
    return snew

# Genetic Algorithm:
def genetic(T, OBJs, execTime, *args):
    popMaxSize = args[0]
    niter = 500
    crossoverRate = args[1]
    mutationRate = args[2]
    si = init_Population(popMaxSize, OBJs)
    bs = [0]*len(OBJs)
    start = time()
    for _ in range(niter):
        if time() - start > execTime:
            break
        si = generate_New_Pop(si, crossoverRate, mutationRate, T, OBJs)
        s = best_in_Pop(si, T, OBJs)
        if bp.state_Verify(s, T, OBJs) and bp.state_Value(s, OBJs) > bp.state_Value(bs, OBJs):
            bs = s
    return bs

# T = 19 # bag size
# OBJs = [(1,3), (4,6), (5,7)] # object list (v,t)
# crossoverRate = 0.8
# mutationRate = 0.2
# iter = 50 # number of generations
# popMaxSize = 10 # size of the population
# print(genetic(T,OBJs,popMaxSize,iter,crossoverRate,mutationRate))
