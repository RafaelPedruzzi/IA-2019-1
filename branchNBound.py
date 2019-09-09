## -------------------------------------------------------- ##
#   Exercício 3: Branch and Bound
#
#   Rafael Belmock Pedruzzi
## -------------------------------------------------------- ##

import hillClimbing as hc
import priorityQ as pq

def triv_Solution(T,objs):
    return hc.hill_Climbing()

def opt_Estimate(status):

def branch_n_bound():
    solution = triv_Solution()
    sv = hc.state_Value(solution) # value of best solution
    pq.pq_insert(0,[0]*len(hc.OBJs)) # inserting initial state in queue
    while pq.isEmpty() == False:
        cs = pq.remove() # current state
        si = hc.state_Expansion(cs) # expansion of current state
        for s in si:
            if hc.state_Verify(s):
                if hc.state_Value(opt_Estimate(s)) > sv:
                    if hc.state_Value(s) > sv:
                        solution = s # updating best solution
                        sv = hc.state_Value(s) # updating best value
                    pq.insert(sv,s)
    return solution
