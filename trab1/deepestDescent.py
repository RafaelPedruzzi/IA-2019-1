## -------------------------------------------------------- ##
#   Trab 1 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   deepestDescent.py: implements the deepest descent heuristic for the bag problem
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp

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

# Return a neightborhood of the given state
def neightborhood(s, T, OBJs):
    neig = []
    for i in bp.state_Expansion(s):   # adding all valid expansions of the given state
        if bp.state_Verify(i, T, OBJs):
            neig.append(i)
    for i in neig:                    # adding all valid retractions of each state currently in the neightborhood
        for j in bp.state_Retract(i):
            if bp.state_Verify(j, T, OBJs):
                neig.append(j)
    for i in bp.state_Retract(s):     # adding all valid retractions of the given state
        if bp.state_Verify(i, T, OBJs):
            neig.append(i)
    return neig

# Deepent Descent:
def deepest_Descent(T, OBJs, s):
    bs = s # best state found
    si = neightborhood(s, T, OBJs)
    c = True # continue flag
    while c:
        c, sn = select_Best(si, T, OBJs)
        if bp.state_Value(sn, OBJs) > bp.state_Value(bs, OBJs):
            bs = sn
            si = neightborhood(sn, T, OBJs)
        else:
            break
    return bs

# T = 19 # bag size
# OBJs = [(1,3), (4,6), (5,7)] # object list (v,t)
# s = [0]*len(OBJs)
# print(deepest_Descent(T, OBJs, s))
