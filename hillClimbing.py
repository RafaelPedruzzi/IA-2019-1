## -------------------------------------------------------- ##
#   Exercício 1: Hill Climbing
#
#   Rafael Belmock Pedruzzi
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

# Returns True and the valid state with the biggest value, or False if no state is valid:
def state_Select(si):
    sn = -1
    sv = 0 # state value
    for i in range(len(si)):
        v = state_Value(si[i]) # current value
        if state_Verify(si[i]) and v > sv:
            sv = v
            sn = i
    if sn == -1:
        return False, []
    return True, si[sn]

# Hill Climbing:
def hill_Climbing():
    sn = [0]*len(OBJs) # initial state
    x = True
    while x:
        cs = sn # storing current state
        x, sn = state_Select(state_Expansion(cs))
    return cs

# print(hill_Climbing())
