class crossing:
    
    def __init__(self,strand0,strand1,strand2,strand3):
        self.strands=[strand0,strand1,strand2,strand3]

    def __getitem__(self,key): #key is 0-3 (int), returns strand
        return(self.strands[key])

    def __contains__(self,item): #returns boolean- True if 'item' is in the crossing
        return(item in self.strands)

    def __str__(self):
        return ("[", strand0, "," strand1, ",", strand2, "," strand3, "]")

    def set_strands(self,strand0,strand1,strand2,strand3): #define new strands that come out of crossing
        self.strands=[strand0,strand1,strand2,strand3] 

    def get_strands(self): #returns the strands
        return(self.strands)
