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

   def print_pd(self):
      for c in self.crossings:
         print ("[", end =" ")
         for i in range (4):
            if (i<3):
               print (c[i], ", ", end =" ")
            else:
               print (c[i], end =" ")
         print ("]")
      for j in self.joins:
         print ("[", end =" ")
         for k in range (2):
            if (k<1):
               print (j[k], ", ", end =" ")
            else:
               print(j[k], end =" ")
         print ("]")

   def get_strands(self,comp):
      s=[]
      for i in self.crossings:
         for j in range (4):
            if (i[j].component==comp and i[j] not in s):
               s.append(i[j])
      for k in self.joins:
         for l in range (2):
            if (k[l].component==comp and k[l] not in s):
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
      return l
  
     
   def add_join(self, x): #adds a join to a strand (splitting it into two different strands)
      y=strand(x.component, x.succ, x) #adds strand w pred x and succ x's succ
      x.succ.set_pred(y) #sets x's old successor's pred to be y
      x.set_succ(y) #sets x's successor to y
      jx=join(x,y) #creates join of [x,y]
      self.joins.append(jx) #adds new join to join list
      #search for crossings containing both x and y.get_succ(), replaces x w/ y
      c=list(set(self.strand_lookup(x))&set(self.strand_lookup(y.succ)))[0] #finds crossing containing x and y.get_succ()
      self.crossings.remove(c) 
      if c[0]==x: #if x is the ith strand in the crossing
         c.set_strands(y, c[1], c[2], c[3]) #then replace strand w strand.get_succ().get_succ()
      elif c[1]==x:
         c.set_strands(c[0], y, c[2], c[3])
      elif c[2]==x:
         c.set_strands(c[0], c[1], y, c[3])
      elif c[3]==x:
         c.set_strands(c[0], c[1], c[2], y)
      self.crossings.append(c)
      #return new strand?

   def remove_join(self,j1):
      self.joins.remove(j1)
      x=j1[0]
      y=j1[1]
      j1[0].set_succ(j1[1].succ) #set's x's succ to be y's succ
      j1[1].succ.set_pred(j1[0]) #set's y succ's pred to be x
      #search crossings for y, replace w x
      c=self.strand_lookup(y)[0]
      self.crossings.remove(c) 
      if c[0]==y: #if x is the ith strand in the crossing
         c.set_strands(x, c[1], c[2], c[3]) #then replace strand w strand.get_succ().get_succ()
      elif c[1]==y:
         c.set_strands(c[0], x, c[2], c[3])
      elif c[2]==y:
         c.set_strands(c[0], c[1], x, c[3])
      elif c[3]==y:
         c.set_strands(c[0], c[1], c[2], x)
      self.crossings.append(c)                

   def add_r1(self,strand, sign): #strand=strand to twist, sign=clockwise or counterclockwise twist (1 will add 1 to framing, -1 will subtract 1 from framing)
      #add two joins to strand using add_join method
      self.add_join(strand) #strand.get_succ().get_succ() (strand1)
      self.add_join(strand) #strand.get_succ() (strand2)
      if (sign==1):
         self.crossings.append([strand.succ, strand, strand.succ.succ, strand.succ]) #adds crossing
         strand.component.change_framing(strand.component.framing+1)
      elif (sign==-1):
         self.crossings.append([strand, strand.succ.succ, strand.succ, strand.succ])
         strand.component.change_framing(strand.component.framing-1)
      #remove joins added from join list but not using the remove join function
      self.joins.remove([strand, strand.succ])
      self.joins.remove([strand.succ, strand.succ.succ])

   def remove_r1(self,s): #s: crossed strand for r1
      c=self.strand_lookup(s)[0]
      if (c[2]==c[3] or (c[0]==c[1])):
         self.crossings.remove(c) #remove crossing
         self.joins.append([s.pred, s]) #adds join
         self.joins.append([s, s.succ]) #adds join
         remove_join([s.pred, s]) #removes join; does relabling
         remove_join([s, s.succ]) #removes join; does relabling
         s.component.change_framing(s.component.framing+1) #add 1 to framing
      elif (c[0]==c[3] or c[1]==c[2]):
         self.crossings.remove(c) #remove crossing
         self.joins.append([s.pred, s]) #adds join
         self.joins.append([s, s.succ]) #adds join
         remove_join([s.pred, s]) #removes join; does relabling
         remove_join([s, s.succ]) #removes join; does relabling
         s.component.change_framing(s.component.framing-1) #subracts 1 from framing


   def add_r2(self,strand1,strand2,orientation): #orientation is a boolean which is true if the strands are oriented the same way, and false otherwise
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

   #def remove_r2 (self,crossing1, crossing2):
      #remove two crossings
      #remove joins

   #def r3(self,strand, crossing):
         
   def handle_annihilation(self,h1,h2):
      #checks to make sure each handle only has 2 strands (all joins must be removed)
      if (len(self.get_strands(h1))!=2 or len(self.get_strands(h2))!=2): #checks that each handle only has two strands
         print ("Handles can't be cancelled.")
      elif (len(list(set(self.strand_lookup(self.get_strands(h1)[0]))&set(self.strand_lookup(self.get_strands(h2)[0])))))!=2):
      #intersection of crossings containing both handles != 2 
         print ("Handles can't be cancelled.")
      #delete crossings
      self.crossings.remove(self.strand_lookup(self.get_strands(h1)[0])[0])
      self.crossings.remove(self.strand_lookup(self.get_strands(h1)[0])[0])
      #deletes components
      #self.components.remove(h1)
      #self.components.remove(h2)

   def handle_creation(self, f): #f=framing for 2-handle to have
      h1=component(1)
      h2=component(2,f)
      a=strand(h1)
      b=strand(h1,a,a)
      a.set_pred(b)
      a.set_succ(b)
      c=strand(h2)
      d=strand(h2,c,c)
      c=set_pred(d)
      c=set_succ(d)
      c1=crossing(a,c,b,d)
      c2=crossing(c,a,b,d)
      self.crossings.append(c1)
      self.crossings.append(c2)
