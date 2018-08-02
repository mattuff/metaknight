from kirbyClass import *
from crossingClass import *
from joinClass import *
from strandClass import *
from componentClass import *

#fixed PD diagrams:

#unknot w/ an R1:
knot=component(2,1)
y=strand(knot)
z=strand(knot,y,y)
y.set_pred(z)
y.set_succ(z)
x=crossing(y,y,z,z)
y.set_pred_con(x)
z.set_pred_con(x)
y.set_succ_con(x)
z.set_succ_con(x)
unknot_r1=Kirby([x], [])

#trefoil
tr=component(2,3)
a=strand(tr)
b=strand(tr,a)
c=strand(tr,b)
d=strand(tr,c)
e=strand(tr,d)
f=strand(tr,e,a)
a.set_pred(f)
a.set_succ(b)
b.set_succ(c)
c.set_succ(d)
d.set_succ(e)
e.set_succ(f)
c1=crossing(a,e,b,d)
c2=crossing(e,c,f,b)
c3=crossing(c,a,d,f)
a.set_pred_con(c3)
a.set_succ_con(c1)
b.set_pred_con(c1)
b.set_succ_con(c2)
c.set_pred_con(c2)
c.set_succ_con(c3)
d.set_pred_con(c3)
d.set_succ_con(c1)
e.set_pred_con(c1)
e.set_succ_con(c2)
f.set_pred_con(c2)
f.set_succ_con(c3)
trefoil=Kirby([c1,c2,c3],[])

#cancelling pair
h1=component(1)
h2=component(2,0)
f=strand(h1)
g=strand(h1,f,f)
f.set_pred(g)
f.set_succ(g)
h=strand(h2)
i=strand(h2,h,h)
h.set_pred(i)
h.set_succ(i)
cx1=crossing(f,h,g,i)
cx2=crossing(h,f,i,g)
f.set_pred_con(cx2)
f.set_succ_con(cx1)
g.set_pred_con(cx1)
g.set_succ_con(cx2)
h.set_pred_con(cx1)
h.set_succ_con(cx2)
i.set_pred_con(cx2)
i.set_succ_con(cx1)
cnpair=Kirby([cx1,cx2],[])

#unknot
knt=component(2,0)
j=strand(knt)
j.set_succ(j)
j.set_pred(j)
j1=join(j,j)
j.set_pred_con(j1)
j.set_succ_con(j1)
unknot=Kirby([],[j1])

#unknot w/ r2
kt=component(2,0)
k=strand(kt)
l=strand(kt,k)
m=strand(kt,l)
n=strand(kt,m,k)
k.set_pred(n)
k.set_succ(l)
l.set_succ(m)
m.set_succ(n)
cr1=crossing(k,k,n,l)
cr2=crossing(m,l,n,m)
k.set_pred_con(cr1)
k.set_succ_con(cr1)
l.set_pred_con(cr1)
l.set_succ_con(cr2)
m.set_pred_con(cr2)
m.set_succ_con(cr2)
n.set_pred_con(cr2)
n.set_succ_con(cr1)
unknot_r2=Kirby([cr1, cr2],[])

#another unknot but w two joins this time!
ukt=component(2,0)
o=strand(ukt)
p=strand(ukt,o,o)
o.set_pred(p)
o.set_succ(p)
jn1=join(o,p)
jn2=join(p,o)
o.set_pred_con(jn1)
o.set_succ_con(jn2)
p.set_pred_con(jn2)
p.set_succ_con(jn1)
unknot2=Kirby([],[jn1,jn2])

mc=component(2,0)
ma=strand(mc)
mb=strand(mc,ma,ma)
ma.pred=mb
ma.succ=mb
md=crossing(mb,ma,ma,mb)
for i in [ma,mb]:
   i.set_pred_con(md)
   i.set_succ_con(md)
me=Kirby([md],[])


#disjoint trefoil and unknot
trefoil_unknot=Kirby([c1,c2,c3],[j1])

#disjoint unknot and cancelling pair
unknot_cancelling_pair=Kirby([cx1,cx2],[j1])
