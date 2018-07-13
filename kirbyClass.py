class Kirby:

   def __init__(self,crossings,joins):
        self.crossings=crossings
        self.joins=joins
        strands=[] #makes list of strands
        for c in crossings:
            for i in range(4):
                if(c[i] not in strands):
                    strands.append(c[i])
        for j in joins:
            for i in range(2):
                if(j[i] not in strands):
                    strands.append(j[i])
                  
    def __str__(self): #check if this helps return the str instead of the memory location
        return('crossings: ' + str(self.crossings) + ', joins: ' + str(self.joins))

    def strandLookup(self,strand): #gives a weird output? #returns list of crossings/joins that a specific strand shows up in
        l=[]
        for c in self.crossings:
            if(strand in c):
                l.append(c)
        for j in self.joins:
            if(strand in j):
                l.append(j)
        return(str(l))
  
     
     def add_join(self, x): #adds a join to a strand (splitting it into two different strands)
          y=strand(x.get_component(), x.get_succ(), x) #adds strand after x
          x.set_succ(y) #sets x's successor to y
          jx=join(x,y) #creates join of [x,y]
          self.joins.append(jx) #adds new join to join list
          #return new strand?

       def remove_join(j1):
         self.joins.remove(j1)
         getitem(j1,0).set_succ(getitem(j1,1).get_succ())) #set's x's succ to be y's succ
         getitem(j1,1).get_succ().set_pred(getitem(j1,0)) #set's y succ's pred to be x
         #search crossings for y, replace w x


      def add_r1(strand, sign):
      """
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
        strand.get_knot.changeFraming(f+1)"""
      #add two joins to strand using add_join method
      self.add_join(strand) #strand1
      self.add_join(strand) #strand2
      if (sign==1):
         #add crossing [strand2, strand, strand1, strand2]
         #strand.get_component().change_framing(strand.get_component().get_framing()+1)
      elif (sign==-1):
         #add crossing [strand, strand1, strand2, strand2]
         #strand.get_component().change_framing(strand.get_component().get_framing()-1)
      #remove joins added from join list but not using the remove join function
      #replace other crossing that strand shows up in w strand1   

   def remove_r1(crossing)
      #remove crossing
      #remove two joins
      #change framing: add/subtract 1

   def add_r2(strand1, strand2)
      #add two joins to each strand
      #add two crossings
      #remove joins

   def remove_r2 (crossing1, crossing2)
      #remove two crossings
      #remove joins

   def r3(strand, crossing)
         
   
