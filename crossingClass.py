class crossing:
    
    def __init__(self,strand0,strand1,strand2,strand3):
        self.strands=[strand0,strand1,strand2,strand3]

    def __getitem__(self,key):
        return(self.strands[key])

    def setStrands(self,strand0,strand1,strand2,strand3):
        self.strands=[strand0,strand1,strand2,strand3]

    def getStrands(self):
        return(self.strands)
