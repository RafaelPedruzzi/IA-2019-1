## -------------------------------------------------------- ##
#   Exercise 1: Hill Climbing
#
#   Rafael Belmock Pedruzzi
## -------------------------------------------------------- ##

import bagProblem as bp

# Returns True and the valid state with the biggest value, or False if no state is valid:
def hc_Select(si):
    sn = -1
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
    x = True
    while x:
        cs = sn # storing current state
        x, sn = hc_Select(bp.state_Expansion(cs))
    return cs

# print(hill_Climbing())
