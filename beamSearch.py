## -------------------------------------------------------- ##
#   Exercise 2: Beam Search
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
import queue

# Return a list with the n best states of the given state's expansion:
def select_Best_States(n, st):
    si = bp.state_Expansion(st)
    si = [[bp.state_Value(s),s] for s in si]
    si.sort(reverse=True)
    si = [i[1] for i in si]
    bss = []
    for i in filter(bp.state_Verify, si):
        bss.append(i)
    return bss[:n]

# Beam Search:
def beam_Search(m):
    f = queue.Queue(m)
    f.put([0]*len(bp.OBJs)) # starting queue with the initial state
    bs = [0]*len(bp.OBJs)   # starting best state as initial state
    while f.qsize() > 0:
        st = f.get()
        if bp.state_Value(st) > bp.state_Value(bs):
            bs = st
        si = select_Best_States(m-f.qsize(), st)
        for i in si:
            f.put(i)
    return bs

print(beam_Search(5))
