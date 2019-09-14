## -------------------------------------------------------- ##
#   Basic functions for the Bag Problem
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

T = 19 # bag size

OBJs = [(1,3), (4,6), (5,7)] # object list (v,t)

# Returns the value(v) of a object:
def value(obj):
    return obj[0]

# Returns the size(t) of a object:
def size(obj):
    return obj[1]

# Returns the value of a state:
def state_Value(st):
    v = 0
    for i in range(len(st)):
        v += st[i] * value(OBJs[i])
    return v

# Returns the size of a state:
def state_Size(st):
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
def state_Verify(st):
    if state_Size(st) <= T:
        return True
    return False