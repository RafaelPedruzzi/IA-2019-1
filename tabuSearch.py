## -------------------------------------------------------- ##
#   Exercise 7: Tabu Search
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
import tabuList as tl
import random

# Return a random item from the given list that is not on the tabu list and update the tabu list:
def take_Random_Tabu(si, t):
    for i in range(len(si)):
        s = si[i]
        if not t.is_in(s):
            break
    if s == []:
        return []
    t.insert(s)
    return s

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
        return []
    return si[sn]

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

# Tabu Search:
def tabu_Search(s, tsize, iter):
    bs = s               # best state found 
    ps = s               # previous state
    t = tl.tabuList(tsize) # tabu list
    t.insert(s)
    si = neightborhood(s)
    for _ in range(iter):
        sn = select_Best(si)
        if bp.state_Value(sn) < bp.state_Value(bs):
            sn = take_Random_Tabu(neightborhood(ps),t)
            # print(neightborhood(ps))
            if sn == []:
                break
        if bp.state_Verify(sn) and bp.state_Value(sn) > bp.state_Value(bs):
            bs = sn
        si = neightborhood(sn)
        ps = sn
    return bs

iter = 50            # number of iterations
tsize = 10           # max size of tabu list
s = [0]*len(bp.OBJs) # initial state
print(tabu_Search(s,tsize,iter))