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
      self.components=self.comp_list() #makes list of components
      for c in self.components:
         c.kirby=self

   def __str__(self): #prints planar diagram
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
   
   def __getitem__(self,key):
      return(self.comp_list()[key])

   def comp_list(self): #returns list of components
      l=[]
      for x in self.strands:
         if(x.component not in l):
            l.append(x.component)
      return(l)

   def strand_list(self, s): #returns an ordered list of strands in a component given a starting strand
      l=[s]
      t=s.succ
      while(t!=s):
         l.append(t)
         t=t.succ
      return l

   def switch(self,c): #switches overcrossing strand given a component
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

   def rename_all(self): #renames every strand
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

   def connect_sum(self,s0,s1): #connect sums two components given a strand from each
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

   def writhe(self,c): #given a component, returns writhe
      return(sum(list(map(lambda x:(-1)**(x[1]==x[3].pred),self.comp_crossings(c)))))

   def linking_number(self,h1,h2): #given two components, returns linking number
      l=0
      for c in list(set(self.comp_intersections(h1) and self.comp_intersections(h2))):
         if (c[0].component==h1):
            if (c[1].succ==c[3]):
               l+=(-1)
            else:
               l+=1
      return l

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

   def add_r1(self, x, o, i):  # x=strand to twist, o determines orientation of twist (T=ccw,F=cw), i =T if incoming strand is over, =F if under
      x.component.framing+=(-1)**(o==i) #changes framing
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
      c=x.succ_con
      x.pred.set_succ_con(j1)
      x.set_succ_con(j2)
      x.set_pred_con(j1)
      x.succ.set_pred_con(j2)
      self.joins+=[j1,j2]

      if (((c[0]==c[1]) and c[0]==x.succ) or ((c[2]==c[3]) and c[2]==x.succ)):
         x.component.framing+=(-1)
      else:
         x.component.framing+=(1)

   def add_r2(self,s1,s2,o): #orientation is a boolean which is true if the strands are oriented the same way, and false otherwise
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
      c2 = strandUnder.succ_con

      if(strandMiddle.pred_con != c1 and strandMiddle.pred_con != c2): c3 = strandMiddle.pred_con
      else: c3 = strandMiddle.succ_con


      strandOrient = lambda s: s.pred if (s.pred in c3) else s.succ

      #add unofficial joins to list
      fixJoin = lambda s: join(s, s.succ) if s.succ not in c3 else join(s.pred, s)
      self.joins.append(fixJoin(strandMiddle))
      self.joins.append(fixJoin(strandOver))

      #add real joins which will turn into crossings
      self.add_join(strandOrient(strandMiddle))
      self.add_join(strandOrient(strandOver))

      oldC1 = crossing(c1[0],c1[1],c1[2],c1[3])#for some reason plain old c1 is changing instead of remainging constant

      #python is being annoying and not letting me consolidate even to one 'for' statement (won't produce correct results)
      for j in self.joins:
         if(strandOrient(strandMiddle) in j): self.joins.remove(j)

      for j in self.joins:
         if(strandOrient(strandOver) in j): self.joins.remove(j)


      crTest = lambda strand1, cross1, strand2, cross2: True if(strand1 in cross1 and strand2 in cross2) else False

      crossSet = lambda strand1, strand2, b: c1.set_strands(strandUnder.pred, strand1, strandUnder, strand2) if(b == True) \
         else c2.set_strands(strandUnder, strand1, strandUnder.succ, strand2)

      #redefine c1
      if (crTest(strandMiddle.pred, c3, strandOver, c1)): crossSet(strandMiddle.pred.pred,strandMiddle.pred, 1)
      elif (crTest(strandOver.pred, c3, strandOver, c2)): crossSet(strandOver.pred, strandOver.pred.pred, 1)
      elif (crTest(strandMiddle.succ, c3, strandOver, c1)): crossSet(strandMiddle.succ.succ, strandMiddle.succ, 1)
      elif (crTest(strandOver.succ, c3, strandOver, c2)): crossSet(strandOver.succ, strandOver.succ.succ, 1)

      #redefine c2 - use oldC1 since c1 gets redefined above
      if (crTest(strandMiddle.pred, c3, strandOver, c2)): crossSet(strandMiddle.pred, strandMiddle.pred.pred, 2)
      elif (crTest(strandOver.pred, c3, strandOver, oldC1)): crossSet(strandOver.pred.pred, strandOver.pred, 2)
      elif (crTest(strandMiddle.succ, c3, strandOver, c2)): crossSet(strandMiddle.succ, strandMiddle.succ.succ, 2)
      elif (crTest(strandOver.succ, c3, strandOver, oldC1)): crossSet(strandOver.succ.succ, strandOver.succ, 2)

      #reset pred_con/succ_con
      c1[0].set_succ_con(c1)
      c1[2].set_pred_con(c1)
      c2[0].set_succ_con(c2)
      c2[2].set_pred_con(c2)

      #maybe theres a way to consolidate this
      if(c1[1] in c3 and c1[1].pred in c1):
         c1[1].set_pred_con(c1)
         c1[1].set_succ_con(c3)
         c1[3].set_succ_con(c1)

      if(c1[1] in c3 and c1[1].pred not in c1):
         c1[1].set_pred_con(c3)
         c1[1].set_succ_con(c1)
         c1[3].set_pred_con(c1)

      if(c2[1] in c3 and c2[1].pred in c2):
         c2[1].set_pred_con(c2)
         c2[1].set_succ_con(c3)
         c2[3].set_succ_con(c2)

      if(c2[1] in c3 and c2[1].pred not in c2):
         c2[1].set_pred_con(c3)
         c2[1].set_succ_con(c2)
         c2[3].set_pred_con(c2)

         
   def handle_annihilation(self,h1,h2=None): #h1,h2 strands
      self.remove_joins()
      #checks to make sure each handle only has 2 strads (all joins must be removed)
      if (h2!=None):
         if (len(self.strand_list(h1))==2 and len(self.strand_list(h2))==2):
            if ((h1.pred_con==h2.pred_con) or (h1.pred_con==h2.succ_con)):
               for i in [h1,h1.succ,h2,h2.succ]:
                  self.strands.remove(i)
               self.crossings.remove(h1.succ_con)
               self.crossings.remove(h1.pred_con)
               self.components.remove(h1.component)
               self.componets.remove(h2.component)
      #cancels out an unknot w framing=0
      else:
         if (len(self.strand_list(h1))==1):
            if (h1.component.framing==0):
               self.joins.remove(h1.succ_con)
               self.strands.remove(h1)
               self.components.remove(h1.component)
            
   def handle_creation(self, f=None): #f=framing for 2-handle to have
      if (f!=None):
         h1=component(1)
         h2=component(2,f)
         h1.kirby=self
         h2.kirby=self
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
         self.components+=[h1,h2]
      else:
         h1=component(2,0)
         h1.kirby=self
         a=strand(h1)
         a.set_pred(a)
         a.set_succ(a)
         j=join(a,a)
         a.set_succ_con(j)
         a.set_pred_con(j)
         self.joins.append(j)
         self.strands.append(a)
         self.components.append(h1)
      

   def handle_slide(self, h1, h2, sign): #h2 is being slid over h1; sign=True if same orientation
      #makes parallel copies of all strands in h1
      s=self.strand_list(h1) #list of strands in h1, in succ order
      l=[]
      comp_crossings=self.comp_crossings(h1.component) #crossings with only strands in h1
      comp_intersections=self.comp_intersections(h1.component) #crossings w 2 strands in h1, and 2 in another strand

      sf1=self.writhe(h1.component)-h1.component.framing #seifert framing of first handle
      sf2=self.writhe(h2.component)-h2.component.framing #seifert framing of second handle
      lk=self.linking_number(h1.component,h2.component) #linking number of two handles

      #can considate, use ternary operator?
      for k in range (len(s)): #sets up parallel copy of h1
         l.append(strand(h2.component))
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
               f.set_succ_con(c1)
               d.set_pred_con(c1)
               b.set_succ_con(c2)
               f.set_pred_con(c2)

               bb.set_succ_con(c3)
               ff.set_pred_con(c3)
               ff.set_succ_con(c4)
               dd.set_pred_con(c4)
      
            else:
               dd.set_succ_con(c1)
               ff.set_pred_con(c1)
               ff.set_succ_con(c2)
               bb.set_pred_con(c2)
               
               f.set_succ_con(c3)
               b.set_pred_con(c3)
               d.set_succ_con(c4)
               f.set_pred_con(c4)
            
         else:
            cc.set_succ_con(c3)
            ee.set_pred_con(c3)
            ee.set_succ_con(c2)
            aa.set_pred_con(c2)

            f1 = lambda x : b if x else bb
            f2 = lambda x : f if x else ff
            f3 = lambda x : d if x else dd

            f1(var).set_succ_con(c2)
            f2(var).set_pred_con(c2)
            f2(var).set_succ_con(c2)
            f3(var).set_pred_con(c1)
            f3(not var).set_succ_con(c4)
            f2(not var).set_pred_con(c4)
            f2(not var).set_succ_con(c3)
            f1(not var).set_pred_con(c3)

      for cx in comp_intersections: #turns crossings between h1 and another comp into 2 crossings
         if (cx[0].component==h1.component):
            a=cx[0]
            b=cx[1]
            c=cx[2]
            d=cx[3]
            aa=l[s.index(a)]
            cc=l[s.index(c)]
            f=strand(b.component)
            self.strands+=[f]
            c1=crossing(a,f,c,d)
            a.set_succ_con(c1)
            c.set_pred_con(c1)
            if (b.succ==d):
               f.set_pred(b)
               f.set_succ(d)
               f1 = lambda x : b if x else f
               f2 = lambda x : aa if x else cc
               c2=crossing(f2(sign),f1(sign),f2(not sign),f1(not sign))
               f2(sign).set_succ_con(c2)
               f2(not sign).set_pred_con(c2)
               b.set_succ_con(c2)
               f.set_pred_con(c2)
               f.set_succ_con(c1)
               d.set_pred_con(c1)
            else:
               f.set_pred(d)
               f.set_succ(b)
               f1 = lambda x : aa if x else cc
               f2 = lambda x : b if x else f
               c2=crossing(f1(sign),f2(sign),f1(not sign),f2(not sign))
               f1(sign).set_succ_con(c2)
               f1(not sign).set_pred_con(c2)
               d.set_succ_con(c1)
               f.set_pred_con(c1)
               f.set_succ_con(c2)
               b.set_pred_con(c2)
         else:
            a=cx[0]
            b=cx[1]
            c=cx[2]
            d=cx[3]
            bb=l[s.index(b)]
            dd=l[s.index(d)]
            e=strand(a.component,a,c)
            a.set_succ(e)
            c.set_pred(e)
            self.strands+=[e]
            if (b.succ==d):
               c1=crossing(a,b,e,d)
               c2=crossing(e,bb,c,dd)
               b.set_succ_con(c1)
               d.set_pred_con(c1)
               f1 = lambda x : bb if x else dd
               f1(sign).set_succ_con(c2)
               f1(not sign).set_pred_con(c2)
            else:
               c1=crossing(a,bb,e,dd)
               c2=crossing(e,b,c,d)
               d.set_succ_con(c2)
               b.set_pred_con(c2)
               f1 = lambda x : dd if x else bb
               f1(sign).set_succ_con(c1)
               f1 (not sign).set_pred_con(c1)
            a.set_succ_con(c1)
            e.set_pred_con(c1)
            e.set_succ_con(c2)
            c.set_pred_con(c2)
               
         self.crossings+=[c1,c2]


      #adding extra twists for framing
      pos=(h1.component.framing>0)
         
      if (sign):
         for i in range(abs(h1.component.framing)):
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
            if (pos): #clockwise twists
               c1=crossing(l1,s2,l2,s1)
               c2=crossing(s2,l3,s3,l2)
            else: #counterclockwise twists
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

      else:
         for i in range(abs(h1.component.framing)):
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
            if (pos): #counterclockwise twists
               c1=crossing(l2,s1,l3,s2)
               c2=crossing(s2,l1,s3,l2)
            else: #clockwise twists
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

      self.connect_sum(h2,l[0])
      self.remove_joins()

      fr=sf1+sf2+((-1)**(not sign))*lk #sets new seifert framing
      
      h2.component.framing=int(self.writhe(h2.component)+fr) #taking back to blackbaord
