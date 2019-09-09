## -------------------------------------------------------- ##
#   Exercício 2: Beam Search
#
#   Rafael Belmock Pedruzzi
## -------------------------------------------------------- ##

import hillClimbing as hc
import queue

# Return a list with the n best states of the given state's expansion:
def select_Best_States(n, st):
    si = hc.state_Expansion(st)
    si = [[hc.state_Value(s),s] for s in si]
    si.sort(reverse=True)
    si = [i[1] for i in si]
    si = filter(hc.state_Verify, si)
    return si[:n]

# Beam Search:
def beam_Search(m):
    f = queue.Queue(m)
    f.put([0]*len(hc.OBJs)) # starting queue with the initial state.
    solution = [0]*len(hc.OBJs)
    while f.qsize() > 0:
        st = f.get()
        if hc.state_Value(st) > hc.state_Value(solution):
            solution = st
        si = select_Best_States(m-f.qsize(), st)
        for i in si:
            f.put(i)
    return solution
