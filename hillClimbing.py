## -------------------------------------------------------- ##
#   Exercise 1: Hill Climbing
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp

# Returns True and the valid state with the biggest value, or False if no state is valid:
def select_Best(si):
    sn = -1 # best state position
    sv = 0 # state value
    for i in range(len(si)):
        v = bp.state_Value(si[i]) # current value
        if bp.state_Verify(si[i]) and v > sv:
            sv = v
            sn = i
    if sn == -1:
        return False, []
    return True, si[sn]

# Hill Climbing:
def hill_Climbing():
    sn = [0]*len(bp.OBJs) # initial state
    c = True # continue flag
    while c:
        cs = sn # storing current state
        c, sn = select_Best(bp.state_Expansion(cs))
    return cs

# print(hill_Climbing())
