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

    def get_strands(self,comp):
       s=[]
       for i in self.crossings:
          for j in range (4):
             if (i[j].get_component()==comp and i[j] not in s):
                s.append(i[j])
       for k in self.joins:
          for l in range (2):
             if (k[l].get_component()==comp and k[l] not in s):
                s.append(k[l])
      return s

    def strand_lookup(self,strand): #gives a weird output? #returns list of crossings/joins that a specific strand shows up in
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
          x.get_succ().set_pred(y) #sets x's old successor's pred to be y
          x.set_succ(y) #sets x's successor to y
          jx=join(x,y) #creates join of [x,y]
          self.joins.append(jx) #adds new join to join list
          #search for crossings containing both x and y.get_succ(), replaces x w/ y
         c=list(set(strand_lookup(x)), set(strand_lookup(y.get_succ())[0] #finds crossing containing x and y.get_succ()
         self.crossings.remove(c) 
         if c.getitem(0)==x: #if x is the ith strand in the crossing
              c.set_strands(y, c.getitem(1), c.getitem(2), c.getitem(3)) #then replace strand w strand.get_succ().get_succ()
         elif c.getitem(1)==x:
             c.set_strands(c.getitem(0), y, c.getitem(2), c.getitem(3))
         elif c.getitem(2)==x:
             c.set_strands(c.getitem(0), c.getitem(1), y, c.getitem(3))
         elif c.getitem(3)==x:
             c.set_strands(c.getitem(0), c.getitem(1), c.getitem(2), y)
         self.crossings.append(c)
          #return new strand?

     def remove_join(self,j1):
         self.joins.remove(j1)
         x=j1[0]
         y=j1[1]
         getitem(j1,0).set_succ(getitem(j1,1).get_succ())) #set's x's succ to be y's succ
         getitem(j1,1).get_succ().set_pred(getitem(j1,0)) #set's y succ's pred to be x
        #search crossings for y, replace w x
         c=strand_lookup(y)[0]
         self.crossings.remove(c) 
         if c.getitem(0)==y: #if x is the ith strand in the crossing
              c.set_strands(x, c.getitem(1), c.getitem(2), c.getitem(3)) #then replace strand w strand.get_succ().get_succ()
         elif c.getitem(1)==y:
             c.set_strands(c.getitem(0), x, c.getitem(2), c.getitem(3))
         elif c.getitem(2)==y:
             c.set_strands(c.getitem(0), c.getitem(1), x, c.getitem(3))
         elif c.getitem(3)==y:
             c.set_strands(c.getitem(0), c.getitem(1), c.getitem(2), x)
         self.crossings.append(c)                

def add_r1(self,strand, sign): #strand=strand to twist, sign=clockwise or counterclockwise twist (1 will add 1 to framing, -1 will subtract 1 from framing)
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

def remove_r1(self,s) #s: crossed strand for r1
   c=self.strand_lookup(s)[0]
   if (c.getitem(2)==c.getitem(3) or (c.getitem(0)==c.getitem(1)):
          self.crossings.remove(c) #remove crossing
          self.joins.append([s.get_prec(), s]) #adds join
          self.joins.append([s, s.get_succ()]) #adds join
          remove_join([s.get_prec(), s]) #removes join; does relabling
          remove_join([s, s.get_succ()]) #removes join; does relabling
          s.get_component().change_framing(s.get_component().get_framing()+1) #add 1 to framing
   elif (c.getitem(0)==c.getitem(3) or c.getitem(1)==c.getitem(2)):
         self.crossings.remove(c) #remove crossing
          self.joins.append([s.get_prec(), s]) #adds join
          self.joins.append([s, s.get_succ()]) #adds join
          remove_join([s.get_prec(), s]) #removes join; does relabling
          remove_join([s, s.get_succ()]) #removes join; does relabling
          s.get_component().change_framing(s.get_component().get_framing()-1) #subracts 1 from framing


   def add_r2(self,strand1,strand2,orientation) #orientation is a boolean which is true if the strands are oriented the same way, and false otherwise
      #add two joins to each strand
      #add two crossings
      #remove joins
      self.add_join(strand1)
      self.add_join(strand1)
      self.add_join(strand2)
      self.add_join(strand2)
      l=(self.strand_lookup(strand1.get_succ()))+(self.strand_lookup(strand2.get_succ()))
      if(orientation):
         c1=crossing(strand1,strand2.get_succ(),strand1.get_succ(),strand2)
         c2=crossing(strand1.get_succ(),strand2.get_succ(),strand1.get_succ().get_succ(),strand2.get_succ().get_succ())
      else:
         c1=crossing(strand1,strand2.get_succ().get_succ(),strand1.get_succ(),strand2.get_succ())
         c2=crossing(strand1.get_succ(),strand2,strand1.get_succ().get_succ(),strand2.get_succ())
      self.crossings+=[c1,c2]
      for s in l:
         self.joins.remove(s)

   def remove_r2 (self,crossing1, crossing2)
      #remove two crossings
      #remove joins

   def r3(self,strand, crossing)
         
   def handle_annihilation(self,h1, h2)
       #checks to make sure each handle only has 2 strands (all joins must be removed)
       if (len(self.get_strands(h1))!==2 or len(self.get_strands(h2))!==2): 
          print ("Handles can't be cancelled.")
       #makes sure h1 and h2 only have crossings with each other
       elif (self.strand_lookup(self.getstrands(h1)[0])[0] not in self.strand_lookup(self.getstrands(h2)[0])):
          print ("Handles can't be cancelled.")
       elif (self.strand_lookup(self.getstrands(h1)[0])[0] not in self.strand_lookup(self.getstrands(h2)[1])):
          print ("Handles can't be cancelled.")
       elif (self.strand_lookup(self.getstrands(h1)[0])[1] not in self.strand_lookup(self.getstrands(h2)[0])):
          print ("Handles can't be cancelled.")
       elif (self.strand_lookup(self.getstrands(h1)[0])[1] not in self.strand_lookup(self.getstrands(h2)[1])):
          print ("Handles can't be cancelled.")
       #delete crossings
       self.crossings.remove(self.strand_lookup(self.getstrands(h1)[0])[0])
       self.crossings.remove(self.strand_lookup(self.getstrands(h1)[0])[1])
       #deletes components
       self.components.remove(h1)
       self.components.remove(h2)
