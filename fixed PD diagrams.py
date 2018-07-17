#fixed PD diagrams:

#unknot w/ an R1:
knot=component(2,1)
a=strand(knot,1)
b=strand(knot,2,a,a)
a.set_pred(b)
a.set_succ(b)
x=crossing(a,a,b,b)
unknot_r1=Kirby([x], [])

#trefoil
tr=component(2,3)
a=strand(tr,1)
b=strand(tr,2,a)
c=strand(tr,3,b)
d=strand(tr,4,c)
e=strand(tr,5,d)
f=strand(tr,6,e,a)
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
