---
layout: post
title: Perfect Amalgadon, exact chances
lang: en
lang-ref: Perfect-Amalgadon-exact-chances
tag: gaming
---

In Hearthstone battlegrounds as of patch [18.6.1](https://playhearthstone.com/en-us/news/23554838) the [Amalgadon](https://hearthstone.fandom.com/wiki/Amalgadon) card have the following effect:

> **Battlecry:** For each different minion type you have among other minions, **Adapt** randomly.

When playing Amalgadon the number of adapts will be in the range between zero and fifteen. 
Zero when having no other minions with a type, and fifteen when having a golden [Brann Bronzebeard](https://hearthstone.fandom.com/wiki/Brann_Bronzebeard_(Battlegrounds)) and five other minions with different types.
A single Amalgadon can get more than fifteen adapts, f.ex. when playing [Jandice Barov](https://hearthstone.fandom.com/wiki/Jandice_Barov_(Battlegrounds)).

The two most notable and often wanted adapts are *Poison* and *Divine Shield*. 
A *perfect* Amalgadon is considered to be an Amalgadon with both *Poison* and *Divine Shield*.
To calculate the changes of getting a perfect Amalgadon, or atleast an Amalgadon with either of those two adapts, we need to consider the total amount of different adapts.
The Amalgadon can get the following adapts:

- Crackling Shield, *Divine Shield*
- Flaming Claws, *+3 Attack*
- Living Spores, *Deathrattle: Summon two 1/1 Plants.*
- Lightning Speed, *Windfury*
- Massive, *Taunt*
- Volcanic Might, *+1/+1*
- Rocky Carapace, *+3 Health*
- Poison Spit, *Poison*

This is a total of eight differnt adapts. 
Naively, the chance of getting *Divine Shield* with four adapts would then be $$1-(7/8)^5\approx 48.7\%$$.
However, there is a twist, some of the adapts can only happen once.
We can, therefore, not calculate the chances naively. 
Four of the adapts can only happen once; *Crackling Shield*, *Lightning Speed*, *Massive* and, *Poison Spit*.
To handle this problem let us set up a series of relations.
Let us now consider the chances of getting any number of the adapts that can only happen once. 
The chance of getting two of the unique adapts after $$i$$´th adapts is the chance of having two unique adapts at the $$(i-1)$$´th adapt and not getting more uniques plus the chance of having one unique adapt at the $$(i-1)$$´th adapt and getting one more unique adapt.
In mathematical terms, this can be expressed as:

$$ P(i,2) = \frac{3}{7}P(i-1,1) + \frac{4}{6}P(i-1,2) $$

here, the $$3/7$$ is three unique adapts out of a total of seven adapts left, i.e. one unique adapt have been used.
The $$4/6$$ it four non-unique adapts out of a total of six adapts, i.e. two unique adapts have been used.
Now, all the the possible equations relating to the chances of getting an amount of unique adapts can be contructed:

$$ \begin{eqnarray}
   P(0,0) &=& 1 \\
   P(i,0) &=& \frac{4}{8}P(i-1,0) \\
   P(i,1) &=& \frac{4}{8}P(i-1,0) + \frac{4}{7}P(i-1,1) \\
   P(i,2) &=& \frac{3}{7}P(i-1,1) + \frac{4}{6}P(i-1,2) \\
   P(i,3) &=& \frac{2}{6}P(i-1,2) + \frac{4}{5}P(i-1,3) \\
   P(i,4) &=& \frac{1}{5}P(i-1,3) + \frac{4}{4}P(i-1,4)
   \end{eqnarray} $$

It should be noted that negative $$i$$ is not defined would just be assigned a $$P=0$$.
Now, let us consider the chances of having *Divine Shield* after five adapts agains.
The chance will be sum of all of the above probabilites that have one or more adapts:

$$ P_\mathrm{Divine\ Shield} = w_1 P(1,5) + w_2 P(2,5) + w_3 P(3,5) + w_4 P(4,5) $$

here, the $$w$$´s are appropiate weights of the probabilities.
These weights have to be determined.
We can consider all the different way the four unique adapts can be obtained.
Since there is four different adapts, this gives a total of $$4!=24$$ different combinations.
All the combinations can be seen below:

|Divine Shield|Poison|Taunt|Windfury|
|Divine Shield|Poison|Windfury|Taunt|
|Divine Shield|Taunt|Poison|Windfury|
|Divine Shield|Taunt|Windfury|Poison|
|Divine Shield|Windfury|Poison|Taunt|
|Divine Shield|Windfury|Taunt|Poison|
|Poison|Divine Shield|Taunt|Windfury|
|Poison|Divine Shield|Windfury|Taunt|
|Poison|Taunt|Divine Shield|Windfury|
|Poison|Taunt|Windfury|Divine Shield|
|Poison|Windfury|Divine Shield|Taunt|
|Poison|Windfury|Taunt|Divine Shield|
|Taunt|Divine Shield|Poison|Windfury|
|Taunt|Divine Shield|Windfury|Poison|
|Taunt|Poison|Divine Shield|Windfury|
|Taunt|Poison|Windfury|Divine Shield|
|Taunt|Windfury|Divine Shield|Poison|
|Taunt|Windfury|Poison|Divine Shield|
|Windfury|Divine Shield|Poison|Taunt|
|Windfury|Divine Shield|Taunt|Poison|
|Windfury|Poison|Divine Shield|Taunt|
|Windfury|Poison|Taunt|Divine Shield|
|Windfury|Taunt|Divine Shield|Poison|
|Windfury|Taunt|Poison|Divine Shield|

The first weight $$w_1$$ can be determined by counting the number of rows with *Divine Shield* in the first coloumn. 
The second weight $$w_2$$ can be determined by counting the number of rows with *Divine Shield* in the first or second coloumn.
Weight three and four follows the same pattern.
The probability is therefore now:

$$ P_\mathrm{Divine\ Shield} = \frac{6}{24} P(1,5) + \frac{12}{24} P(2,5) + \frac{18}{24} P(3,5) + \frac{24}{24} P(4,5) \approx 53.0\% $$

In the same way the probility of getting either *Poison* or *Divine Shield* and, the probability of getting *Poison* and *Divine Shield* can be construced:

$$ \begin{eqnarray}
   P_\mathrm{DS}(i) &=& \frac{6}{24} P(1,i) + \frac{12}{24} P(2,i) + \frac{18}{24} P(3,i) + \frac{24}{24} P(4,i) \\
   P_\mathrm{DS\ or\ P}(i) &=& \frac{12}{24} P(1,i) + \frac{20}{24} P(2,i) + \frac{24}{24} P(3,i) + \frac{24}{24} P(4,i) \\
   P_\mathrm{DS\ and\ P}(i) &=& \frac{0}{24} P(1,i) + \frac{4}{24} P(2,i) + \frac{12}{24} P(3,i) + \frac{24}{24} P(4,i)
   \end{eqnarray} $$

here, DS is *Divine Shield* and P is *Poison*.
The "DS or P" also includes the combinates that have both *Divine Shield* and *Poison*.
For the "DS and P" case the $$w_1=0/24$$ because none of the combinations have both *Poison* and *Divine Shield* in the first coloumn.
The above equations can be evaluated for any number of adaptions.
The graph below shows the probabilities for all number of adaptions between zero and fifteen:

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/amalgadon_chances.svg"> 
</p>

The Python script for the graph can be found here: [amalgadon_chances.py]({{site.baseurl}}/assets/python_scripts/amalgadon_chances.py)

The exact chances and approximate chances can also be found in the table below.

|Adapts|$$P_\mathrm{DS\ or\ P}$$|$$\approx P_\mathrm{DS\ or\ P}$$|$$P_\mathrm{DS}$$|$$\approx P_\mathrm{DS}$$|$$P_\mathrm{DS\ and\ P}$$|$$\approx P_\mathrm{DS\ and\ P}$$|
|------|------------------------|--------------------------------|-----------------|-------------------------|-------------------------|---------------------------------|
|0|$$0$$|0.0%|$$0$$|0.0%|$$0$$|0.0%|
|1|$$\frac{1}{4}$$|25.0%|$$\frac{1}{8}$$|12.5%|$$0$$|0.0%|
|2|$$\frac{25}{56}$$|44.6%|$$\frac{27}{112}$$|24.1%|$$\frac{1}{28}$$|3.6%|
|3|$$\frac{1405}{2352}$$|59.7%|$$\frac{545}{1568}$$|34.8%|$$\frac{115}{1176}$$|9.8%|
|4|$$\frac{70225}{98784}$$|71.1%|$$\frac{146201}{329280}$$|44.4%|$$\frac{43739}{246960}$$|17.7%|
|5|$$\frac{3297157}{4148928}$$|79.5%|$$\frac{36652993}{69148800}$$|53.0%|$$\frac{13765027}{51861600}$$|26.5%|
|6|$$\frac{149089705}{174254976}$$|85.6%|$$\frac{8796724649}{14521248000}$$|60.6%|$$\frac{3876980411}{10890936000}$$|35.6%|
|7|$$\frac{6581143645}{7318708992}$$|89.9%|$$\frac{2047820152657}{3049462080000}$$|67.2%|$$\frac{1015122839923}{2287096560000}$$|44.4%|
|8|$$\frac{285914853025}{307385777664}$$|93.0%|$$\frac{466169430547001}{640387036800000}$$|72.8%|$$\frac{252512187968939}{480290277600000}$$|52.6%|
|9|$$\frac{12288758130997}{12910202661888}$$|95.2%|$$\frac{104336675177661793}{134481277728000000}$$|77.6%|$$\frac{60499089868078627}{100860958296000000}$$|60.0%|
|10|$$\frac{524329249930585}{542228511799296}$$|96.7%|$$\frac{23048628087724571849}{28241068322880000000}$$|81.6%|$$\frac{14091330806173381211}{21180801242160000000}$$|66.5%|
|11|$$\frac{22260181843140685}{22773597495570432}$$|97.7%|$$\frac{5039673033138054086257}{5930624347804800000000}$$|85.0%|$$\frac{3211817783468666090323}{4447968260853600000000}$$|72.2%|
|12|$$\frac{941816224903059025}{956491094813958144}$$|98.5%|$$\frac{1093060437686264118131801}{1245431113039008000000000}$$|87.8%|$$\frac{719848249397502598096139}{934073334779256000000000}$$|77.1%|
|13|$$\frac{39754431306085430437}{40172625982186242048}$$|99.0%|$$\frac{235555248833311662168408193}{261540533738191680000000000}$$|90.1%|$$\frac{159219439138222227446948227}{196155400303643760000000000}$$|81.2%|
|14|$$\frac{1675363228732200374665}{1687250291251822166016}$$|99.3%|$$\frac{50502543655799117848130467049}{54923512085020252800000000000}$$|92.0%|$$\frac{34851392907228941062600974011}{41192634063765189600000000000}$$|84.6%|
|15|$$\frac{70527360313103363518525}{70864512232576530972672}$$|99.5%|$$\frac{10783299572880310043888896979857}{11533937537854253088000000000000}$$|93.5%|$$\frac{7565652446099839636325899180723}{8650453153390689816000000000000}$$|87.5%|
