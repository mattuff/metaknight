from kirbyClass import *
from crossingClass import *
from joinClass import *
from strandClass import *
from componentClass import *

##c=[None]*4
##a=[None]*4
##j=[None]*4
##k=[None]*4
##for i in range(4):
##   c[i]=component(2,0)
##   a[i]=strand(c[i])
##   j[i]=join(a[i],a[i])
##   a[i].pred=a[i]
##   a[i].succ=a[i]
##   a[i].pred_con=j[i]
##   a[i].succ_con=j[i]
##   k[i]=Kirby([],[j[i]])
##   k[i].add_join(a[i])
##   print(k[i])
##   print("...becomes...")
##   k[i].add_r1(a[i],1-(i//2),1-(i%2))
##   print(str(k[i])+"\n")

##c=component(2,-1)
##s=strand(c)
##s.pred=s
##s.succ=s
##j=join(s,s)
##k=Kirby([],[j])
##k.set_cons(j)
##k.add_r1(s,True,False)
##k.add_r2(s,s.succ,False,True)
##k.switch(k[1].succ_con)
##k.remove_joins()
##print(k)

##c=s=j=[]
##for i in range(3):
##   c.append(component(2,0))
##   s.append(strand(c[i]))
##   s[i].pred=s[i]
##   s[i].succ=s[i]
##   j.append(join(s[i],s[i]))
##   s[i].pred_con=j[i]
##   s[i].succ_con=j[i]
####k=Kirby([],j)
####print(k)
##print(type(j))
##print(type(j[0]))

##c=s=j=[None]*3
##c0=component(2,0)
##s0=strand(c0)
##s0.pred=s0
##s0.succ=s0
##j0=join(s0,s0)
##s0.pred_con=j0
##s0.succ_con=j0
##c1=component(2,0)
##s1=strand(c1)
##s1.pred=s1
##s1.succ=s1
##j1=join(s1,s1)
##s1.pred_con=j1
##s1.succ_con=j1
##c2=component(2,0)
##s2=strand(c2)
##s2.pred=s2
##s2.succ=s2
##j2=join(s2,s2)
##s2.pred_con=j2
##s2.succ_con=j2
##k=Kirby([],[j0,j1,j2])
##print(type(s0.pred_con))
##print(type(k.strands[0].pred_con))
##print(k)
##k.add_r2(k[1],k[2],False,False)
##print(k)

c,s,j=[None]*3,[None]*3,[None]*3
for i in range(3):
   c[i]=component(2,0)
   s[i]=strand(c[i])
   s[i].pred=s[i]
   s[i].succ=s[i]
   j[i]=join(s[i],s[i])
   s[i].pred_con=j[i]
   s[i].succ_con=j[i]
k=Kirby([],j)
k.add_r2(k[1],k[2],False,False)
k.add_r2(k[3],k[7],False,False)
k.add_r2(k[6],k[11],False,False)
k.add_r3(k[13],k[8],k[3])
print(k)
