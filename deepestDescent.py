## -------------------------------------------------------- ##
#   Exercise 5: Deepest Descent
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

# Return a neightborhood of the given state
def neightborhood(s):
    neig = []
    for i in bp.state_Expansion(s):   # adding all valid expansions of the given state
        if bp.state_Verify(i):
            neig.append(i)
    for i in neig:                    # adding all valid retractions of each state currently in the neightborhood
        for j in bp.state_Retract(i):
            if bp.state_Verify(j):
                neig.append(j)
    for i in bp.state_Retract(s):     # adding all valid retractions of the given state
        if bp.state_Verify(i):
            neig.append(i)
    return neig

# Deepent Descent:
def deepest_Descent(s):
    bs = s # best state found
    si = neightborhood(s)
    c = True # continue flag
    while c:
        c, sn = select_Best(si)
        if bp.state_Value(sn) > bp.state_Value(bs):
            bs = sn
            si = neightborhood(sn)
        else:
            break
    return bs

s = [0]*len(bp.OBJs)
print(deepest_Descent(s))
