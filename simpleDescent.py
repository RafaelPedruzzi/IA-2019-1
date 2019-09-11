## -------------------------------------------------------- ##
#   Exercício 4: Simple Descent
#
#   Rafael Belmock Pedruzzi
## -------------------------------------------------------- ##

import hillClimbing as hc

def state_Retract(st):
    si = []
    for i in range(len(st)):
        saux = st.copy()
        if saux[i] > 0:
            saux[i] -= 1
        si.append(saux)
    return si

def sd_State_Select():

def simple_Descent():