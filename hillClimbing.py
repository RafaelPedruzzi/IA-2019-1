T = 19 # tamanho da mochila.

# (V,T)
OBJs = [(1,3), (4,6), (5,7)]

def value(obj):
    return obj[0]

def size(obj):
    return obj[1]

def state_Value(st,objs):
    v = 0
    for i in range(len(st)):
        v += st[i] * value(objs[i])
    return v

def state_Size(st,objs):
    s = 0
    for i in range(len(st)):
        s += st[i] * size(objs[i])
    return s

def state_Expansion(st):
    si = []
    for i in range(len(st)):
        saux = st.copy()
        saux[i] += 1
        si.append(saux)
    return si

def state_Verify(st,T,objs):
    if state_Size(st,objs) <= T:
        return True
    return False

def state_Select(si,T,objs):
    sn = -1
    sv = 0 # state value
    for i in range(len(si)):
        v = state_Value(si[i],objs) # current value
        if state_Verify(si[i],T,objs) and v > sv:
            sv = v
            sn = i
    if sn == -1:
        return False, []
    return True, si[sn]

def hill_Climbing(T,objs):
    sn = [0]*len(objs) # next state
    x = True
    while x:
        st = sn
        x, sn = state_Select(state_Expansion(st), T, objs)
    return st

print(hill_Climbing(T,OBJs))
