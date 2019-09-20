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
    si.sort(key = bp.state_Value)
    probRatio = []
    for s in si:
        probRatio.append(bp.state_Value(s))
    ratSum = sum(probRatio)
    probRatio = [ (i/ratSum) for i in probRatio]
    for i in probRatio:
        propRatio[i] = sum(probRatio[:i])
    ratSum = sum(probRatio)
    selector = random.random(ratSum)
    for i in probRatio:
        if selector < probRatio[i]:
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

iter = 50
print(grasp(iter))