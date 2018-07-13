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

    def strand_lookup(self,strand): #gives a weird output? #returns list of crossings/joins that a specific strand shows up in
        l=[]
        for c in self.crossings:
            if(strand in c):
                l.append(c)
        for j in self.joins:
            if(strand in j):
                l.append(j)
        return l
  
     
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


   def add_r1(strand, sign): #strand=strand to twist, sign=clockwise or counterclockwise twist (1 will add 1 to framing, -1 will subtract 1 from framing)
      #add two joins to strand using add_join method
      self.add_join(strand) #strand.get_succ().get_succ() (strand1)
      self.add_join(strand) #strand.get_succ() (strand2)
      if (sign==1):
         self.crossings.append([strand.get_succ(), strand, strand.get_succ().get_succ(), strand.get_succ()]) #adds crossing
         strand.get_component().change_framing(strand.get_component().get_framing()+1)
      elif (sign==-1):
         self.crossings.append([strand, strand.get_succ().get_succ(), strand.get_succ(), strand.get_succ()])
         strand.get_component().change_framing(strand.get_component().get_framing()-1)
      #remove joins added from join list but not using the remove join function
      self.joins.remove([strand, strand.get_succ()])
      self.joins.remove([strand.get_succ(), strand.get_succ().get_succ()])
      #replace other crossing that strand shows up in w strand1
      c=list(set(strand_lookup(strand)), set(strand_lookup(strand.get_succ().get_succ().get_succ()))[0] #finds crossing containing strand and strand's old succ
      self.crossings.remove(c) 
      if getitem(c,0)==strand: #if strand is the ith strand in the crossing
             c.set_strands(strand.get_succ().get_succ(), getitem(c,1), getitem(c,2), getitem(c,3)) #then replace strand w strand.get_succ().get_succ()
      elif getitem(c,1)==strand:
             c.set_strands(getitem(c,0), strand.get_succ().get_succ(), getitem(c,2), getitem(c,3))
      elif getitem(c,2)==strand:
             c.set_strands(getitem(c,0), getitem(c,1), strand.get_succ().get_succ(), getitem(c,3))
      elif getitem(c,3)==strand:
             c.set_strands(getitem(c,0), getitem(c,1), getitem(c,2), strand.get_succ().get_succ())
      self.crossings.append(c)

   def remove_r1(c, sign) #c: crossing for r1, sign=if the r1 added or subtracted 1 from framing
      #remove crossing: [a, b, b, c] or something
      self.crossings.remove(c)
      s=getitem(c,0).get_component()
      #add joins [a,b] and [b,c] (not using add joins method)
      #remove joins [a,b] and [b,c] using remove joins method --> takes care of relabling 
      #change framing: add/subtract 1
      if (sign==1):
             s.change_framing(s.get_framing()-1)
      elif (sign==-1):
             s.change_framing(s.get_framing()+1)

   def add_r2(strand1, strand2)
      #add two joins to each strand
      #add two crossings
      #remove joins

   def remove_r2 (crossing1, crossing2)
      #remove two crossings
      #remove joins

   def r3(strand, crossing)
         
   
