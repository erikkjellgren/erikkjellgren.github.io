---
layout: post
title: Making RESP charges for AMBER calculations
---

Most organic molecules are not explicitly included in the force fields use in [Amber](https://ambermd.org/).
For these kinds of molecules the GAFF in Amber can be used. 
This force field includes all the bonded and the Lennard-Jones parameters. 
Thus when using these kind of general force field, charges are still needed to account for the electrostatic interactions.
In Amber these charges can be found by doing a restrained electrostatic potential fit (RESP).
RESP can be done using Antechamber, which is a part of the Amber program.
The RESP calculation in Antechamber requires an electro static potential (ESP).
This ESP can be calculated using Gaussian, which then produces a file that can immediately be used by Antechamber.
A minimal [Gaussian](https://gaussian.com/) input file, used to make an ESP for RESP can be seen below:

{% highlight txt %}
%NProcShared="NUMBER PROCESSES"
%mem="AMOUNT MEMORY"MB
%chk="PATH TO SAVE CHK FILE"
#p HF/6-31G* SCF=Tight Pop=MK IOp(6/50=1)

 "SOME TITLE"

"CHARGE" "MULTIPLICITY"
"ATOM"         "X"        "Y"       "Z"
"..."

"NAME OF ESP FOR ANTECHAMBER".gesp
{% endhighlight %}

Everything in " " should be replaced with something user defined (including the " ").
For GAFF the method should be Hartree-Fock with the basis set 6-31G\*.
This is used to be consistent with the rest of the force field parameters.
The setting IOp(6/50=1) specifies that the ESP should be printed in a format accepted by Antechamber.
The printed ESP is the ".gesp" file.
Before doing an ESP calculation it is advised to do a geometry optimization with HF/6-31G*.
If metal sites are present B3LYP/6-31G\* should be used instead.
For ESP calculations other useful settings are:

IOp(6/41=N), sets the number of layers for which the ESP is calculated.
Default is N = 4.
The chosen value must be 4 or above.
I.e. N ≤ 4.

IOp(6/42=N), sets the density of points per area of the ESP.
Default is N = 1.

IOp(6/43=N), sets the increment between ESP layers.
Default is $$\frac{0.4}{\sqrt{\mathrm{layer\ index}}}$$.
If N is user defined, the increments will be 0.01*N.

If more than one IOp setting is used, is specified as:

{% highlight txt %}
IOp(6/41=10,6/42=17,6/50=1)
{% endhighlight %} 
   
I.e. IOp is just specified once, with all the settings inside.
Setting IOp(6/41=10) and IOp(6/42=17) is [recommended settings](http://signe.teokem.lu.se/~ulf/Methods/resp.html).
Now that the ".gesp" file have been produced, the RESP charges can be calculated with Antechamber by the following command:

{% highlight bash %}
antechamber -i "ESP FILE".gesp -fi gesp -o "OUTPUT FILE".mol2 -fo mol2 -c resp
{% endhighlight %}

This will produce a mol2 file, where the charges can be found in last column for each atom. 


## Example - para-nitrophenolate

Here is an example with para-nitrophenolate of calculating the ESP file needed in Antechamber.

{% highlight txt %}
%NProcShared=12
%mem=20000MB
%chk=/home/erik/AmberRuns/PNP1/Resp/PNP1resp.chk
#p HF/6-31G* SCF=Tight Pop=MK IOp(6/41=10,6/42=17,6/50=1)

 PNP1 RESP

-1 1
C          0.00000        1.22448        1.40664
C          0.00000        1.21586        0.05197
C          0.00000        0.00000       -0.66739
C          0.00000       -1.21586        0.05197
C          0.00000       -1.22448        1.40664
C          0.00000        0.00000        2.19316
O          0.00000        0.00000        3.41948
N          0.00000        0.00000       -2.06029
O          0.00000       -1.05965       -2.65602
O          0.00000        1.05965       -2.65602
H          0.00000        2.15260        1.95166
H          0.00000        2.13693       -0.49934
H          0.00000       -2.13693       -0.49934
H          0.00000       -2.15260        1.95166

PNP1resp.gesp
{% endhighlight %} 

After running Gaussian, the Antechamber command looks like the following for this example:
	
{% highlight bash %}
antechamber -i PNP1resp.gesp -fi gesp -o PNP1.mol2 -fo mol2 -c resp
{% endhighlight %}