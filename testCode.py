from kirbyClass import *
from crossingClass import *
from joinClass import *
from strandClass import *
from componentClass import *

#fixed PD diagrams:

#unknot w/ an R1:
knot=component(2,1)
a=strand(1,knot)
b=strand(2,knot,a,a)
a.set_pred(b)
a.set_succ(b)
x=crossing(a,a,b,b)
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
