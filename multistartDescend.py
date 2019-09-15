## -------------------------------------------------------- ##
#   Exercise 6: Multistart Descent
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
import simpleDescent as sd
import deepestDescent as dd
import random
from math import floor

# Returns a random valid state:
def random_Start_State():
    s = []
    for i in range(len(bp.OBJs)):
        v = floor(bp.size(bp.OBJs[i]) * random.random())
        s.append(v)
    random.shuffle(s)
    return s

# Multistart Descend:
def multistart_Descend(iter, use_Deepest = False):
    if use_Deepest:
        func = dd.deepest_Descent
    else:
        func = sd.simple_Descent
    bs = [0]*len(bp.OBJs) # best state found
    for _ in range(iter):
        s = random_Start_State()
        sn = func(s)
        if bp.state_Verify(sn) and bp.state_Value(sn) > bp.state_Value(bs):
            bs = sn
    return bs

iter = 50
print("Simple descending:", multistart_Descend(iter))
print("Deepest descending:", multistart_Descend(iter,True))