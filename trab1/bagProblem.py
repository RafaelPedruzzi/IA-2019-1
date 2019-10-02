## -------------------------------------------------------- ##
#   Trab 1 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   bagProblem.py: Basic functions for the Bag Problem
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

# Returns the value(v) of a object:
def value(obj):
    return obj[0]

# Returns the size(t) of a object:
def size(obj):
    return obj[1]

# Returns the value of a state:
def state_Value(st, OBJs):
    v = 0
    for i in range(len(st)):
        v += st[i] * value(OBJs[i])
    return v

# Returns the size of a state:
def state_Size(st, OBJs):
    s = 0
    for i in range(len(st)):
        s += st[i] * size(OBJs[i])
    return s

# Returns a list with all possible retractions of a state without negative values:
def state_Retract(st):
    si = []
    for i in range(len(st)):
        saux = st.copy()
        if saux[i] > 0:
            saux[i] -= 1
            si.append(saux)
    return si

# Returns a list with all possible expansions of a state:
def state_Expansion(st):
    si = []
    for i in range(len(st)):
        saux = st.copy()
        saux[i] += 1
        si.append(saux)
    return si

# Check if a state is valid:
def state_Verify(st, T, OBJs):
    if state_Size(st, OBJs) <= T:
        return True
    return False