from kirbyClass import *
from crossingClass import *
from joinClass import *
from strandClass import *
from componentClass import *

#fixed PD diagrams:

#unknot w/ an R1:
knot=component(2,1)
y=strand(1,knot)
z=strand(2,knot,y,y)
y.set_pred(z)
y.set_succ(z)
x=crossing(y,y,z,z)
unknot_r1=Kirby([x], [])

#trefoil
tr=component(2,3)
a=strand(1,tr)
b=strand(2,tr,a)
c=strand(3,tr,b)
d=strand(4,tr,c)
e=strand(5,tr,d)
f=strand(6,tr,e,a)
a.set_pred(f)
a.set_succ(b)
b.set_succ(c)
c.set_succ(d)
d.set_succ(e)
e.set_succ(f)
c1=crossing(a,e,b,d)
c2=crossing(e,c,f,b)
c3=crossing(c,a,d,f)
trefoil=Kirby([c1,c2,c3],[])

#cancelling pair
h1=component(1)
h2=component(2,3)
f=strand(1,h1)
g=strand(2,h1,f,f)
f.set_pred(g)
f.set_succ(g)
h=strand(3,h2)
i=strand(4,h2,h,h)
h.set_pred(i)
h.set_succ(i)
cx1=crossing(f,h,g,i)
cx2=crossing(h,f,i,g)
cnpair=Kirby([cx1,cx2],[])
