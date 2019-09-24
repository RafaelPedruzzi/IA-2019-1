## -------------------------------------------------------- ##
#   Exercise 8: Genetic Algorithm
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
import random
from math import floor

# Objective function:
def fitness(s):
    if bp.state_Verify(s):
        return bp.state_Value(s)
    return 0

# Returns the best individual in the population:
def best_in_Pop(si):
    sn = 0 # best state index
    for i in range(len(si)):
        if bp.state_Value(si[i]) > bp.state_Value(si[sn]):
            sn = i
    return si[sn]

# Returns the index to the worse individual in the population:
def worse_in_Pop(si):
    sn = 0 # worse state index
    for i in range(len(si)):
        if bp.state_Value(si[i]) < bp.state_Value(si[sn]):
            sn = i
    return sn

# Returns a initial population:
def init_Population(popMaxSize):
    pop = []
    for _ in range(popMaxSize):
        s = []
        for i in range(len(bp.OBJs)):
            v = floor(bp.size(bp.OBJs[i]) * random.random())
            s.append(v)
        random.shuffle(s)
        pop.append(s)
    return pop

# Generates a new population:
def generate_New_Pop(si, elite):

# Select the most fit individuals in the given population:
def select_Most_Fit(si):

# Genetic Algorithm:
def genetic(popMaxSize, iter):
    si = init_Population(popMaxSize)
    bs = [0]*len(bp.OBJs)
    for _ in range(iter):
        ss = generate_New_Pop(select_Most_Fit(si), best_in_Pop(si))
        s = best_in_Pop(ss)
        if bp.state_Verify(s) and bp.state_Value(s) > bp.state_Value(bs):
            bs = s
        si = ss
    return bs

iter = 50
popMaxSize = 10
#print(genetic(popMaxSize,iter))
