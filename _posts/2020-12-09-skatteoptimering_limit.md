---
layout: post
title: Øvregrænse for skatteoptimering
lang: dk
lang-ref: Øvregrænse-for-skatteoptimering
tag: dkfinance
---

For et realisationsbeskattet depot vil depot-værdien efter $$y$$ år være givet ved:

$$ D_{y}\left(k,\left\{ a_{i}\right\} \right)=k\cdot\prod_{i=1}^{y}\left(1+a_{i}\right)-s_{p,q,g,y}\left(k\cdot\prod_{i=1}^{y}\left(1+a_{i}\right)-k,\left\{ r_{i}\right\} \right) $$

$$k$$ er start kapital, $$\left\{ a_{i}\right\}$$  er et sæt af årlige afkast og $$y$$ er antal år.
Her er skatten givet ved:

$$ s_{p,q,g,y}\left(x,\left\{ r_{i}\right\} \right)=p\cdot\min\left(x,g\cdot\prod_{i=1}^{y}\left(1+r_{i}\right)\right)+q\cdot\max\left(0,x-g\cdot\prod_{i=1}^{y}\left(1+r_{i}\right)\right) $$

Med $$x$$ er kapital der skal beskattes, $$p$$ værende den lavere procentsats, $$q$$ værende det højere procentsats, $$g$$ er progressionsgrænsen og $$\left\{ r_{i}\right\}$$  er et sæt af procentielle stigninger af progressionsgrænsen.
Da depot-værdien medregnet skat kun afhænger af startværdien og slutværdien af depotet, derfor:

$$ \prod_{i=1}^{y}\left(1+x_{i}\right)=\left(1+\bar{x}\right)^{y} $$

Det fås derfor at:

$$ D_{y}\left(k,\bar{a}\right)=k\cdot\left(1+\bar{a}\right)^{y}-s_{p,q,g,y}\left(k\cdot\left(1+\bar{a}\right)^{y}-k,\bar{r}\right) $$

med:

$$ s_{p,q,g,y}\left(x,\bar{r}\right)=p\cdot\min\left(x,g\cdot\left(1+\bar{r}\right)^{y}\right)+q\cdot\max\left(0,x-g\cdot\left(1+\bar{r}\right)^{y}\right) $$

Givet et depot der giver et afkast, kan afkastet realiseres eller forblive urealiseret, dette giver to situationer for afkastet fra depotet.
Hvis depotet realiseres vil delen fra afkastet udvikle sig følgende:

$$ \begin{eqnarray}
   D_{\mathrm{realiseret}} &=& \left.D_{y}\left(m\cdot k,\bar{a}\right)\right|_{g=g_{\mathrm{effektiv}}} \\
	                       &=& m\cdot k\cdot\left(1+\bar{a}\right)^{y}-s_{p,q,g_{\mathrm{effektiv}},y}\left(m\cdot k\cdot\left(1+\bar{a}\right)^{y}-m\cdot k,\bar{r}\right)
    \end{eqnarray} $$

Her er $$m$$ en minus skatteprocenten betalt vel realisering og $$g_{\mathrm{effektiv}}$$ er progressionsgrænsen modregnet den del af progressionsgrænsen der bliver opbrugt af det underligende depot.
Den anden situation er at afkastet forbliver urealiseret, dette depot vil udvikle sig følgende:

$$ \begin{eqnarray}
   D_{\mathrm{urealiseret}} &=& D_{y}\left(k,\bar{a}\right)+s_{p,q,g,y}\left(k\cdot\left(1+\bar{a}\right)^{y}-k,\bar{r}\right)-s_{p,q,g_{\mathrm{effektiv}},y}\left(k\cdot\left(1+\bar{a}\right)^{y},\bar{r}\right) \\
	                       &=& k\cdot\left(1+\bar{a}\right)^{y}-s_{p,q,g_{\mathrm{effektiv}},y}\left(k\cdot\left(1+\bar{a}\right)^{y},\bar{r}\right)
    \end{eqnarray} $$

Bemærk her at der vil blive betalt skat af hele depotet, da “start kapitalen” er urealiseret.
I situationen hvor det underliggende depot bruger hele progressionsgrænsen vil skatten være givet ved:

$$ \left.s_{p,q,0,y}\left(x,\bar{r}\right)\right|_{x>0}=q\cdot x $$

Antal år der skal gå før realisering for at denne skatteoptimering ikke kan betale sig, kan findes ved at sætte:

$$ \begin{eqnarray}
   \left.D_{\mathrm{urealiseret}}\right|_{g_{\mathrm{effektiv}}=0} &=& 	\left.D_{\mathrm{realiseret}}\right|_{g_{\mathrm{effektiv}}=0} \\
   k\cdot\left(1+\bar{a}\right)^{y}-q\cdot k\cdot\left(1+\bar{a}\right)^{y} &=& m\cdot k\cdot\left(1+\bar{a}\right)^{y}-q\cdot\left(m\cdot k\cdot\left(1+\bar{a}\right)^{y}-m\cdot k\right) \\
   \left(1+\bar{a}\right)^{y}\cdot\left(k-q\cdot k\right) &=& \left(1+\bar{a}\right)^{y}\cdot\left(m\cdot k-q\cdot m\cdot k\right)+q\cdot m\cdot k \\
   \left(1+\bar{a}\right)^{y}\cdot\left(k-q\cdot k-m\cdot k+q\cdot m\cdot k\right) &=& q\cdot m\cdot k \\
   \left(1+\bar{a}\right)^{y} &=& \frac{q\cdot m\cdot k}{k-q\cdot k-m\cdot k+q\cdot m\cdot k} \\
   y\cdot\log\left(1+\bar{a}\right) &=& \log\left(\frac{q\cdot m\cdot k}{k-q\cdot k-m\cdot k+q\cdot m\cdot k}\right) \\
   y &=& \frac{\log\left(\frac{q\cdot m\cdot k}{k-q\cdot k-m\cdot k+q\cdot m\cdot k}\right)}{\log\left(1+\bar{a}\right)} \\
   y &=& \frac{\log\left(\frac{q\cdot m}{1-q-m+q\cdot m}\right)}{\log\left(1+\bar{a}\right)} \label{eq1}\tag{1}
   \end{eqnarray} $$

Den ovenstående ligning er en øvre grænse for hvornår skatteoptimering kan betale sig.
Her det kan bemærkes at samme ligning fås med $$g_{\mathrm{effektiv}}=\infty$$, altså hvis progressionsgrænsen ikke nås.
For denne progressionsgrænse vil $$q\rightarrow p$$, og $$m=1-p$$ og derved fås:

$$ \begin{eqnarray}
   y &=& \frac{\log\left(\frac{p\cdot\left(1-p\right)}{1-p-\left(1-p\right)+p\cdot\left(1-p\right)}\right)}{\log\left(1+\bar{a}\right)} \\
    &=& \frac{\log\left(\frac{p\cdot\left(1-p\right)}{1-p+1+p+p\cdot\left(1-p\right)}\right)}{\log\left(1+\bar{a}\right)} \\
    &=& \frac{\log\left(\frac{p\cdot\left(1-p\right)}{p\cdot\left(1-p\right)}\right)}{\log\left(1+\bar{a}\right)} \\
    &=& \frac{\log\left(1\right)}{\log\left(1+\bar{a}\right)} \\
    &=& 0
   \end{eqnarray} $$

Den nedre grænse er derfor 0 år, og derfor ikke særlig brugbar.
Den øvre grænse fra ligning (\ref{eq1}) kan nu plottes.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/oevregraense_skatteoptimering.svg">
</p>

Ofte vil det ikke kunne betale sig at lave skatteoptimering hvis der er mere end 10 år til man skal bruge pengene.

<!-- python_split -->

## Python detaljer

Starter med at importere alle de moduler der skal bruges:

{% highlight python %}
import matplotlib.pyplot as plt
import numpy as np
{% endhighlight %}

Definerer funktion for ligning (\ref{eq1}).

{% highlight python %}
def y(q: float, m: float, a_bar: float) -> float:
    """Udregn øvregrænse for hvornår skatteoptimering kan betale sig.

    Args:
       q: Øvre skattesats for aktiebeskatning.
       m: Skattesats for realiseret situation.
       a_bar: Middel årligt afkast.

    Returns:
      Antal år hvor efter skatteoptimering ikke kan betale sig.
    """
    return np.log(q * m / (1 - q - m + q * m)) / np.log(1 + a_bar)
{% endhighlight %}

Sætter graf op.

{% highlight python %}
x = np.linspace(0.04, 0.14, 1000)
f = np.zeros(np.shape(x))

for i, xi in enumerate(x):
    f[i] = y(0.42, 0.73, xi)

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(x, f, linewidth=3)
ax1.set_ylim(0, 20)
ax1.set_xlim(0.035, 0.145)
ax1.set_ylabel("År")
ax1.set_xlabel(r"$\bar{a}$")
ax1.grid(which="minor")
ax1.grid(which="major")
plt.tight_layout()
plt.savefig("oevregraense_skatteoptimering.svg")
{% endhighlight %}

Den fulde kode kan findes her: [skatteoptimering_limit.py]({{ site.baseurl }}/assets/python_scripts/skatteoptimering_limit.py)
