# MetaKnight

developed by: Yael Eisenberg, Laura Stordy, and Matt Uffenheimer

MetaKnight (Manifolds Encoded Through the Architecture of Knots and Numbers In the Geometry of Handlebody Theory) is a Python Package for Kirby Calculus!

Kirby diagrams are a way of modeling 4-manifolds based off of their handlebody decomposition. The Kirby class takes planar diagrams as inputs, and can perform all the Kirby moves on the diagram: Reidemeister moves, handle annihilation, handle creation, and handle slides.

### Setting up a Kirby Diagram

1. Set up components:  

The building blocks of all Kirby diagrams are the 1-handles and 2-handles. The component class, **componentClass.py** initializes these handles. The attributes of the components are its handle type and framing: ```component(1) ``` sets up a 1-handle, while ```component(2, f)``` sets up a 2-handle with blackboard framing *f*.

2. Set up strands:

Every component is made up of strands. The strand class, **strandClass.py**, initializes these strands. The attributes of the strand are the component it belongs to, the strands directly before and after it, and the connections directly before and after it. It's set up by ```strand(comp, pred, succ, pred_con, succ_con)```.

Let's set up three strands going in a circle in the component *comp* (without worrying about the connections):
```
a=strand(comp)
b=strand(comp,a)
c=strand(comp,b,a)
a.set_pred(c)
a.set_succ(b)
b.set_succ(c)
```

3. Set up crossings and joins:

On each side of a strand is a crossing or a join, initaizted by **crossingClass.py** and **joinClass.py** respectively.

Crossings are intiialized by the four strands they contain, listed counterclockwise with the incoming under strand first. For example, the crossing below would be set up by ```crossing(a,b,c,d)```.

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

The Kirby class, **kirbyClass.py**, is where everything comes together. It's initialized with just lists of crossings and joins, but also stores lists of components and strands. Kirby diagrams are set up with ```Kirby([c1,c2,...,c_n],[])```

Let's put our circle into a Kirby diagram: ```circ=Kirby([],[j1,j2,j3])```.

And that's it! Now we have a Kirby diagram to work with.


###Kirby Moves
