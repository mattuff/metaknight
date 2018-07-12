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

    def strandLookup(self,strand): #gives a weird output?
        l=[]
        for c in self.crossings:
            if(strand in c):
                l.append(c)
        for j in self.joins:
            if(strand in j):
                l.append(j)
        return(l)

       def add_r1(self, strand, orientation):
        count=0
        for i in self.crossings:
            for j in range (4):
                if (i[j]==strand and count<1):
                    i[j]=(arc+"a")
                    count=count+1
                elif (i[j]==strand and count<2):
                    i[j]=(arc+"b")
                    count=count+1
        c=crossing(arc,arc,arc+"a", arc+"b")
        crossings.append(c)
