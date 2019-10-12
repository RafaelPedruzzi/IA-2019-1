## -------------------------------------------------------- ##
#   Trab 1 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   hillClimbing.py: implements the hill climbing metaheuristic for the bag problem
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
from time import time

# Returns True and the valid state with the biggest value, or False if no state is valid:
def select_Best(si, T, OBJs):
    sn = -1 # best state position
    sv = 0 # state value
    for i in range(len(si)):
        v = bp.state_Value(si[i], OBJs) # current value
        if bp.state_Verify(si[i], T, OBJs) and v > sv:
            sv = v
            sn = i
    if sn == -1:
        return False, []
    return True, si[sn]

# Hill Climbing:
def hill_Climbing(T, OBJs, execTime, *args):
    sn = [0]*len(OBJs) # initial state
    c = True # continue flag
    start = time()
    while c:
        if time() - start > execTime:
            break
        cs = sn # storing current state
        c, sn = select_Best(bp.state_Expansion(cs), T, OBJs)
    return cs

# T = 19 # bag size
# OBJs = [(1,3), (4,6), (5,7)] # object list (v,t)
# print(hill_Climbing(T,OBJs))
