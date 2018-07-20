from kirbyClass import *
from crossingClass import *
from strandClass import *
from componentClass import *

class join:
    
    def __init__(self,strand0,strand1): #sets up join from 2 strands
        self.strands=[strand0,strand1]

    def __getitem__(self,key): #returns either 0th strand or 1st strand
        return(self.strands[key])

    def __contains__(self,item): #returns true/false if strand is in join
        return(item in self.strands)

    def __str__(self):
<<<<<<< HEAD
        return ("["+str(self.strands[0])+","+str(self.strands[1])+"]")
=======
        return ("[" + str(strand0) + "," + str(strand1) + "]")
>>>>>>> 924038fd8c82e0aedc2a82cf23314fd3b6e75703

    def set_strands(self,strand0,strand1): #sets strands for join
        self.strands=[strand0,strand1]

    def get_strands(self): #returns strands for join as a list
        return(self.strands)
