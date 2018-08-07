# MetaKnight :watermelon:

developed by: Yael Eisenberg, Laura Stordy, and Matt Uffenheimer

MetaKnight (Manifolds Encoded Through the Architecture of Knots and Numbers In the Geometry of Handlebody Theory) is a Python Package for Kirby Calculus!

Kirby diagrams are a way of modeling 4-manifolds based off of their handlebody decomposition. The Kirby class takes planar diagrams as inputs, and can perform all the Kirby moves on the diagram: Reidemeister moves, handle annihilation, handle creation, and handle slides.

### Setting up a Planar Diagram

1. Set up components:  

The building blocks of all Kirby diagrams are the 1-handles and 2-handles. The component class, **componentClass.py** initializes these handles. The attributes of the components are its handle type and framing: ```component(1) ``` sets up a 1-handle, while ```component(2, f)``` sets up a 2-handle with blackboard framing *f*.

Let's set up the planar diagram for this unknot with framing 0.

![threestrandunknot](https://github.com/mattuff/KirbyCalculus/blob/master/Images/circleexample.png)

We start with ```comp=component(2,0)```.

2. Set up strands:

Every component is made up of strands. The strand class, **strandClass.py**, initializes these strands. The attributes of the strand are the component it belongs to, the strands directly before and after it, and the connections directly before and after it. It's set up by ```strand(comp, pred, succ, pred_con, succ_con)```.

Let's set up three strands for the unknot above (without worrying about the connections):
```
a=strand(comp)
b=strand(comp,a)
c=strand(comp,b,a)
a.set_pred(c)
a.set_succ(b)
b.set_succ(c)
```

3. Set up crossings and joins:

Crossings are intersections of four strands, and joins are intersections of two.

On each side of a strand is a crossing or a join, initaizted by **crossingClass.py** and **joinClass.py**.

Crossings are intiialized by the four strands they contain, listed counterclockwise with the incoming under strand first. For example, the crossing below would be set up by ```crossing(a,b,c,d)```.

![crossingex](https://github.com/mattuff/KirbyCalculus/blob/master/Images/crossingexample.png)

Joins are initialized by the two strands they contain, with the incoming strand first. For example, the join below would be set up by ```join(a,b)```.

Note: crossings and joins can be indexed like lists.

Now that we have crossings and joins, time to add them as attributes in our strands!

For our three-stranded circle above, let's put in some joins.

```
j1=join(a,b)
a.set_succ_con(j1)
b.set_pred_con(j1)
j2=join(b,c)
b.set_succ_con(j2)
c.set_pred_con(j2)
j3=join(c,a)
c.set_succ_con(j3)
a.set_pred_con(j3)
```
4. Compile everything into a Kirby object:

The Kirby class, **kirbyClass.py**, is where everything comes together. It's initialized with just lists of crossings and joins, but also stores lists of components and strands. Kirby diagrams are set up with ```Kirby([c_1,c_2,...,c_n],[j_1,j_2,...,j_n])``` where *c_i* and *j_i* are crossings and joins respectively.

Let's put our circle into a Kirby diagram: ```circ=Kirby([],[j1,j2,j3])```.

And that's it! Now we have a Kirby diagram to work with. Let's print *circ* and see if it works:
```
print(circ)
```
```
Components:
 - [1,2,3] (2-handle; f=0)
Crossings:
None
Joins:
[1,2],[2,3],[3,1]
```

##### Another Example

Sure, 0-framed unknots are great, but what if we want to make something more complicated– say, a trefoil linked through a 1-handle?

![trefoil_thru_one-handle](https://github.com/mattuff/KirbyCalculus/blob/master/Images/trefoil_1-handle.png)

First, let's set up the components:

```
trefoil = component(2,3)
one_handle = component(1)
```

Now the strands!

```
a = strand(trefoil)
b = strand(trefoil, a)
a.set_succ(b)
c = strand(trefoil, b)
b.set_succ(c)
d = strand(trefoil, c)
c.set_succ(d)
e = strand(trefoil, d)
d.set_succ(e)
f = strand(trefoil, e)
e.set_succ(f)
g = strand(trefoil, f)
f.set_succ(g)
h = strand(trefoil, g, a)
g.set_succ(h)
a.set_pred(h)

i = strand(one_handle)
j = strand(one_handle, i, i)
i.set_pred(j)
i.set_succ(j)
```
Onto the crossings:
```
c1 = crossing(a, f, b, g)
c2 = crossing(g, c, h, b)
c3 = crossing(i, d, j, c)
c4 = crossing(d, i, e, j)
c5 = crossing(e, a, f, h)
```
Setting up the preceeding and succeeding connections in strands:
```
a.set_succ_con(c1)
b.set_pred_con(c1)
b.set_succ_con(c2)
c.set_pred_con(c2)
c.set_succ_con(c3)
d.set_pred_con(c3)
d.set_succ_con(c4)
e.set_pred_con(c4)
e.set_succ_con(c5)
f.set_pred_con(c5)
f.set_succ_con(c1)
g.set_pred_con(c1)
g.set_succ_con(c2)
h.set_pred_con(c2)
h.set_succ_con(c5)
a.set_pred_con(c5)

i.set_succ_con(c3)
j.set_pred_con(c3)
j.set_succ_con(c4)
i.set_pred_con(c4)
```

And putting it all together!

```
tr1 = Kirby([c1,c2,c3,c4,c5],[])
```
Let's check what we get when we print.

```
print(tr1)
```
```
Components:
 - [1,2,3,4,5,6,7,8] (2-handle;f=3)
 - [9,10] (1-handle)
Crossings:
[1,6,2,7],[7,3,8,2],[9,4,10,3],[4,9,5,10],[5,1,6,8]
Joins:
None
```
And... it worked!

Now how do we manipulate these diagrams?

### Kirby Moves
