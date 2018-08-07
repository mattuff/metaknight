# MetaKnight

developed by: Yael Eisenberg, Laura Stordy, and Matt Uffenheimer

MetaKnight (Manifolds Encoded Through the Architecture of Knots and Numbers In the Geometry of Handlebody Theory) is a Python Package for Kirby Calculus!

Kirby diagrams are a way of modeling 4-manifolds based off of their handlebody decomposition. The Kirby class takes planar diagrams as inputs, and can perform all the Kirby moves on the diagram: Reidemeister moves, handle annihilation, handle creation, and handle slides.

### Inputting a PD

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

Crossings and joins can be indexed like lists.
