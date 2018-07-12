class kirby:

   def __init__(self,crossings,joins):
        self.crossings=crossings
        self.joins=joins
        strands=[]
        for c in crossings:
            for i in range(4):
                if(c[i] not in strands):
                    strands.append(c[i])
        for j in joins:
            for i in range(2):
                if(j[i] not in strands):
                    strands.append(j[i])

    def strandLookup(self,strand):
        l=[]
        for c in self.crossings:
            if(strand in c):
                l.append(c)
        for j in self.joins:
            if(strand in j):
                l.append(j)
        return(l)
