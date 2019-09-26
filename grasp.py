## -------------------------------------------------------- ##
#   Greedy Randomized Adaptive Search (GRASP)
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
import deepestDescent as dp
import random

def local_Search(s):
    return dp.deepest_Descent(s)

def select_Random(si):
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
    if bp.state_Verify(s):
        return True, s
    return False, []

def greedy_Random_Construct():
    sn = [0]*len(bp.OBJs) # initial state
    c = True # continue flag
    while c:
        cs = sn # storing current state
        c, sn = select_Random(bp.state_Expansion(cs))
    return cs

def grasp(iter):
    bs = [0]*len(bp.OBJs)
    for _ in range(iter):
        s = greedy_Random_Construct()
        s = local_Search(s)
        if bp.state_Verify(s) and bp.state_Value(s) > bp.state_Value(bs):
            bs = s
    return bs

iter = 10
print(grasp(iter))