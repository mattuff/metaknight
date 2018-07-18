from crossingClass import *
from joinClass import *
from strandClass import *
from componentClass import *

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
                  
   def __str__(self):
   #prints PD
      s="<Crossings: {"
      if(len(self.crossings)>=2):
         for i in range(len(self.crossings)-1):
            s+=str(self.crossings[i])+","
      if(len(self.crossings)>=1):
         s+=str(self.crossings[-1])
      s+="}; Joins: {"
      if(len(self.joins)>=2):
         for i in range(len(self.joins)-1):
            s+=str(self.joins[i])+","
      if(len(self.joins)>=1):
         s+=str(self.joins[-1])
      s+="}>"
      return(s)

   def strand_lookup(self,strand):
   #returns list of crossings/joins that a specific strand shows up in
      l=[]
      for c in self.crossings:
         if(strand in c):
            l.append(c)
      for j in self.joins:
         if(strand in j):
            l.append(j)
      return l
  
   def comp_list(self):
      l=[]
      for c in crossings:
         for i in range (4):
            if (c[i].component not in l):
               l.append(c[i].component)
      for j in joins:
         for k in range (2):
            if (k[j].component not in l):
               l.append(k[j].component)
      return l

   def strand_list(self, comp):
      l=[]
      for c in crossings:
         for i in range (4):
            if (c[i].component==comp and c[i] not in l):
               l.append(c[i])
      for j in joins:
         for k in range (2):
            if (j[k].component==comp and j[k] not in l):
               l.append(j[k])
      for i in range (len(l)):
         if (l[i+1] != l[i].succ):
            for k in range (i, len(l)):
               if (l[k]==l[i].succ):
                  placeholder=l[i+1]
                  l[i+1]=l[k]
                  l[k]=placeholder
      return l

   def strand_name(self):
      l=[]
      for c in self.crossings:
         for i in range (4):
            if (c[i].name not in l):
               l.append(c[i].name)
      for j in self.joins:
         for k in range (2):
            if (j[k].name not in l):
               l.append(j[k].name)
      l.sort()
      k=l[-1]+1
      return k
   
   def add_join(self, x): #adds a join to a strand (splitting it into two different strands)
      y=strand(x.component, self.strand_name(), x, x.succ) #adds strand w pred x and succ x's succ
      x.succ.set_pred(y) #sets x's old successor's pred to be y
      x.set_succ(y) #sets x's successor to y
      jx=join(x,y) #creates join of [x,y]
      self.joins.append(jx) #adds new join to join list
      #search for crossings containing both x and y.get_succ(), replaces x w/ y
      c=list(set(self.strand_lookup(x))&set(self.strand_lookup(y.succ)))[0] #finds crossing containing x and y.get_succ()
      if (c in self.crossings):
         self.crossings.remove(c) 
         if (c[0]==x): #if x is the ith strand in the crossing
            c.set_strands(y, c[1], c[2], c[3]) #then replace strand w strand.get_succ().get_succ()
         elif (c[1]==x):
            c.set_strands(c[0], y, c[2], c[3])
         elif (c[2]==x):
            c.set_strands(c[0], c[1], y, c[3])
         elif (c[3]==x):
            c.set_strands(c[0], c[1], c[2], y)
         self.crossings.append(c)
      elif (c in self.joins):
         self.joins.remove(c)
         if (c[0]==x):
            c.set_strands(y,c[1])
         elif (c[1]==x):
            c.set_strands(c[0], y)
      #return new strand?

   def remove_join(self,j1):
      self.joins.remove(j1)
      x=j1[0]
      y=j1[1]
      j1[0].set_succ(j1[1].succ) #set's x's succ to be y's succ
      j1[1].succ.set_pred(j1[0]) #set's y succ's pred to be x
      #search crossings for y, replace w x
      c=self.strand_lookup(y)[0]
      if (c in self.crossings):
         self.crossings.remove(c)
         if (c[0]==y):
            c.set_strands(x, c[1], c[2], c[3])
         elif (c[1]==y):
            c.set_strands(c[0], x, c[2], c[3])
         elif (c[2]==y):
            c.set_strands(c[0], c[1], x, c[3])
         elif (c[3]==y):
            c.set_strands(c[0], c[1], c[2], x)
         self.crossings.append(c)
      elif (c in self.joins):
         self.joins.remove(c)
         if (c[0]==y):
            c.set_strands(x,c[1])
         elif (c[1]==y):
            c.set_strands(c[0], x)

   def remove_joins(self): #removes all joins except for joins in unknots
      for j in self.joins:
         if ([j[1],j[0]] not in self.joins): #checks if join is in unknot
            remove_join(j)

   def add_r1(self,strand, sign): #strand=strand to twist, sign=clockwise or counterclockwise twist (1 will add 1 to framing, -1 will subtract 1 from framing)
      #add two joins to strand using add_join method
      self.add_join(strand) #strand.succ.succ (strand1)
      self.add_join(strand) #strand.succ (strand2)
      if (sign==1):
         self.crossings.append([strand.succ, strand, strand.succ.succ, strand.succ]) #adds crossing
         strand.component.change_framing(strand.component.framing+1) #adds 1 to framing
      elif (sign==-1):
         self.crossings.append([strand, strand.succ.succ, strand.succ, strand.succ]) #adds crossing
         strand.component.change_framing(strand.component.framing-1) #subtracts one from framing
      #remove joins added from join list but not using the remove join function
      self.joins.remove([strand, strand.succ])
      self.joins.remove([strand.succ, strand.succ.succ])

##   def remove_r1(self, s): #s: crossed strand for r1 #make names longer?
##      c=self.strand_lookup(s)[0]
##      if (c[2]==c[3] or (c[0]==c[1])):
##         self.crossings.remove(c) #remove crossing
##         self.joins.append([s.pred, s]) #adds join
##         self.joins.append([s, s.succ]) #adds join
##         remove_join([s.pred, s]) #removes join; does relabling
##         remove_join([s, s.succ]) #removes join; does relabling
##         s.component.change_framing(s.component.framing+1) #add 1 to framing
##      elif (c[0]==c[3] or c[1]==c[2]):
##         self.crossings.remove(c) #remove crossing
##         self.joins.append([s.pred, s]) #adds join
##         self.joins.append([s, s.succ]) #adds join
##         remove_join([s.pred, s]) #removes join; does relabling
##         remove_join([s, s.succ]) #removes join; does relabling
##         s.component.change_framing(s.component.framing-1) #subracts 1 from framing

   def add_r2(self,s1,s2,orientation): #orientation is a boolean which is true if the strands are oriented the same way, and false otherwise
      #change strand1 --> s1?
      #find all places you can do r2?
      #add two joins to each strand
      #add two crossings
      #remove joins
      self.add_join(s1)
      self.add_join(s1)
      self.add_join(s2)
      self.add_join(s2)
      l=(self.strand_lookup(s1.succ))+(self.strand_lookup(s2.succ))
      if(orientation):
         c1=crossing(s1,s2.succ,s1.succ,s2)
         c2=crossing(s1.succ,s2.succ,s1.succ.succ,s2.succ.succ)
      else:
         c1=crossing(s1,s2.succ.succ,s1.succ,s2.succ)
         c2=crossing(s1.succ,s2,s1.succ.succ,s2.succ)
      self.crossings+=[c1,c2]
      for s in l:
         self.joins.remove(s)

   def remove_r2 (self,s1, s2): #strands s1 and s2
      l=self.strand_lookup(s1)
      if(s1.succ==s2.pred):
         self.add_join(s1.succ)
      if(s2.succ==s1.pred):
         self.add_join(s2.succ)
      s1.set_succ(s1.succ.succ)
      s1.succ.set_pred(s1)
      s1.set_pred(s1.pred.pred)
      s1.pred.set_succ(s1)
      s2.set_succ(s2.succ.succ)
      s2.succ.set_pred(s2)
      s2.set_pred(s2.pred.pred)
      s2.pred.set_succ(s2)
      for c in l:
         if(c in self.crossings):
            self.crossings.remove(c)

    #Pseudo code

   def add_r3(self, strand1, strand2, strand3): #the input should be the 'heads' of the three crossings
      c1 = self.returnCrossing(strand1,strand1.succ) #define returnCrossing which will give the crossing between a strand and its succ
      c2 = self.returnCrossing(strand1.succ, strand1.succ.succ)
      c3 = self.returnCrossing(strand2, strand2.succ)
      if(c3 == c1 or c3 == c2):
         c3 = returnCrosssing(strand2.succ, strand2.succ.succ)

        #identify badStrand that will be moved over.
      if((c2[0] == c1[0].succ) or (c3[0] == c1[0].succ)): badStrand = c1[0] #change to be pred also
      elif((c1[0] == c2[0].succ) or (c3[0] == c2[0].succ)): badStrand = c2[0]  #change to be pred too
      elif((c1[0] == c3[0].succ) or (c2[0] == c3[0].succ)): badStrand = c3[0] #change to be pred as well

        #identify strand to add joins to - the strand that is not in a crossing with badStrand
      if(badStrand, badStrand.succ, badStrand.succ.succ not in c1): #add join here
         self.add_join(strand1)
         goodStrand1 = strand1
         if(strand2.succ in c1):
            if(strand2) in c1:
               self.add_join(strand2)
               goodStrand2 = strand2
            else:
               self.add_join(strand2.succ.succ)
               goodStrand2 = strand2.succ.succ
         elif(strand3 in c1):
            self.add_join(strand3)
            goodStrand2 = strand3
         elif(strand3.succ.succ in c1):
            self.add_join(strand3.succ.succ)
            goodStrand2 = strand3.succ.succ

      elif(badStrand, badStrand.succ, badStrand.succ.succ not in c2):#add join here
         self.add_join(strand1.succ.succ)
         goodStrand1 = strand1.succ.succ
         if (strand2.succ in c1):
            if (strand2) in c1:
               self.add_join(strand2)
               goodStrand2 = strand2
            else:
               self.add_join(strand2.succ.succ)
               goodStrand2 = strand2.succ.succ
         elif (strand3 in c1):
            self.add_join(strand3)
            goodStrand2 = strand3
         elif (strand3.succ.succ in c1):
            self.add_join(strand3.succ.succ)
            goodStrand2 = strand3.succ.succ


      elif(badStrand, badStrand.succ, badStrand.succ.succ not in c3):#add join here
         if(strand2 in c3):
            self.add_join(strand2)
            goodStrand1 = strand2
         elif(strand2.succ.succ in c3):
            self.add_join(strand2.succ.succ)
            goodStrand1 = strand2.succ.succ

         if(strand3 in c3):
            self.add_join(strand3)
            goodStrand2 = strand3
         elif(strand3.succ.succ in c3):
            self.add_join(strand3.succ.succ)
            goodStrand2 = strand3.succ.succ

      c4 = crossing(badStrand, goodStrand1, badStrand.succ, goodStrand1.succ) #change for different orientations
      c5 = crossing(badStrand.succ, goodStrand2, badStrand.succ.succ, goodStrand2.succ) #change for diff orientations

      self.remove_joins() #not sure if this method exists yet (it does!)




         
   def handle_annihilation(self,h1,h2):
      #checks to make sure each handle only has 2 strands (all joins must be removed)
      if (len(self.get_strands(h1))!=2 or len(self.get_strands(h2))!=2): #checks that each handle only has two strands
         print ("Handles can't be cancelled.")
      elif (len(list(set(self.strand_lookup(self.get_strands(h1)[0]))&set(self.strand_lookup(self.get_strands(h2)[0]))))!=2):
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
      a=strand(h1, self.strand_name())
      b=strand(h1,self.strand_name(),a,a)
      a.set_pred(b)
      a.set_succ(b)
      c=strand(h2,self.strand_name())
      d=strand(h2,self.strand_name(),c,c)
      c=set_pred(d)
      c=set_succ(d)
      c1=crossing(a,c,b,d)
      c2=crossing(c,a,b,d)
      self.crossings.append(c1)
      self.crossings.append(c2)
