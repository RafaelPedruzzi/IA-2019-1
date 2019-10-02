## -------------------------------------------------------- ##
#   Trab 1 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   grasp.py: implements the greedy randomized adaptive search (GRASP) heuristic for the bag problem
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
import deepestDescent as dp
import random

def local_Search(T, OBJs, s):
    return dp.deepest_Descent(T, OBJs, s)

def roulette(l):
    probRatio = [] # roulette
    c = (0,0)
    # Adding values to probRatio:
    for i in l:
        probRatio.append(i[1])
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
            c = l[i]
            break
    return c

def greedy_Random_Construct(s, numBest, T, OBJs):
    sv = bp.state_Value(s, OBJs) # value of state s
    additions = [0]*len(OBJs)    # list of possible additions to state s
    best = []                    # list of best additions
    # Each i-position of "additions" receive the maximum number of additional i-objects (object in position i of OBJs) suported by the bag:
    for i in range(len(additions)):
        q = 0
        while sv + (q+1)*bp.size(OBJs[i]) < T:
            q += 1
        additions[i] = q
    # Selecting the best addition:
    while len(best) < numBest:
        i = additions.index(max(additions)) # taking index of addition with the best value
        if additions[i] <= 0: # breaking if there are no possible additions
            break
        best.append((i,additions[i])) # appending addition to best
        additions[i] -= 1 # updating addition
    if len(best) > 0:
        # c = best[random.randint(0, len(best)-1)]
        c = roulette(best)
        s[c[0]] += c[1] # c[0] = position to update; c[1] = value to be added
    return s

def grasp(T, OBJs, iter, numBest):
    s = [0]*len(OBJs)
    bs = s # best state found
    for _ in range(iter):
        s = greedy_Random_Construct(s, numBest, T, OBJs)
        sl = local_Search(T, OBJs, s) # local state found
        if bp.state_Verify(sl, T, OBJs) and bp.state_Value(sl, OBJs) > bp.state_Value(bs, OBJs):
            bs = sl
    return bs

T = 19 # bag size
OBJs = [(1,3), (4,6), (5,7)] # object list (v,t)
iter = 50
numBest = 10
print(grasp(T,OBJs,iter,numBest))
