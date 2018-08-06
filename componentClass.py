from kirbyClass import *
from crossingClass import *
from joinClass import *
from strandClass import *

class component:

    def __init__(self, h, f=None): #for 1-handles, framing=infinity
        self.handle = h
        self.framing = f
        
    def __str__(self): #prints out component in nice way
        return('handle: ' + str(self.handle) + ', framing: ' + str(self.framing))
    
    def __getitiem__(self,key):
        return(list(filter(lambda x:x.component==s.component,k.strands))[key])


    def get_handle(self): #returns type of handle: one or two handle
        return self.handle

    def get_framing(self): #returns framing of 2-handles
        return self.framing

    def change_framing(self, f): #changes framing of 2-handles
        self.framing=f
