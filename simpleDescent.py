## -------------------------------------------------------- ##
#   Exercise 4: Simple Descent
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
import random

# Remove and return a random item from the given list:
def take_Random(si):
    if si == []:
        return []
    return si.pop(random.randint(0,len(si)-1))

# Return a neightborhood of the given state
def neightborhood(s):
    neig = []
    for i in bp.state_Expansion(s): # add all valid states from the expansion of the given state
        if bp.state_Verify(i):
            neig.append(i)
    for i in bp.state_Retract(s): # add all valid states from the retraction of the given state
        if bp.state_Verify(i):
            neig.append(i)
    return neig

# Simple Descent:
def simple_Descent(s):
    bs = s # best state found
    si = neightborhood(s)
    while len(si) > 0:
        for _ in range(len(si)):
            sn = take_Random(si)
            if bp.state_Value(sn) > bp.state_Value(bs):
                bs = sn
                si = neightborhood(sn)
                break
        else:
            break # exiting if no better state is found
    return bs

s = [0]*len(bp.OBJs)
print(simple_Descent(s))
