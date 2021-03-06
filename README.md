# MetaKnight :watermelon:

Developed by: Yael Eisenberg, Laura Stordy, and Matt Uffenheimer

MetaKnight (Manifolds Encoded Through the Architecture of Knots and Numbers In the Geometry of Handlebody Theory) is a Python Package for Kirby Calculus!

Kirby diagrams are a method of modeling 4-manifolds based off of their handlebody decomposition. The Kirby class inputs planar diagrams of Kirby diagrams in circle-dot notation, and can perform all the Kirby moves on the diagram: Reidemeister moves, handle annihilation, handle creation, and handle slides.

### Setting up a Planar Diagram

1. Set up components:  

The building blocks of all Kirby diagrams are the 1-handles and 2-handles. The component class, **componentClass.py** initializes these handles. The attributes of the components are its handle type and framing: ```component(1) ``` sets up a 1-handle, while ```component(2, f)``` sets up a 2-handle with blackboard framing *f*.

Let's set up the planar diagram for this unknot with framing 0.

![threestrandunknot](https://github.com/mattuff/KirbyCalculus/blob/master/Images/circleexample.png)

We start with ```comp=component(2,0)```.

2. Set up strands:

Every component is composed of strands. The strand class, **strandClass.py**, initializes these strands. The attributes of the strand are the component it belongs to, the strands directly before and after it, and the crossings directly before and after it. It's initialized by ```strand(comp, pred, succ, pred_con, succ_con)```.

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

Crossings are intersections of four strands, and joins are intersections of two strands.

On both sides of a strand there is a crossing or a join, initailized by **crossingClass.py** and **joinClass.py**.

Crossings are intiialized by the four strands they contain, listed counterclockwise with the incoming under strand first. For example, the crossing below would be set up by ```crossing(a,b,c,d)```.

![crossingex](https://github.com/mattuff/KirbyCalculus/blob/master/Images/crossingexample.png)

Joins are initialized by the two strands they contain, with the incoming strand first.

Note: crossings and joins can be indexed like lists.

Now that we have crossings and joins, time to add them as attributes in our strands!

For our three-stranded circle above, let's insert some joins.

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

The Kirby class, **kirbyClass.py**, is where everything comes together. It's initialized with lists of crossings and joins, but also stores lists of components and strands. Kirby diagrams are set up with ```Kirby([c_1,c_2,...,c_n],[j_1,j_2,...,j_n])``` where *c_i* and *j_i* are crossings and joins respectively.

Let's turn our circle into a Kirby diagram: ```circ=Kirby([],[j1,j2,j3])```.

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

#### Another Example

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
Setting up the strands' preceeding and succeeding connections:
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

Setting *pred_con*s and *succ_con*s seems like a lot right now, but don't worry! Once you put everything together into a Kirby diagram *k*, ```k.set_all_cons()``` will take care of it for you.

And putting it all together!

```
tr1 = Kirby([c1,c2,c3,c4,c5],[])
```
Let's print tr1:

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

#### Reidemeister 1

##### Adding a Reidemeister 1: ```k.add_r1(x,o,i)```

![r1](https://github.com/mattuff/KirbyCalculus/blob/master/Images/r1.png)

Applying a Reidemeister 1 to the strand on the left– let's call it *x*, in a Kirby diagram *k*– can produce any of the four loops on the right. 

The loops on the right depend on two things: whether the incoming strand goes over or under, and whether the strand goes clockwise or counterclockwise inside of the loop. 

These are determined by two booleans, *o* and *i*: *o* is ```True``` if the loop goes counterclockwise, ```False``` if the loop goes clockwise; and *i* is ```True``` if the incoming strand goes over, ```False``` if the incoming strand goes under.

In the above image, the top left corresponds to ```k.add_r1(a, True, False)```, top right ```k.add_r1(a, False, False)```, bottom left ```k.add_r1(a, True, False)```, and bottom right ```k.add_r1(a, False, True)```.

##### Removing a Reidemiester 1: ```k.remove_r1(x)```

![r1again](https://github.com/mattuff/KirbyCalculus/blob/master/Images/coloredr1.png)

Removing a Reidemeister 1 is easy! Let's call the blue strand above *x* on a Kirby diagram *k*.

Then, to remove it would just be ```k.remove_r1(x)```!

#### Reidemeister 2

##### Adding a Reidemeister 2: ```k.add_r2(s1,s2,o,d)```

![r2](https://github.com/mattuff/KirbyCalculus/blob/master/Images/r2.png)

Let the black strand be *a*, and the red strand be *b* in a Kirby diagram *k*. 

In all four cases of a Reidemeister 2 shown above, *a* is being pulled above *b*. The cases differ by orientations of *a* and *b*, and if *b* is to the right or left of *a*. 

Similarly to Reidemeister 1, these are determined by two booleans: *o* and *s*: *o* is ```True``` if the strands are oriented the same way, ```False``` if they have opposite orientations; and *s* is ```True``` if *b* is to the right of *a*, ```False``` otherwise.

In the above image, the top left corresponds to ```k.add_r2(a,b,True,True)```, the top right ```k.add_r2(a,b,True,False)```, the bottom left ```k.add_r2(a,b,False,True)```, and the bottom right ```k.add_r2(a,b,False,False)```.

##### Removing a Reidemeister 2: ```k.remove_r2(s0,s1)```

![r2again](https://github.com/mattuff/KirbyCalculus/blob/master/Images/coloredr2.png)

Removing a Reidemeister 2 is easy as well! Let's call the blue strand above *a* and the red strand *b* (again, on a Kirby diagram *k*).

To remove the Reidemeister 2 is ```k.remove_r2(a,b)```.

#### Reidemeister 3: ```k.add_r3(strandUnder,strandMiddle,strandOver)```

![r3](https://github.com/mattuff/KirbyCalculus/blob/master/Images/r3.png)

A Reidemiester 3 moves a strand *a* to the other side of a crossing (where *a* is the under strand in the crossing, shown in green above, *b* is the 'middle' strand going over the understrand and over another strand, shown in black above, and *c* the over strand in the crossing, shown in purple above). On a Kirby diagram *k*, we perform a Reidememiester 3 by ```k.add_r3(a,b,c)```.

Implementing and removing a Reidemeister 3 are equivalent.

#### Handle Annihilation and Creation

##### Cancel a cancelling pair: ```k.handle_annihilation(h1,h2)```

##### Adding a cancelling pair: ```k.handle_creation(f)```

![cancellingpair](https://github.com/mattuff/KirbyCalculus/blob/master/Images/cancellingpair.png)

A linked 1-handle and unknot 2-handle of any framing can be cancelled without changing the manifold. Similarly, they can be added without changing anything.

To cancel such a pair on a diagram *k*, where *a* is a strand from one component and *b* is a strand from the other: ```k.handle_annihilation(a,b)```.

To add such a pair on *k*, where you want the unknot to have framing *f*: ```k.handle_creation(f)```.

##### Cancelling an unknot: ```k.handle_annihilation(h1)```

##### Adding an unknot: ```k.handle_creation()```

![unknot0](https://github.com/mattuff/KirbyCalculus/blob/master/Images/unknot.png)

Additionally, an unknot 2-handle with framing 0 can be added to or cancelled from any diagram.

To cancel an unknot on a diagram *k*, where *a* is a strand in the unknot : ```k.handle_annihilation(a)```.

To add an unknot on *k* : ```k.handle_creation()```.

#### Handle Slides: ```k.handle_slide(h1,h2,sign)```

![handleslides](https://github.com/mattuff/KirbyCalculus/blob/master/Images/handleslides.png)

A handle slide quite literally slides one handle– let's call it *B*, in red above, over another– *A*, in black above, in a Kirby diagram *k*.

This is done by making a parallel copy to the right of all the strands in *A*, adjusting crossings (each crossing in *A* turns into four!), and attaching the parallel copy of *A* onto *B*. If *A* has blackboard framing *f*, we add *f* clockwise/counterclockwise (depending on sign) twists to *B* about *A*. The framing of *B* is changed as well.

Handle slides can either be handle addition (where the parallel copy of *A* is oriented the same as *A*), or handle subtraction (where *A* and its parallel copy have opposite orientations).

Let *a* be a strand in *A* and *b* be a strand in *B*.

Handle addition is done by ```k.handle_slide(a,b,True)``` and handle subtraction by ```k.handle_slide(a,b,False)```.

### Other Methods

```k.switch(c)```:

   Given a crossing *c*, switches its over and under strands.
 
```k.set_cons(c)```:

  Given a crossing *c*, sets *pred_con* and *succ_con* of strands within *c*.
  
```k.set_all_cons()```:

   Applies *set_cons* to every crossing in the Kirby class.
 
```k.comp_crossings(h1)```:

   Given a component *h1*, returns list of all crossings fully contained in *h1*.
  
```k.comp_joins(h1)```:

   Given a component *h1*, returns a list of all joins contained in *h1*.
  
```k.comp_intersection(h1)```:

   Given a component *h1*, returns a list of crossings between *h1* and another component.
   
```k.writhe(c)```:

   Given a component *c*, returns its writhe.
   
```k.linking_number(h1,h2)```:

   Given two components *h1* and *h2*, returns their linking number.
   
```k.add_join(s0)```:

   Adds a join onto a strand *s0*.
   
```k.remove_join(j)```:

   Removes a join *j* from diagram.
   
```k.remove_joins()```:

   Removes all joins from diagram.
   
```k.disjoint_union(k2)```:

   Replaces Kirby diagram *k* with the disjoint union of *k* and another diagram, *k2*.
   
```k.reverse(c)```:

   Changes orientation given a component *c*.
