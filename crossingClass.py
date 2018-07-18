class crossing:
    
    def __init__(self,s0,s1,s2,s3):
        self.strands=[s0,s1,s2,s3]

    def __getitem__(self,key): #key is 0-3 (int), returns strand
        return(self.strands[key])

    def __contains__(self,item): #returns boolean- True if 'item' is in the crossing
        return(item in self.strands)

    def __str__(self): #method doesn't work!!
        return ("["+str(s0)+","+str(s1)+","+str(s2)+","+str(s3)+"]")

    def set_strands(self,s0,s1,s2,s3): #define new strands that come out of crossing
        self.strands=[s0,s1,s2,s3] 

    def get_strands(self): #returns the strands
        return(self.strands)
