## -------------------------------------------------------- ##
#   Trab 1 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   grasp.py: implements the greedy randomized adaptive search (GRASP) metaheuristic for the bag problem
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
import deepestDescent as dp
import random
from time import time

from itertools import accumulate

def local_Search(T, OBJs, s, startTime, execTime):
    return dp.deepest_Descent(T, OBJs, s, startTime, execTime)

# Implements the roulette random selection method:
def roulette(si,OBJs):
    probRatio = [] # roulette
    c = []
    # Adding values to probRatio:
    for s in si:
        probRatio.append(bp.state_Value(s,OBJs))
    # Normalizing the values:
    ratioSum = sum(probRatio)
    probRatio = [ (i/ratioSum) for i in probRatio]
    # Building the "partitions" of the roulette:
    probRatio = list(accumulate(probRatio))
    # Selecting a random element:
    ratioSum = sum(probRatio)
    selector = random.random()
    for i in range(len(probRatio)):
        if selector <= probRatio[i]:
            c = si[i]
            break
    return c

# First part of the GRASP algorithm:
def greedy_Random_Construct(s, numBest, T, OBJs, start, execTime):
    sn = [0]*len(OBJs)                     # initial state
    while True:
        if time() - start > execTime:
            break
        additions = bp.state_Expansion(sn) # list of possible additions to state sn
        best = []                          # list of best additions
        # Selecting the best additions:
        i = 0
        # add states to best until best is full or there are no more states:
        while len(best) < numBest and i < len(additions):
            if bp.state_Verify(additions[i], T, OBJs):
                best.append(additions[i])
                if len(best) >= len(additions):
                    break
            i += 1
        # if best is not empty chose a state by the roulette method:
        if len(best) > 0:
            c = roulette(best,OBJs)
            sn = c
            continue
        break
    return sn

# GRASP
def grasp(T, OBJs, execTime, *args):
    niter = args[0]
    numBest = args[1]
    s = [0]*len(OBJs)
    bs = s # best state found
    start = time()
    for _ in range(niter):
        if time() - start > execTime:
            break
        s = greedy_Random_Construct(s, numBest, T, OBJs, start, execTime)
        sl = local_Search(T, OBJs, s, start, execTime) # local state found
        if bp.state_Verify(sl, T, OBJs) and bp.state_Value(sl, OBJs) > bp.state_Value(bs, OBJs):
            bs = sl
    return bs

# T = 19 # bag size
# OBJs = [(1,3), (4,6), (5,7)] # object list (v,t)
# iter = 50
# numBest = 10
# print(grasp(T,OBJs,iter,numBest))
