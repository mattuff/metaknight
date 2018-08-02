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
      self.strands=strands

   def __str__(self):
      l=[]
      c=[]
      for x in self.strands:
         if(x.component not in c):
            l.append(x)
            c.append(x.component)
      s="Components:\n"
      n=0
      for x in l:
         n+=1
         s+=" - ["+str(n)
         x.name=n
         y=x.succ
         while(y!=x):
            n+=1
            s+=","+str(n)
            y.name=n
            y=y.succ
         s+="] ("
         if(x.component.handle==2):
            s+="2-handle;f="+str(x.component.framing)+")\n"
         else:
            s+=str(x.component.handle)+"-handle)\n"
      s+="Crossings:\n"
      if(len(self.crossings)==0):
         s+="None"
      if(len(self.crossings)>=2):
         for i in range(len(self.crossings)-1):
            s+=str(self.crossings[i])+","
      if(len(self.crossings)>=1):
         s+=str(self.crossings[-1])
      s+="\nJoins:\n"
      if(len(self.joins)==0):
         s+="None"
      if(len(self.joins)>=2):
         for i in range(len(self.joins)-1):
            s+=str(self.joins[i])+","
      if(len(self.joins)>=1):
         s+=str(self.joins[-1])
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

   def strand_list(self, s): #returns an ordered list of strands given a component
      l=[s]
      t=s.succ
      while(t!=s):
         l.append(t)
         t=t.succ
      return l

   def switch(self,c): #switches overcrossing strand
      if(c[1]==c[3].pred):
         f=lambda x:c.strands[(x+1)%4]
      else:
         f=lambda x:c.strands[(x-1)%4]
      c.strands = list(map(f,range(4)))

   def rename(self,s,n): #s is named n, strand's name is predecessor's +1
      s.name=n
      t=s.succ
      while(t!=s):
         n+=1
         t.name=n
         t=t.succ
      return(n)

   def rename_all(self):
      l=[]
      n=1
      for s in self.strands:
         if(s.component not in l):
            n=self.rename(s,n)+1
            l.append(s.component)

   def comp_crossings(self,h1): #given a component, returns crossings fully contained within component
      l=[]
      for c in self.crossings:
         if (c[0].component==c[1].component==h1):
            l.append(c)
      return l

   def comp_joins(self,h1): #given a component, returns joins fully contained within component
      l=[]
      for j in self.joins:
         if (j[0].component==h1):
            l.append(j)
      return l
            
   def comp_intersections(self,h1): #given a component, returns crossings between that component and another
      l=[]
      for c in self.crossings:
         if (c[0].component==h1 and c[1].component!=h1):
            l.append(c)
         elif (c[1].component==h1 and c[0].component!=h1):
            l.append(c)
      return l

   def connect_sum(self,s0,s1):
      s=[s0,s1]
      j=[]
      for i in range(2):
         self.add_join(s[i])
      for i in range(2):
         j=join(s[i],s[not i].succ)
         self.joins.remove(s[i].succ_con)
         self.joins.append(j)
         s[i].succ_con=j
         s[not i].succ.pred_con=j
      for i in range(2):
         s[i].succ=s[not i].succ
         s[i].succ.pred=s[i]

   def add_join(self, s0): #s0 is strand to be split, s0 will be the predecessor of the new s1
      c0=s0.pred_con
      c1=s0.succ_con
      s1=strand(s0.component,s0,s0.succ,None,s0.succ_con)
      self.strands.append(s1)
      s0.set_succ(s1)
      s1.succ.set_pred(s1)
      j=join(s0,s1)
      s0.set_succ_con(j)
      s1.set_pred_con(j)
      if(c1==c0):
         if(c0.len-2): #if c0 is a crossing rather than a join
            if((c0[2]==s0) & (c0[3]==s0)): #this is the only case in which the first instance of s0 should not be replaced with s1
               c0.strands[3]=s1
            else:
               c0.strands[c0.strands.index(s0)]=s1 #index method returns index of first instance of s0 in list
         else:
            c0.strands[0]=s1
      else:
         for i in range(c1.len):
            if(c1[i]==s0):
               c1.strands[i]=s1
      self.joins.append(j)

   def remove_join(self,j):
      s=strand(j[0].component,j[0].pred,j[1].succ,j[0].pred_con,j[1].succ_con)
      for i in range(s.pred_con.len):
         if(s.pred_con[i]==j[0]):
            s.pred_con.strands[i]=s
      for i in range(s.succ_con.len):
         if(s.succ_con[i]==j[1]):
            s.succ_con.strands[i]=s
      s.pred.succ=s
      s.succ.pred=s
      self.strands.append(s)
      self.strands.remove(j[0])
      self.strands.remove(j[1])
      self.joins.remove(j)

   def remove_joins(self): #removes all joins except for joins in unknots
      j=self.joins.copy()
      for x in j:
         if(x[0]!=x[1]):
            self.remove_join(x)

#   def add_r1(self, x, sign,counterclockwise):
#   # strand=strand to twist, sign=clockwise or counterclockwise twist (True will add 1 to framing, False will subtract 1 from framing)
#
#      f = x.component.framing
#      w = x.succ
#      y = strand(x.component, x)
#      z = strand(x.component, y, w)
#      z.set_succ_con = x.succ_con
#      y.set_succ(z)
#      w.set_pred(z)
#      x.set_succ(y)
#      s = x.succ_con
#      s.strands[s.strands.index(x)] = z
#
#      # adds crossing
#      if (sign):
#         if counterclockwise:
#            c = crossing(x, y, y, z)
#         else:
#            c = crossing(y, x, z, y)
#         x.component.change_framing(f + 1)  # adds 1 to framing
#      else:
#         if counterclockwise:
#            c = crossing(y, y, z, x)
#         else:
#            c = crossing(x, z, y, y)
#         x.component.change_framing(f - 1)  # subtracts one from framing
#      self.crossings.append(c)  # adds crossing to crossing list
#
#      # changes succ and pred crossings of strands involved
#      z.succ_con = s
#      x.set_succ_con(c)
#      y.set_pred_con(c)
#      y.set_succ_con(c)
#      z.set_pred_con(c)

   def add_r1(self, x, o, i):  # strand=strand to twist, sign=clockwise or counterclockwise twist (1 will add 1 to framing, 0 will subtract 1 from framing)
      x.component.framing+=(-1)**(o!=i) #changes framing
      self.add_join(x)
      self.add_join(x)
      for j in [x.succ_con,x.succ.succ_con]:
         self.joins.remove(j)
      s=[x,x.succ,x.succ.succ]
      if(o): # computes crossing
         if(i):
            c=crossing(s[1],s[0],s[2],s[1])
         else:
            c=crossing(s[1],s[1],s[0],s[2])
      else:
         if(i):
            c=crossing(s[1],s[1],s[2],s[0])
         else:
            c=crossing(s[0],s[1],s[1],s[2])
      self.crossings.append(c)  # adds crossing to crossing list
      for i in range(2): # changes succ and pred crossings of strands involved
         s[i].succ_con=c
         s[i+1].pred_con=c
      

   def remove_r1(self, x):  #x is the looped strand

      j1 = join(x.pred, x)
      j2 = join(x, x.succ)

      self.crossings.remove(x.succ_con)

      x.pred.set_succ_con(j1)
      x.set_succ_con(j2)
      x.set_pred_con(j1)
      x.succ.set_pred_con(j2)
      
      self.joins.append(j1)
      self.joins.append(j2)
      

   def add_r2(self,s1,s2,o): #orientation is a boolean which is true if the strands are oriented the same way, and false otherwise
      #s1 gets pulled under s2
      #find all places you can do r2?
      #add two joins to each strand
      #add two crossings
      #remove joins
      self.add_join(s1)
      self.add_join(s1)
      self.add_join(s2)
      self.add_join(s2)
      l=[s1.succ_con,s1.succ.succ_con,s2.succ_con,s2.succ.succ_con]

      if(o):
         c1=crossing(s1,s2.succ,s1.succ,s2)
         c2=crossing(s1.succ,s2.succ,s1.succ.succ,s2.succ.succ)
      else:
         c1=crossing(s1,s2.succ,s1.succ,s2.succ.succ)
         c2=crossing(s1.succ,s2.succ,s1.succ.succ,s2)
      c = lambda x : c1 if x else c2
      s = lambda x : s1 if x else s2
      for b in [True,False]:
         s(b).succ_con=c(o or b)
         s(b).succ.pred_con=c(o or b)
         s(b).succ.succ_con=c(not o and not b)
         s(b).succ.succ.pred_con=c(not o and not b)
      self.crossings+=[c1,c2]
      for s in l:
         self.joins.remove(s)

   def remove_r2(self,s0,s1):
      s=[s0,s1]
      c=[s0.pred_con,s0.succ_con]
      j=[join(s0.pred,s0),join(s1.pred,s1),join(s0,s0.succ),join(s1,s1.succ)]
      for i in range(2):
         s[i].pred_con=j[i]
         s[i].pred.succ_con=j[i]
         s[i].succ_con=j[i+2]
         s[i].succ.pred_con=j[i+2]
      self.joins+=j
      for x in c:
         self.crossings.remove(x)

   def add_r3(self, strandUnder, strandMiddle, strandOver):
      # strandUnder is the strand that goes under strandMiddle and strandOver, which we are going to move
      # strandMiddle goes over strandUnder and under strandOver
      # strandOver goes over strandUnder and strandMiddle
      # strands refer to triangle

      c1 = strandUnder.pred_con
      #print('cross1: ' + str(cross1))
      c2 = strandUnder.succ_con
      #print('cross2: ' + str(cross2))
      if(strandMiddle.pred_con != c1 and strandMiddle.pred_con != c2): c3 = strandMiddle.pred_con
      else: c3 = strandMiddle.succ_con


      #orientation of strandMiddle
      if (strandMiddle.pred not in c1 and strandMiddle.pred not in c2):
         self.add_join(strandMiddle.pred)

         #orientation of strandOver
         if (strandOver.pred not in c1 and strandOver.pred not in c2):
            self.add_join(strandOver.pred)

            #orientation of strandUnder
            if(strandOver in c1):
               c1.set_strands(strandUnder.pred, strandMiddle.pred, strandUnder, strandMiddle.pred.pred)
               c2.set_strands(strandUnder, strandOver.pred, strandUnder.succ, strandOver.pred.pred)

            elif(strandOver in c2):
               c1.set_strands(strandUnder.pred, strandOver.pred.pred, strandUnder, strandOver.pred)
               c2.set_strands(strandUnder, strandMiddle.pred.pred, strandUnder.succ, strandMiddle.pred)

         #orientation of strandOver
         elif (strandOver.succ not in cross1 and strandOver.succ not in c2):
            self.add_join(strandOver.succ)

            #orientation of strandUnder
            if(strandOver in c1):
               c1.set_strands(strandUnder.pred, strandMiddle.succ, strandUnder, strandUnder.pred)
               c2.set_strands(strandUnder, strandOver.pred, strandUnder.succ, strandUnder.succ)

            elif(strandOver in c2):
               c1.set_strands(strandUnder.pred, strandOver.succ.succ, strandUnder, strandOver.succ)
               c2.set_strands(strandUnder, strandMiddle.pred.pred, strandUnder.succ, strandMiddle.pred)

      #orientation of strandMiddle
      elif (strandMiddle.succ not in c1 and strandMiddle.succ not in c2):
         self.add_join(strandMiddle.succ)

         #orientation of strandOver
         if (strandOver.pred not in c1 and strandOver.pred not in c2):
            print('strandOver.pred not in cross1 and strandOver.pred not in cross2, adding join')
            self.add_join(strandOver.pred)

            #orientation of strandUnder
            if(strandOver in c1):
               c1.set_strands(strandUnder.pred, strandMiddle.succ, strandUnder, strandMiddle.succ.succ)
               c2.set_strands(strandUnder, strandOver.pred, strandUnder.succ, strandOver.pred.pred)

            elif(strandOver in c2):
               c1.set_strands(strandUnder.pred, strandOver.pred.pred, strandUnder, strandOver.pred)
               c2.set_strands(strandUnder, strandMiddle.succ.succ, strandUnder.succ, strandMiddle.succ)

         #orientation of strandOver
         elif (strandOver.succ not in c1, c2):
            self.add_join(strandOver.succ)

            #orientation of strandUnder
            if(strandOver in c1):
               c1.set_strands(strandUnder.pred, strandMiddle.succ, strandUnder, strandMiddle.succ.succ)
               c2.set_strands(strandUnder, strandOver.succ, strandUnder.succ, strandOver.succ.succ)

            elif(strandOver in c2):
               c1.set_strands(strandUnder.pred, strandOver.succ.succ, strandUnder, strandOver.succ)
               c2.set_strands(strandUnder, strandMiddle.succ.succ, strandUnder.succ, strandMiddle.succ)
         

   def handle_annihilation(self,h1,h2):
      #checks to make sure each handle only has 2 strands (all joins must be removed)
      if (len(self.strand_list(h1))==2 and len(self.strand_list(h2))==2): #checks that each handle only has two strands   
         if (len(list(set(self.strand_lookup(self.strand_list(h1)[0]))&set(self.strand_lookup(self.strand_list(h2)[0]))))==2):
             self.crossings.remove(self.strand_lookup(self.strand_list(h1)[0])[0]) #deletes first crossing
             self.crossings.remove(self.strand_lookup(self.strand_list(h1)[0])[0]) #deletes second crossing 
            
   def handle_creation(self, f): #f=framing for 2-handle to have
   #THIS CODE WORKS!!!!!! :) :) :) :)
      h1=component(1)
      h2=component(2,f)
      a=strand(h1)
      b=strand(h1, a,a)
      a.set_pred(b)
      a.set_succ(b)
      c=strand(h2)
      d=strand(h2,c,c)
      c.set_pred(d)
      c.set_succ(d)
      c1=crossing(a,c,b,d)
      c2=crossing(c,a,b,d)
      self.crossings+=[c1,c2]
      self.strands+=[a,b,c,d]
      

   def handle_slide(self, h1, h2, sign): #h2 is being slid over h1; sign=True if same orientation
      #makes parallel copies of all strands in h1
      s=self.strand_list(h1) #list of strands in h1, in succ order
      l=[]
      comp_crossings=self.comp_crossings(h1.component) #crossings with only strands in h1
      comp_intersections=self.comp_intersections(h1.component) #crossings w 2 strands in h1, and 2 in another strand

      #can considate, use ternary operator?
      for k in range (len(s)): #sets up parallel copy of h1
         st=strand(h2.component)
         l+=[st]
      for i in range (len(l)-1): #sets up preds and succs
         if (sign):
            l[i].set_pred(l[i-1])
            if (i < (len(l)-1)):
               l[i].set_succ(l[i+1])
            else:
               l[i].set_succ(l[0])
         else:
            l[i].set_succ(l[i-1])
            if (i < (len(l)-1)):
               l[i].set_pred(l[i+1])
            else:
               l[i].set_pred(l[0])

      self.strands+=l

      for j in self.comp_joins(h1.component): #duplicates joins
         a=s.index(j[0])
         if (sign):
            jn=join(l[a],l[a+1])
         else:
            jn=join(l[a+1],l[a])
         self.joins.append(jn)

      for cx in comp_crossings: #takes crossing, makes into four
         a=cx[0]
         b=cx[1]
         c=cx[2]
         d=cx[3]
         aa=l[s.index(a)]
         bb=l[s.index(b)]
         cc=l[s.index(c)]
         dd=l[s.index(d)]
         var=(b.succ==d)

         e=strand(h1.component, a,c)
         a.set_succ(e)
         c.set_pred(e)
         s.insert(s.index(a)+1, e)
         if (sign):
            ee=strand(h2.component, aa, cc)
            aa.set_succ(ee)
            cc.set_pred(ee)
         else:
            ee=strand(h2.component, cc, aa)
            cc.set_succ(ee)
            aa.set_pred(ee)
         l.insert(l.index(aa)+1, ee)
         
         if (var):
            f=strand(h1.component, b, d)
            s.insert(s.index(b)+1, f)
            b.set_succ(f)
            d.set_pred(f)
            if (sign):
               ff=strand(h2.component, bb, dd)
               bb.set_succ(ff)
               dd.set_pred(ff)
            else:
               ff=strand(h2.component, dd, bb)
               dd.set_succ(ff)
               bb.set_pred(ff)
            l.insert(l.index(bb)+1, ff)
         else:
            f=strand(h1.component, d, b)
            d.set_succ(f)
            b.set_pred(f)
            s.insert(s.index(d)+1, f)
            if (sign):
               ff=strand(h2.component, dd, bb)
               dd.set_succ(ff)
               bb.set_pred(ff)
            else:
               ff=strand(h2.component, bb, dd)
               bb.set_succ(ff)
               dd.set_pred(ff)
            l.insert(s.index(d)+1, ff)
         self.strands+=[e,ee,f,ff]
         self.crossings.remove(cx)

         if (var):
            c1=crossing(a,f,e,d)
            c4=crossing(e,ff,c,dd)
            if (sign):
               c2=crossing(aa,b,ee,f)
               c3=crossing(ee,bb,cc,ff)
            else:
               c2=crossing(ee,f,aa,b)
               c3=crossing(cc,ff,ee,bb)
         else:
            c1=crossing(a,ff,e,dd)
            c4=crossing(e,f,c,d)
            if (sign):
               c2=crossing(aa,bb,ee,ff)
               c3=crossing(ee,b,cc,f)
            else:
               c2=crossing(ee,ff,aa,bb)
               c3=crossing(cc,f,ee,b)
         
         self.crossings+=[c1,c2,c3,c4]

         a.set_succ_con(c1)
         e.set_pred_con(c1)
         e.set_succ_con(c4)
         c.set_pred_con(c4)

         if (sign):
            aa.set_succ_con(c2)
            ee.set_pred_con(c2)
            ee.set_succ_con(c3)
            cc.set_pred_con(c3)

            if (var):
               b.set_succ_con(c2)
               f.set_pred_con(c2)
               f.set_succ_con(c1)
               d.set_pred_con(c1)

               bb.set_succ_con(c3)
               ff.set_pred_con(c3)
               ff.set_succ_con(c4)
               dd.set_pred_con(c4)
      
            else:
               d.set_succ_con(c4)
               f.set_pred_con(c4)
               f.set_succ_con(c3)
               b.set_pred_con(c3)

               dd.set_succ_con(c1)
               ff.set_pred_con(c1)
               ff.set_succ_con(c2)
               bb.set_pred_con(c2)
            
         else:
            cc.set_succ_con(c3)
            ee.set_pred_con(c3)
            ee.set_succ_con(c2)
            aa.set_pred_con(c2)

            if (var):
               b.set_succ_con(c2)
               f.set_pred_con(c2)
               f.set_succ_con(c1)
               d.set_pred_con(c1)

               dd.set_succ_con(c4)
               ff.set_pred_con(c4)
               ff.set_succ_con(c3)
               bb.set_pred_con(c3)

            else:
               d.set_succ_con(c4)
               f.set_pred_con(c4)
               f.set_succ_con(c3)
               b.set_pred_con(c3)

               bb.set_succ_con(c2)
               ff.set_pred_con(c2)
               ff.set_succ_con(c1)
               dd.set_pred_con(c1)               

      for cx in comp_intersections: #turns crossings between h1 and another comp into 2 crossings
         if (cx[0].component==h1.component):
            a=cx[0]
            b=cx[1]
            c=cx[2]
            d=cx[3]
            aa=l[s.index(a)]
            cc=l[s.index(c)]
            f=strand(b.component)
            if (b.succ==d):
               f.set_pred(b)
               f.set_succ(d)
               if (sign):
                  c2=crossing(aa,b,cc,f)
                  aa.set_succ_con(c2)
                  cc.set_pred_con(c2)    
               else:
                  c2=crossing(cc,f,aa,b)
                  aa.set_pred_con(c2)
                  cc.set_succ_con(c2)  
               c1=crossing(a,f,c,d)   
               a.set_succ_con(c1)
               c.set_pred_con(c1)   
               b.set_succ_con(c2)
               f.set_pred_con(c2)
               f.set_succ_con(c1)
               d.set_pred_con(c1)
               
            else:
               f.set_succ(b)
               f.set_pred(d)
               if (sign):
                  c2=crossing(aa,b,cc,f)
                  aa.set_succ_con(c2)
                  cc.set_pred_con(c2) 
               else:
                  c2=crossing(cc,f,aa,b)
                  aa.set_pred_con(c2)
                  cc.set_succ_con(c2)
               c1=crossing(a,f,c,d)   
               a.set_succ_con(c1)
               c.set_pred_con(c1)   
               b.set_pred_con(c2)
               f.set_succ_con(c2)
               f.set_pred_con(c1)
               d.set_succ_con(c1)

            self.strands+=[f]
               
         else:
            a=cx[0]
            b=cx[1]
            c=cx[2]
            d=cx[3]
            bb=l[s.index(b)]
            dd=l[s.index(d)]
            e=strand(a.component,a,c)
            if (b.succ==d):
               c1=crossing(a,b,e,d)
               c2=crossing(e,bb,c,dd)
               a.set_succ_con(c1)
               e.set_pred_con(c1)
               e.set_succ_con(c2)
               c.set_pred_con(c2)
               b.set_succ_con(c1)
               d.set_pred_con(c1)
               if (sign):
                  bb.set_succ_con(c2)
                  dd.set_pred_con(c2)
               else:
                  bb.set_pred_con(c2)
                  dd.set_succ_con(c2)
            else:
               c1=crossing(a,bb,e,dd)
               c2=crossing(e,b,c,d)
               a.set_succ_con(c1)
               e.set_pred_con(c1)
               e.set_succ_con(c2)
               c.set_succ_con(c2)
               b.set_pred_con(c2)
               d.set_succ_con(c2)
               if (sign):
                  bb.set_pred_con(c1)
                  dd.set_succ_con(c1)
               else:
                  bb.set_succ_con(c2)
                  dd.set_pred_con(c2)

            self.strands+=[e]
               
         self.crossings+=[c1,c2]


      #adding extra twists for framing
      if (sign):
         if (h1.component.framing>0): #counterclockwise twists
            for i in range(h1.component.framing):
               l1=l[-1]
               s1=s[-1]
               self.add_join(l1)
               self.add_join(l1)
               l2=l1.succ
               l3=l1.succ.succ
               self.add_join(s1)
               self.add_join(s1)
               s2=s1.succ
               s3=s1.succ
               joinlist=[l1.succ_con, l2.succ_con, s1.succ_con, s2.succ_con]
               l+=[l2,l3]
               s+=[s2,s3]
               c1=crossing(s1,l1,s2,l2)
               c2=crossing(s2,l3,s3,l2)
               self.crossings+=[c1,c2]
               for j in joinlist:
                  self.joins.remove(j)
               l1.set_succ_con(c1)
               l2.set_pred_con(c1)
               l2.set_succ_con(c2)
               l3.set_pred_con(c2)
               s1.set_succ_con(c1)
               s2.set_pred_con(c1)
               s2.set_succ_con(c2)
               s3.set_pred_con(c2)
               
         else: #clockwise twists
            for i in range(-h1.component.framing):
               l1=l[-1]
               s1=s[-1]
               selef.add_join(l1)
               self.add_join(l1)
               l2=l1.succ
               l3=l1.succ.succ
               self.add_join(s1)
               self.add_join(s1)
               s2=s1.succ
               s3.s1.succ
               joinlist=[l1.succ_con, l2.succ_con, s1.succ_con, s2.succ_con]
               l+=[l2,l3]
               s+=[s2,s3]
               c1=crossing(l1,s2,l2,s1)
               c2=crossing(s2,l3,s3,l2)
               self.crossings+=[c1,c2]
               for j in joinlist:
                  self.joins.remove(j)
               l1.set_succ_con(c1)
               l2.set_pred_con(c1)
               l2.set_succ_con(c2)
               l3.set_pred_con(c2)
               s1.set_succ_con(c1)
               s2.set_pred_con(c1)
               s2.set_succ_con(c2)
               s3.set_pred_con(c2)

      else:
         if (h1.component.framing>0): #counterclockwise twists
            for i in range(h1.component.framing):
               l1=l[-1]
               s1=s[-1]
               self.add_join(l1)
               self.add_join(l1)
               l2=l1.succ
               l3=l2.succ
               self.add_join(s1)
               self.add_join(s1)
               s2=s1.succ
               s3=s2.succ
               joinlist=[l1.succ_con, l2.succ_con, s1.succ_con, s2.succ_con]
               s+=[s2,s3]
               l.remove(l1)
               l+=[l3,l2,l1]
               c1=crossing(s1,l3,s2,l2)
               c2=crossing(s2,l1,s3,l2)
               self.crossings+=[c1,c2]
               for j in joinlist:
                  self.joins.remove(j)
               l1.set_succ_con(c2)
               l2.set_pred_con(c2)
               l2.set_succ_con(c1)
               l3.set_pred_con(c1)
               s1.set_succ_con(c1)
               s2.set_pred_con(c1)
               s2.set_succ_con(c2)
               s3.set_succ_con(c2)

         else: #clockwise twists
            for i in range(-h1.component.framing):
               l1=l[-1]
               s1=s[-1]
               self.add_join(l1)
               self.add_join(l1)
               l2=l1.succ
               l3=l2.succ
               self.add_join(s1)
               self.add_join(s1)
               s2=s1.succ
               s3=s2.succ
               joinlist=[l1.succ_con, l2.succ_con, s1.succ_con, s2.succ_con]
               s+=[s2,s3]
               l.remove(l1)
               l+=[l3,l2,l1]
               c1=crossing(l2,s1,l3,s2)
               c2=crossing(s2,l1,s3,l2)
               self.crossings+=[c1,c2]
               for j in joinlist:
                  self.joins.remove(j)
               l1.set_succ_con(c2)
               l2.set_pred_con(c2)
               l2.set_succ_con(c1)
               l3.set_pred_con(c1)
               s1.set_succ_con(c1)
               s2.set_pred_con(c1)
               s2.set_succ_con(c2)
               s3.set_succ_con(c2)
               
      self.connect_sum(h2,l[0])
      self.remove_joins()

      

## change in blackboard framing?????????????????????????????????
##      if (sign):
##         h2.component.framing+=h1.component.framing
##      else:
##         h2.component.framing+=(-h1.component.framing)

      
      #framing: for h1 framing n; add n counterclockwise twists of h2 about h1 (canonical framing)
      #compute differnce between blackboard and canonical framings
      #apply framing formula from pg 142

