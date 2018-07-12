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
        return(str(l))
  
     
     def add_joins(self, x):
          y=strand(x.get_component(), x.get_succ(), x)
          x.set_succ(y)
          jx=join(x,y)
          self.joins(x,y)





      def add_r1(strand):
      
        #initialize 2 new strands, no succ or pred yet (fix these lines - maybe do this later with suc and pred)
         newStrand1 = strand(newStrand1)
         newStrand2 = strand(newStrand2)
         
        for i in self.crossings: #go through all the nodes
           for j in range(4):    #for each node, go through the 4 edges coming out of it
               if i[j] == strand: #we reached the strand we wish to twist
                  #we have 2 crossings: the crossing with strand.succ and the crossing with strand.prec. 
               
      
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
        f=strand.get_knot.getFraming()
        strand.get_knot.changeFraming(f+1)
