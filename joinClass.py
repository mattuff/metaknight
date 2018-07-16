class join:
    
    def __init__(self,strand0,strand1): #sets up join from 2 strands
        self.strands=[strand0,strand1]

    def __getitem__(self,key): #returns either 0th strand or 1st strand
        return(self.strands[key])

    def __contains__(self,item): #returns true/false if strand is in join
        return(item in self.strands)

    def set__Strands(self,strand0,strand1): #sets strands for join
        self.strands=[strand0,strand1]

    def get__Strands(self): #returns strands for join as a list
        return(self.strands)
