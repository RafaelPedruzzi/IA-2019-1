## -------------------------------------------------------- ##
#   Exercise 7: Simulated Annealing
#
#   Rafael Belmock Pedruzzi
## -------------------------------------------------------- ##

import bagProblem as bp
import hillClimbing as hc
import priorityQ as pq
import random
import math

# Return a trivial solution to the problem:
def triv_Solution():
    return hc.hill_Climbing()

# Remove and return a random state from the list:
def take_Random(si):
    if si == []:
        return []
    return si.pop(random.randint(0,len(si)-1))

def neightborhood(s):
    neig = []
    for i in bp.state_Expansion(s):
        if bp.state_Verify(i):
            neig.append(i)
    for i in bp.state_Retract(s):
        if bp.state_Verify(i):
            neig.append(i)
    return neig

# Simulated Anneling:
def sim_Annealing(s,temp,iter):
    solution = s
    alpha = random.random()
    while temp > 1:
        si = neightborhood(s)
        for i in range(iter):
            sn = take_Random(si)
            if bp.state_Value(sn) > bp.state_Value(s):
                s = sn
                si = neightborhood(s)
                if bp.state_Value(sn) > bp.state_Value(solution):
                    solution = sn
            else:
                p = math.exp((bp.state_Value(sn) - bp.state_Value(s))/temp)
                if random.random() < p:
                    s = sn
                    si = neightborhood(s)
        temp *= alpha
    return solution

temp = 10
iter = 50
s = triv_Solution()

print(sim_Annealing(s,temp,iter))
