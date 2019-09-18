## -------------------------------------------------------- ##
#   Exercise 7: Simulated Annealing
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp
import hillClimbing as hc
import priorityQ as pq
import random
import math

# Return a trivial solution to the problem:
def triv_solution():
    return hc.hill_Climbing()

# Remove and return a random item from the given list:
def take_Random(si):
    if si == []:
        return []
    return si.pop(random.randint(0,len(si)-1))

# Return a neightborhood of the given state
def neightborhood(s):
    neig = []
    for i in bp.state_Expansion(s): # add all valid states from the expansion of the given state
        if bp.state_Verify(i):
            neig.append(i)
    for i in neig:                    # adding all valid retractions of each state currently in the neightborhood
        for j in bp.state_Retract(i):
            if bp.state_Verify(j):
                neig.append(j)
    for i in bp.state_Retract(s): # add all valid states from the retraction of the given state
        if bp.state_Verify(i):
            neig.append(i)
    return neig

# Simulated Anneling:
def sim_Annealing(s,temp,iter):
    bs = s # best state found
    alpha = random.random() # random value in [0,1]
    while temp > 1:
        si = neightborhood(s)
        for _ in range(iter):
            sn = take_Random(si)
            if bp.state_Value(sn) > bp.state_Value(s):
                s = sn
                si = neightborhood(s) # updating neightborhood
                if bp.state_Value(sn) > bp.state_Value(bs):
                    bs = sn
            else:
                p = math.exp((bp.state_Value(sn) - bp.state_Value(s))/temp)
                if random.random() < p:
                    s = sn
                    si = neightborhood(s) # updating neightborhood
        temp *= alpha
    return bs

temp = 10 # initial temperature
iter = 50 # number of iterations
s = triv_solution() # starting value

print(sim_Annealing(s,temp,iter))
