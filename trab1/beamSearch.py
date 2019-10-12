## -------------------------------------------------------- ##
#   Trab 1 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   beamSearch.py: implements the beam search metaheuristic for the bag problem
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
import queue
from time import time

# Return a list with the n best states of the given state's expansion:
def select_Best_States(n, st, T, OBJs):
    si = bp.state_Expansion(st)
    si = [[bp.state_Value(s, OBJs),s] for s in si]
    si.sort(reverse=True)
    si = [i[1] for i in si]
    bss = []
    for i in si:
        if bp.state_Verify(i, T, OBJs):
            bss.append(i)
    return bss[:n]

# Beam Search:
def beam_Search(T, OBJs, execTime, *args):
    m = args[0]
    f = queue.Queue(m)
    f.put([0]*len(OBJs)) # starting queue with the initial state
    bs = [0]*len(OBJs)   # starting best state as initial state
    start = time()
    while f.qsize() > 0:
        if time() - start > execTime:
            break
        st = f.get()
        if bp.state_Value(st, OBJs) > bp.state_Value(bs, OBJs):
            bs = st
        si = select_Best_States(m-f.qsize(), st, T, OBJs)
        for i in si:
            f.put(i)
    return bs

# T = 19 # bag size
# OBJs = [(1,3), (4,6), (5,7)] # object list (v,t)
# print(beam_Search(T,OBJs,5))
