---
layout: post
title: Set periodic boundary conditions in VMD
---

Sometimes trajectories from programs does not include the information about the periodic boundary conditions. For a cubic box this is easy to specify on via the TCL terminal. This can be specified by the following two commands.

{% highlight tcl %}
pbc set {X Y Z} -all -molid top
pbc box -center origin -shiftcenter {cX cY cZ}
{% endhighlight %}

The first command sets the size of the box for all frames.
"X", "Y" and "Z" have to be specified in Angstrom.
The next command sets the origin of the box.
"cX", "cY" and "cZ" is specified as the starting location of the box.
The default is just (0, 0, 0).
