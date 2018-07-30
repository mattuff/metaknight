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
      s+="}>"##Components: {"
##      for c in self.comp_list():
##         s+="Handle:"+ str(c.handle)+","
##         if c.handle==2:
##            str+="Framing:"+str(c.framing)+","
##         s+="Strands:["
##         for st in self.strand_list(c):
##            s+=str(st)+","
##         s+="]"
##         s+="}"
##      s+=">"
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

   def strand_list(self, comp): #returns an ordered list of strands given a component
      l=[]
      for c in self.crossings:
         for i in range (4):
            if (c[i].component==comp and c[i] not in l):
               l.append(c[i])
      for j in self.joins:
         for k in range (2):
            if (j[k].component==comp and j[k] not in l):
               l.append(j[k])
      for i in range (len(l)-1):
         if (l[i+1] != l[i].succ):
            for k in range (i, len(l)):
               if (l[k]==l[i].succ):
                  placeholder=l[i+1]
                  l[i+1]=l[k]
                  l[k]=placeholder
      return l

##   def strand_name(self):
##      return(max(map(lambda x:x.name,self.strands))+1)

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

   def add_join(self, s0): #s0 is strand to be split, s0 will be the predecessor of the new s1
      c0=s0.pred_con
      c1=s0.succ_con
      s1=strand(self.strand_name(),s0.component,s0,s0.succ,None,s0.succ_con)
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
      s=strand(self.strand_name(),j[0].component,j[0].pred,j[1].succ,j[0].pred_con,j[1].succ_con)
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

   def add_r1(self,x, sign, counterclockwise): #strand=strand to twist, sign=clockwise or counterclockwise twist (1 will add 1 to framing, 0 will subtract 1 from framing)

      f=x.component.framing
      w=x.succ
      y=strand(self.strand_name(), x.component, x)
      z=strand(self.strand_name()+1, x.component, y, w)
      z.set_succ_con=x.succ_con
      w.set_pred(z)
      x.set_succ(y)
      s=x.succ_con
      s.strands[s.strands.index(x)]=z

      #adds crossing
      if (sign%2):
         if counterclockwise:
            c = crossing(x,y,y,z)
         else:
            c = crossing(y,x,z,y)
         x.component.change_framing(f+1) #adds 1 to framing
      else:
         if counterclockwise:
            c = crossing(y,y,z,x)
         else:
            c = crossing(x,z,y,y)
         x.component.change_framing(f-1) #subtracts one from framing
      self.crossings.append(c) #adds crossing to crossing list 

      #changes succ and pred crossings of strands involved
      z.succ_con=s
      x.set_succ_con(c)
      y.set_pred_con(c)
      y.set_succ_con(c)
      z.set_pred_con(c)
      
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
##      l=(self.strand_lookup(s1.succ))+(self.strand_lookup(s2.succ))
      l=[s1.succ_con,s1.succ.succ_con,s2.succ_con,s2.succ.succ_con]
##      if(orientation):
##         c1=crossing(s1,s2.succ,s1.succ,s2)
##         c2=crossing(s1.succ,s2.succ,s1.succ.succ,s2.succ.succ)
##         s1.set_succ_con(c1)
##         s1.succ.set_pred_con(c1)
##         s1.succ.set_succ_con(c2)
##         s1.succ.succ.set_pred_con(c2)
##         s2.set_succ_con(c1)
##         s2.succ.set_pred_con(c1)
##         s2.succ.set_succ_con(c2)
##         s2.succ.succ.set_pred_con(c2)
##      else:
##         c1=crossing(s1,s2.succ,s1.succ,s2.succ.succ)
##         c2=crossing(s1.succ,s2.succ,s1.succ.succ,s2)
##         s1.set_succ_con(c1)
##         s1.succ.set_pred_con(c1)
##         s1.succ.set_succ_con(c2)
##         s1.succ.succ.set_pred_con(c2)
##         s2.set_succ_con(c2)
##         s2.succ.set_pred_con(c2)
##         s2.succ.set_succ_con(c1)
##         s2.succ.succ.set_pred_con(c1)
##      self.crossings+=[c1,c2]
##      for s in l:
##         self.joins.remove(s)
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

##   def remove_r2 (self,s1, s2): #strands s1 and s2
##      l=self.strand_lookup(s1)
##      if(s1.succ==s2.pred):
##         self.add_join(s1.succ)
##      if(s2.succ==s1.pred):
##         self.add_join(s2.succ)
##      for s in [s1,s2]:
##         s.set_succ(s.succ.succ)
##         s.succ.set_pred(s)
##         s.set_pred(s.pred.pred)
##         s.pred.set_succ(s)
##      for c in l:
##         if(c in self.crossings):
##            self.crossings.remove(c)

##   def remove_r2 (self,s1, s2): #strands s1 and s2
##      l=self.strand_lookup(s1)
##      if(s1.succ==s2.pred):
##         self.add_join(s1.succ)
##      if(s2.succ==s1.pred):
##         self.add_join(s2.succ)
##      for s in [s1,s2]:
##         s.set_succ(s.succ.succ)
##         s.succ.set_pred(s)
##         s.set_pred(s.pred.pred)
##         s.pred.set_succ(s)
##      for c in l:
##         if(c in self.crossings):
##            self.crossings.remove(c)

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

    #Pseudo code
   def add_r3(self, strandUnder, strandMiddle, strandOver):
       # strandUnder is the strand that goes under strandMiddle and strandOver, which we are going to move
      # strandMiddle goes over strandUnder and under strandOver
      # strandOver goes over strandUnder and strandMiddle
      # strands refer to triangle

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

   def handle_slide(self, h1, h2, sign): #h2 is being slid over h1; sign=True if same orientation
      #makes parallel copies of all strands in h1
      h2st=self.strand_list(h2)[0] #arbitrary strand in h2, pre-slide
      s=self.strand_list(h1) #list of strands in h1, in succ order
      ls=len(s) #original # of strands in h1
      l=[]
      comp_crossings=self.comp_crossings(h1) #crossings with only strands in h1
      comp_intersections=self.comp_intersections(h1) #crossings w 2 strands in h1, and 2 in another strand
      for k in range (len(s)): #sets up parallel copy of h1
         st=strand(self.strand_name()+k, h2)
         l+=[st]
      for i in range (len(l)): #sets up preds and succs
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

      for j in self.comp_joins(h1): #duplicates joins
         a=s.index(j[0])
         b=s.index(j[1])
         if (sign):
            jn=join(l[a],l[b])
         else:
            jn=join(l[b],l[a])
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
         if (b.succ==d):
            var=True
         else:
            var=False

         if (s.index(a)<s.index(c)):
            e=strand(self.strand_name()+ls+1, h1, a,c)
            s.insert(s.index(a)+1, e)
            if (sign):
               ee=strand(self.strand_name()+ls+2, h2, aa, cc)
            else:
               ee=strand(self.strand_name()+ls+3, h2, cc, aa)
            l.insert(l.index(aa)+1, ee)
         else:
            e=strand(self.strand_name()+ls+4, h1, c, a)
            s.insert(s.index(c)+1, e)
            if (sign):
               ee=strand(self.strand_name()+ls+5, h2, cc, aa)
            else:
               ee=strand(self.strand_name()+ls+6, h2, aa, cc)
            l.insert(l.index(cc)+1, ee)
         if (var):
            f=strand(self.strand_name()+ls+7, h1, b, d)
            s.insert(s.index(b)+1, f)
            if (sign):
               ff=strand(self.strand_name()+ls+8, h2, bb, dd)
            else:
               ff=strand(self.strand_name()+ls+9, h2, dd, bb)
            l.insert(l.index(bb)+1, ff)
         else:
            f=strand(self.strand_name()+ls+10, h1, d, b)
            s.insert(s.index(d)+1, f)
            if (sign):
               ff=strand(self.strand_name()+ls+11, h2, bb, dd)
            else:
               ff=strand(self.strand_name()+ls+12,h2, dd, bb)
            l.insert(s.index(d)+1, ff)
         self.crossings.remove(cx)

         if (sign):
            
            if (var):
               c1=crossing(a,f,e,d)
               c2=crossing(aa,b,ee,f)
               c3=crossing(ee,b,cc,ff)
               c4=crossing(e,ff,c,dd)

               b.set_succ_con(c2)
               f.set_pred_con(c2)
               f.set_succ_con(c1)
               d.set_pred_con(c1)

               bb.set_succ_con(c3)
               ff.set_pred_con(c3)
               ff.set_succ_con(c4)
               dd.set_pred_con(c4)
                
            else:
               c1=crossing(a,ff,e,dd)
               c2=crossing(aa,bb,ee,ff)
               c3=crossing(ee,b,cc,f)
               c4=crossing(e,f,c,d)

               aa.set_succ_con(c2)
               ee.set_pred_con(c2)
               ee.set_succ_con(c3)
               cc.set_pred_con(c3)

               b.set_pred_con(c2)
               f.set_succ_con(c2)
               f.set_pred_con(c1)
               d.set_succ_con(c1)

               bb.set_pred_con(c3)
               ff.set_succ_con(c3)
               ff.set_pred_con(c4)
               dd.set_succ_con(c4)

            a.set_succ_con(c1)
            e.set_pred_con(c1)
            e.set_succ_con(c4)
            c.set_pred_con(c4)

            aa.set_succ_con(c2)
            ee.set_pred_con(c2)
            ee.set_succ_con(c3)
            cc.set_pred_con(c3)
                
         else:
            
            if (var):
                c1=crossing(a,f,e,d)
                c2=crossing(ee,f,aa,b)
                c3=crossing(cc,ff,ee,bb)
                c4=crossing(ff,c,dd,e)

                b.set_succ_con(c2)
                f.set_pred_con(c2)
                f.set_succ_con(c1)
                d.set_pred_con(c1)

                bb.set_pred_con(c3)
                ff.set_succ_con(c3)
                ff.set_pred_con(c4)
                dd.set_succ_con(c4)
                
            else:
                c1=crossing(a,ff,e,dd)
                c2=crossing(ee,ff,aa,bb)
                c3=crossing(cc,f,ee,b)
                c4=crossing(e,f,c,d)

                b.set_pred_con(c3)
                f.set_succ_con(c3)
                f.set_pred_con(c4)
                d.set_succ_con(c4)

                bb.set_succ_con(c2)
                ff.set_pred_con(c2)
                ff.set_succ_con(c1)
                dd.set_pred_con(c1)

            a.set_succ_con(c1)
            e.set_pred_con(c1)
            e.set_succ_con(c4)
            c.set_pred_con(c4)

            aa.set_pred_con(c2)
            ee.set_succ_con(c2)
            ee.set_pred_con(c3)
            cc.set_succ_con(c3)
         
         self.crossings+=[c1,c2,c3,c4]

      for cx in comp_intersections: #turns crossings between h1 and another comp into 2 crossings
         if (cx[0].component==h1):
            a=cx[0]
            b=cx[1]
            c=cx[2]
            d=cx[3]
            aa=l[s.index(a)]
            cc=l[s.index(c)]
            f=strand(self.strand_name(), b.component)
            if (b.succ==d):
               f.set_pred(b)
               f.set_succ(d)
               if (sign):
                  c1=crossing(a,f,c,d)
                  c2=crossing(aa,b,cc,f)
                  a.set_succ_con(c1)
                  c.set_pred_con(c1)
                  aa.set_succ_con(c2)
                  cc.set_pred_con(c2)
                  
               else:
                  c1=crossing(a,f,c,d)
                  c2=crossing(cc,f,aa,b)
                  a.set_succ_con(c1)
                  c.set_pred_con(c1)
                  aa.set_pred_con(c2)
                  cc.set_succ_con(c2)
                  
               b.set_succ_con(c2)
               f.set_pred_con(c2)
               f.set_succ_con(c1)
               d.set_pred_con(c1)
               
            else:
               f.set_succ(b)
               f.set_pred(d)
               if (sign):
                  c1=crossing(a,f,c,d)
                  c2=crossing(aa,b,cc,f)
                  a.set_succ_con(c1)
                  c.set_pred_con(c1)
                  aa.set_succ_con(c2)
                  cc.set_pred_con(c2)
                  
               else:
                  c1=crossing(a,f,c,d)
                  c2=crossing(cc,f,aa,b)
                  a.set_succ_con(c1)
                  c.set_pred_con(c1)
                  aa.set_pred_con(c2)
                  cc.set_succ_con(c2)
                  
               b.set_pred_con(c2)
               f.set_succ_con(c2)
               f.set_pred_con(c1)
               d.set_succ_con(c1)  
         else:
            a=cx[0]
            b=cx[1]
            c=cx[2]
            d=cx[3]
            bb=l[s.index(b)]
            dd=l[s.index(d)]
            e=strand(self.strand_name(), a.component,a,c)
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
         self.crossings+=[c1,c2]

         #attaching parallel copy of h1 onto h2:
         #split self.strand_list(h2)[0] in two by adding join

      self.add_join(h2st) 
      self.joins.remove(h2st.succ_con)
      if (sign):
         jn1=join(h2st,l[0])
         jn2=join(l[-1],h2st.succ)
         h2st.set_succ_con(jn1)
         l[0].set_pred_con(jn1)
         l[-1].set_succ_con(jn2)
         h2st.succ.set_pred_con(jn2)
      else:
         jn1=join(h2st,l[-1])
         jn2=join(l[0],h2st.succ)
         h2st.set_succ_con(jn1)
         l[-1].set_pred_con(jn1)
         l[0].set_succ_con(jn2)
         h2st.succ.set_pred_con(jn2)
      self.joins+=[jn1,jn2]
      
      #framing: for h1 framing n; add n counterclockwise twists of h2 about h1 (canonical framing)
      #compute differnce between blackboard and canonical framings
      #apply framing formula from pg 142

      #connecting the parallel copy of h1 to the rest of h2 at some point??
      

   #have something to go from blackboard framing to canonical framing?
   #blackboard framing = canonical framing + n; solve for n
