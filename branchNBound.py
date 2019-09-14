## -------------------------------------------------------- ##
#   Exercise 3: Branch and Bound
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import hillClimbing as hc
import bagProblem as bp
import priorityQ as pq

# Return a trivial solution to the problem:
def triv_solution():
    return hc.hill_Climbing()

# Optimistic estimate of status cost (Kelvin's algorithm):
def opt_Estimate(status):
    # Selecting the most cost-effective object:
    w = [o[0]/o[1] for o in bp.OBJs]
    e = w.index(max(w))
    # Filling the given status with it:
    s = status.copy()
    while bp.state_Verify(s):
        s[e] += 1
    return s

# Non-optimistic estimate of status cost (Kelvin's algorithm -1):
def n_Opt_Estimate(status):
    # Selecting the most cost-effective object:
    w = [o[0]/o[1] for o in bp.OBJs]
    e = w.index(max(w))
    # Filling the given status with it:
    s = status.copy()
    while bp.state_Verify(s):
        s[e] += 1
    s[e] -= 1 # making s valid
    return s

# Branch and Bound:
def branch_n_bound(use_opt_estimate=True):
    bs = triv_solution()          # best state found
    sv = bp.state_Value(bs)       # value of best bs
    pq.insert(0,[0]*len(bp.OBJs)) # pushing initial state in queue
    while not pq.isEmpty():
        cs = pq.remove() # current state
        si = bp.state_Expansion(cs) # expansion of current state
        for s in si:
            if bp.state_Verify(s):
                if use_opt_estimate: # selecting estimate method
                    est = opt_Estimate(s)
                else:
                    est = n_Opt_Estimate(s)
                if bp.state_Value(est) > sv:
                    if bp.state_Value(s) > sv:
                        bs = s # updating best bs
                        sv = bp.state_Value(s) # updating best value
                    pq.insert(bp.state_Value(s),s)
    return bs

print("optimist =", branch_n_bound())
print("n optimist =", branch_n_bound(False))
