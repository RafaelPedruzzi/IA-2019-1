## -------------------------------------------------------- ##
#   Exercício 3: Branch and Bound
#
#   Rafael Belmock Pedruzzi
## -------------------------------------------------------- ##

import hillClimbing as hc
import priorityQ as pq

# Return a trivial solution to the problem:
def triv_Solution():
    return hc.hill_Climbing()

# Optimistic estimate of status cost (Kelvin function):
def opt_Estimate(status):
    # Selecting the most cost-effective object:
    w = [o[0]/o[1] for o in hc.OBJs]
    e = w.index(max(w))
    # Filling the given status with it:
    s = status.copy()
    while hc.state_Verify(s):
        s[e] += 1
    return s

# Non-optimistic estimate of status cost (Kelvin function -1):
def n_Opt_Estimate(status):
    # Selecting the most cost-effective object:
    w = [o[0]/o[1] for o in hc.OBJs]
    e = w.index(max(w))
    # Filling the given status with it:
    s = status.copy()
    while hc.state_Verify(s):
        s[e] += 1
    s[e] -= 1 # making s valid
    return s

# Branch and Bound:
def branch_n_bound(use_opt_estimate=True):
    solution = triv_Solution()
    sv = hc.state_Value(solution) # value of best solution
    pq.insert(0,[0]*len(hc.OBJs)) # pushing initial state in queue
    while pq.isEmpty() == False:
        cs = pq.remove() # current state
        si = hc.state_Expansion(cs) # expansion of current state
        for s in si:
            if hc.state_Verify(s):
                if use_opt_estimate: # selecting estimate method
                    est = opt_Estimate(s)
                else:
                    est = n_Opt_Estimate(s)
                if hc.state_Value(est) > sv:
                    if hc.state_Value(s) > sv:
                        solution = s # updating best solution
                        sv = hc.state_Value(s) # updating best value
                    pq.insert(hc.state_Value(s),s)
    return solution

print("opt =", branch_n_bound())
print("n opt =", branch_n_bound(False))
