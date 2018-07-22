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
      for c in self.crossings:
         for i in range (4):
            if (c[i].component==comp and c[i] not in l):
               l.append(c[i])
      for j in self.joins:
         for k in range (2):
            if (j[k].component==comp and j[k] not in l):
               l.append(j[k])
##      for i in range (len(l)-1):
##         if (l[i+1] != l[i].succ):
##            for k in range (i, len(l)):
##               if (l[k]==l[i].succ):
##                  placeholder=l[i+1]
##                  l[i+1]=l[k]
##                  l[k]=placeholder
      return l

   def strand_name(self):
      return(max(map(lambda x:x.name,self.strands))+1)


   
   def add_join(self, x): #adds a join to a strand (splitting it into two different strands)
      y=strand(self.strand_name(), x.component, x, x.succ) #adds strand w pred x and succ x's succ
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
         self.joins.append(c)
      #return new strand?

##   def add_join(self, s0): #s0 is strand to be split, s0 will be the predecessor of the new s1
##      c0=s0.pred_con
##      c1=s0.succ_con
##      self.strands.append(s1)
##      s1=strand(None,s0.component,s0,s0.succ,None,s0.succ_con)
##      j=join(s0,s1)
##      s1.set_pred_con(j)
##      s1.succ.set_pred(s1)
##      s0.set_succ_con(j)
##      s0.set_succ(s1)
##      if(c1==c0):
##         print("stuff")
##      else:
##         for i in range(c1.len):
##            if(c1[i]==s0):
##               c1.strands[i]=s1
      
   def remove_join(self,j):
      s=strand(None,j[0],j[1],j[0].pred_con,j[1].succ_con)
      for i in ranges(s.pred_con.len):
         if(s.pred_con[i]==j[0]):
            s.pred_con.strands[i]=s
      for i in ranges(s.succ_con.len):
         if(s.succ_con[i]==j[1]):
            s.succ_con.strands[i]=s
      self.joins.remove(j)


##   def remove_join(self,j1):
##      self.joins.remove(j1)
##      x=j1[0]
##      y=j1[1]
##      j1[0].set_succ(j1[1].succ) #set's x's succ to be y's succ
##      j1[1].succ.set_pred(j1[0]) #set's y succ's pred to be x
##      #search crossings for y, replace w x
##      c=self.strand_lookup(y)[0]
##      if (c in self.crossings):
##         self.crossings.remove(c)
##         if (c[0]==y):
##            c.set_strands(x, c[1], c[2], c[3])
##         elif (c[1]==y):
##            c.set_strands(c[0], x, c[2], c[3])
##         elif (c[2]==y):
##            c.set_strands(c[0], c[1], x, c[3])
##         elif (c[3]==y):
##            c.set_strands(c[0], c[1], c[2], x)
##         self.crossings.append(c)
##      elif (c in self.joins):
##         self.joins.remove(c)
##         if (c[0]==y):
##            c.set_strands(x,c[1])
##         elif (c[1]==y):
##            c.set_strands(c[0], x)

   def remove_joins(self): #removes all joins except for joins in unknots
      for j in self.joins:
         if ([j[1],j[0]] not in self.joins): #checks if join is in unknot
            self.remove_join(j)

   def add_r1(self,x, sign): #strand=strand to twist, sign=clockwise or counterclockwise twist (1 will add 1 to framing, -1 will subtract 1 from framing)
      #add two joins to strand using add_join method
      self.add_join(x)
      z=x.succ
      self.add_join(x)
      y=x.succ
##      w=x.succ
##      y=strand(self.strand_name(), x.component, x)
##      z=strand(self.strand_name(), x.component, y, w)
##      w.set_pred(z)
##      x.set_succ(y)
##      s=list(set(self.strand_lookup(z))&set(self.strand_lookup(w)))[0]
##      if (s in self.crossings):
##         self.crossings.remove(s)
##         if (s[0]==x):
##            s.set_strands(z,s[1],s[2],s[3])
##         elif (s[1]==x):
##            s.set_strands(s[0],z,s[2],s[3])
##         elif (s[2]==x):
##            s.set_strands(s[0],s[1],z,s[3])
##         elif (s[3]==x):
##            s.set_strands(s[0],s[2],s[3],z)
##         self.crossings.append(s)
##      elif (s in self.joins):
##         self.joins.remove(s)
##         if (s[0]==x):
##            s.set_strands(z,s[1])
##         elif (s[1]==x):
##            s.set_strands(s[0],z)
##         self.joins.append(s)

      if (sign==1):
         c = crossing(y,x,z,y)
         x.component.change_framing(x.component.framing+1) #adds 1 to framing
      elif (sign==-1):
         c = crossing(x,z,y,y)
         x.component.change_framing(x.component.framing-1) #subtracts one from framing
      self.crossings.append(c) #adds crossing to crossing list


      for j in self.joins:
         if (j==join(x,y)):
            jn1=j
      for k in self.joins:
         if (k==join(y,z)):
            jn2=k 
      self.joins.remove(jn1)
      self.joins.remove(jn2)
      
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
   def add_r3(self, strandUnder, strandMiddle, strandOver):
      # need to add: if a goes up instead of down. maybe add input called orientation.


      # strandUnder is the strand that goes under strandMiddle and strandOver, which we are going to move
      # strandMiddle goes over strandUnder and under strandOver
      # strandOver goes over strandUnder and strandMiddle
      # strands refer to triangle




     # crossingsUnder = self.strand_list(strandUnder)  # the two crossing for strandUnder

      #this would be more efficient
      cross1 = self.pred__con(strandUnder)
      cross2 = self.succ__con(strandUnder)

      # add joins to where we are going to move strandUnder
      if (strandMiddle.pred not in cross1,cross2):
         self.add_join(strandMiddle.pred)

         #if strandUnder originally goes from strandOver to strandMiddle:
         c1 = crossing(strandUnder.pred, strandMiddle.pred, strandUnder, strandMiddle.pred.pred)
         
         #if strandUnder originally goes from strandMiddle to strandOver:
         c1 = crossing(strandUnder.pred, strandMiddle.pred.pred, strandUnder, strandMiddle.pred)

         if (strandOver.pred not in cross1,cross2):
            self.add_join(strandOver.pred)

            # if strandUnder originally goes from strandOver to strandMiddle:
            c2 = crossing(strandUnder, strandOver.pred, strandUnder.succ, strandOver.pred.pred)
            
            # if strandUnder originally goes from strandMiddle to strandOver:
            c2 = crossing(strandUnder.pred, strandOver.pred.pred, strandUnder, strandOver.pred)

         elif (strandOver.succ not in cross1,cross2):
            self.add_join(strandOver.succ)
            
            # if strandUnder originally goes from strandOver to strandMiddle:
            c2 = crossing(strandUnder, strandOver.succ, strandUnder.succ, strandOver.succ.succ)
            
            # if strandUnder originally goes from strandMiddle to strandOver:
            c2 = crossing(strandUnder.pred, strandOver.suc.suc, strandUnder, strandOver.succ)

            
      elif (strandMiddle.succ not in cross1,cross2):
         self.add_join(strandMiddle.succ)

         #if strandUnder originally goes from strandOver to strandMiddle:
         c1 = crossing(strandUnder.pred, strandMiddle.succ, strandUnder, strandMiddle.succ.succ) 
         
         #if strandUnder originally goes from strandMiddle to strandOver
         c1 = crossing(strandUnder,strandMiddle.succ.succ,strandUnder.succ,strandMiddle.succ)

         if (strandOver.pred not in cross1,cross2):
            self.add_join(strandOver.pred)

            # if strandUnder originally goes from strandOver to strandMiddle:
            c2 = crossing(strandUnder, strandOver.pred, strandUnder.succ, strandOver.pred.pred)
            # if strandUnder originally goes from strandMiddle to strandOver:
            c2 = crossing(strandUnder.pred, strandOver.pred.pred, strandUnder, strandOver.pred)

         elif (strandOver.succ not in cross1,cross2):
            self.add_join(strandOver.succ)

            # if strandUnder originally goes from strandOver to strandMiddle:
            c2 = crossing(strandUnder, strandOver.succ, strandUnder.succ, strandOver.succ.succ)
            # if strandUnder originally goes from strandMiddle to strandOver:
            c2 = crossing(strandUnder.pred, strandOver.succ, strandUnder, strandOver.succ.succ)

      self.crossings += [c1, c2]
      self.crossings.remove(crossingsUnder)  # remove old crossings
      self.remove_joins()  # remove extra joins

         
##   def handle_annihilation(self,h1,h2):
##      #checks to make sure each handle only has 2 strands (all joins must be removed)
##      if (len(self.strand_list(h1))!=2 or len(self.strand_list(h2))!=2): #checks that each handle only has two strands
##      elif (len(list(set(self.strand_lookup(self.strand_list(h1)[0]))&set(self.strand_lookup(self.strand_list(h2)[0]))))!=2):
##      #intersection of crossings containing both handles != 2 
##      #delete crossings
##      else:
##         self.crossings.remove(self.strand_lookup(self.strand_list(h1)[0])[0]) #deletes first crossing
##         self.crossings.remove(self.strand_lookup(self.strand_list(h1)[0])[0]) #deletes second crossing


   def handle_creation(self, f): #f=framing for 2-handle to have
   #THIS CODE WORKS!!!!!! :) :) :) :)
      h1=component(1)
      h2=component(2,f)
      a=strand(self.strand_name(), h1)
      b=strand(self.strand_name()+1, h1, a,a)
      a.set_pred(b)
      a.set_succ(b)
      c=strand(self.strand_name()+2, h2)
      d=strand(self.strand_name()+3,h2,c,c)
      c.set_pred(d)
      c.set_succ(d)
      c1=crossing(a,c,b,d)
      c2=crossing(c,a,b,d)
      self.crossings.append(c1)
      self.crossings.append(c2)
