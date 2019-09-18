## -------------------------------------------------------- ##
#   Exercise 8: Genetic Algorithm
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import bagProblem as bp

# Returns a initial population:
def init_Population():

# Generates a new population:
def generate_New_Pop(si):

# Select the most fit states in the given population:
def select_Most_Fit(si):

# Returns the best state in the population:
def best_in_Pop(si):

# Genetic Algorithm:
def genetic(n, iter):
    si = init_Population()
    bs = [0]*len(bp.OBJs)
    for _ in range(iter):
        ss = generate_New_Pop(select_Most_Fit(si))
        s = best_in_Pop(ss)
        if bp.state_Verify(s) and bp.state_Value(s) > bp.state_Value(bs):
            bs = s
    return bs

iter = 50
n = 10
print(genetic(n,iter))
