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
        if fitness(si[i]) > fitness(si[sn]):
            sn = i
    return si[sn]

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
def roulette(si):
    probRatio = [] # roulette
    # Adding all states's values to probRatio:
    for s in si:
        probRatio.append(bp.state_Value(s))
    # Normalizing the values:
    ratioSum = sum(probRatio)
    probRatio = [ (i/ratioSum) for i in probRatio]
    # Building the "partitions" of the roulette:
    for i in range(len(probRatio)):
        probRatio[i] = sum(probRatio[i:])
    # Selecting a random element:
    ratioSum = sum(probRatio)
    selector = random.random()
    for i in range(len(probRatio)):
        if selector >= probRatio[i]:
            s = si[i]
            break
    return s

# Generates a new population:
def generate_New_Pop(si, crossoverRate, mutationRate):
    elite = best_in_Pop(si)
    snew = [elite]
    while len(snew) < len(si):
        s1 = roulette(si) # selecting a individual by the roulette method
        if random.random() < crossoverRate: # crossover operation
            s2 = roulette(si)
            s1, s2 = crossover(s1, s2)
            snew.append(s2)
            if len(snew) >= len(si): # breaking if population is full
                break
        if random.random() < mutationRate: # mutation operation
            s1 = mutation(s1)
        snew.append(s1)
    return snew

# Genetic Algorithm:
def genetic(popMaxSize, iter, crossoverRate, mutationRate):
    si = init_Population(popMaxSize)
    bs = [0]*len(bp.OBJs)
    for _ in range(iter):
        si = generate_New_Pop(si, crossoverRate, mutationRate)
        s = best_in_Pop(si)
        if bp.state_Verify(s) and bp.state_Value(s) > bp.state_Value(bs):
            bs = s
    return bs

crossoverRate = 0.8
mutationRate = 0.2
iter = 50 # number of generations
popMaxSize = 20 # size of the population
print(genetic(popMaxSize,iter,crossoverRate,mutationRate))
