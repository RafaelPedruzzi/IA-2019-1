## -------------------------------------------------------- ##
#   Exercise 7: Tabu Search
#
#   Rafael Belmock Pedruzzi
#
#   tabuList.py: implements a tabu list
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

class tabuList:
    states = [] # states list
    size = 0    # max number of elements on the list
    lenght = 0  # current lenght of the list
    
    def __init__(self, size):
        self.size = size
        for _ in range(size):
            self.states.append([])

    # Insert a state on the list:
    def insert(self, s):
        self.states[self.lenght] = s
        self.lenght += 1
        self.lenght %= self.size
    
    # Checks if a state is in the list:
    def is_in(self, s):
        return s in self.states