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

# Crossover operation:
def crossover(s1, s2):
    cut = random.randint(1,len(s1)-1)
    child1 = s1[:cut] + s2[cut:]
    child2 = s2[:cut] + s1[cut:]
    return child1, child2

# Mutation operation:
def mutation(s):
    for _ in range(random.randint(0, len(s)-1)):
        target = random.randint(0, len(s)-1)
        if random.random() >= 0.5:
            s[target] += 1
        elif s[target] > 0:
            s[target] -= 1
    return s

# Select a random individual in the given population by the roulette method:
def roulette(si):
    scpy = si.copy()
    scpy.sort(key = bp.state_Value)
    probRatio = []
    for s in scpy:
        probRatio.append(bp.state_Value(s))
    ratioSum = sum(probRatio)
    probRatio = [ (i/ratioSum) for i in probRatio]
    print(probRatio)
    for i in range(len(probRatio)):
        probRatio[i] = sum(probRatio[:i])
    ratioSum = sum(probRatio)
    selector = random.randint(0, ratioSum)
    for i in range(len(probRatio)):
        if selector < probRatio[i]:
            s = scpy[i]
            break
    return s

# Generates a new population:
# def generate_New_Pop(si, crossoverRate, mutationRate):

# # Genetic Algorithm:
# def genetic(popMaxSize, iter, crossoverRate, mutationRate):
#     si = init_Population(popMaxSize)
#     bs = [0]*len(bp.OBJs)
#     for _ in range(iter):
#         ss = generate_New_Pop(si, crossoverRate, mutationRate)
#         s = best_in_Pop(ss)
#         if bp.state_Verify(s) and bp.state_Value(s) > bp.state_Value(bs):
#             bs = s
#         si = ss
#     return bs

crossoverRate = 0.75
mutationRate = 0.2
iter = 50
popMaxSize = 10
# print(genetic(popMaxSize,iter))
print(roulette([[1,2,3],[3,2,1],[5,6,7],[8,7,6]]))
