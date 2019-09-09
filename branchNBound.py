import hillClimbing as hc
import priorityQ as pq


def triv_Solution(T,objs):
    return hc.hill_Climbing(T,objs)

def opt_Estimate(status, objs, T):

def branch_n_bound(T,objs):
    solution = triv_Solution(T,objs)
    sv = hc.state_Value(solution)
    pq.pq_insert(0,[0]*len(objs)) # inserting initial state in queue
    while pq.isEmpty() == False:
        cs = pq.remove() # current state
        si = hc.state_Expansion(cs) # expansion of current state
        for s in si:
            if hc.state_Verify(s):
                if hc.state_Value(opt_Estimate(s, T, objs), objs) > sv:
                    if hc.state_Value(s,objs) > sv:
                        solution = s
                        sv = hc.state_Value(s,objs)
                    pq.insert(s)
        return solution
