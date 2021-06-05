---
layout: post
title: Estimat af CAGR efter skat og ÅOP
lang: dk
lang-ref: Estimat-af-CAGR-efter-skat-og-ÅOP
tag: dkfinance
---

Givet at man har en idé om hvor meget ens strategi i gennemsnit giver per år, 
kan det være brugbart at estimere hvor meget dette vil svare til efter skat og ÅOP.
Dette estimat er forskelligt for lagerbeskatning og realisationsbeskatning.

## Realisationsbeskatning udledning

Kapital for et realisationsbeskattet depot er givet ved:

$$ k'_{\mathrm{slut}}=k_{\mathrm{start}}\cdot\prod_{i=1}^{y}\left(1+a_{i}\right)-s\left(k_{\mathrm{start}}\cdot\left(\prod_{i=1}^{y}\left(1+a_{i}\right)-1\right)\right) $$

Her er $$a_{i}$$ procentielle afkast for det $$i$$'te år,
og $$y$$ er antal år og $$s\left(x\right)$$ er en funktion der beregner skatten for $$x$$ afkast.
Det kan ses at:

$$ k'_{\mathrm{start}}\cdot\left(\prod_{i=1}^{y}\left(1+a_{i}\right)-1\right)=k_{\mathrm{start}}\cdot\prod_{i=1}^{y}\left(1+a_{i}\right)-k_{\mathrm{start}} $$

Det er altså kapital der overstiger start kapitalen.
En simplificering kan nu laves med følgende definition:

$$ \begin{eqnarray}
   \bar{a}&=&\left(\prod_{i=1}^{y}\left(1+a_{i}\right)\right)^{1/y}-1 \\
   \left(1+\bar{a}\right)^{y}&=&\prod_{i=1}^{y}\left(1+a_{i}\right)
   \end{eqnarray} $$

Det kan ses at dette er definitionen af CAGR.
Slut kapitalen kan nu skrives som:

$$ k'_{\mathrm{slut}}=k_{\mathrm{start}}\cdot\left(1+\bar{a}\right)^{y}-s\left(k_{\mathrm{start}}\cdot\left(\left(1+\bar{a}\right)^{y}-1\right)\right) $$

Modregning af ÅOP kan gøres ved at trække ÅOP fra CAGR:

$$ k_{\mathrm{slut}}=k_{\mathrm{start}}\cdot\left(1+\bar{a}-\mathrm{åop}\right)^{y}-s\left(k_{\mathrm{start}}\cdot\left(\left(1+\bar{a}-\mathrm{åop}\right)^{y}-1\right)\right) $$

I stedet for at have skatten som en funktion af overskud, kan skatten også beregnes som en effektiv skatteprocent ganget med overskuddet.
Den effektive skatteprocent kan beregnes som:

$$ q_{\mathrm{effektiv}}=\frac{s\left(x\right)}{x} $$

Derfor:

$$ q_{\mathrm{effektiv}}\cdot k_{\mathrm{start}}\cdot\left(\left(1+\bar{a}-\mathrm{åop}\right)^{y}-1\right)=s\left(k_{\mathrm{start}}\cdot\left(\left(1+\bar{a}-\mathrm{åop}\right)^{y}-1\right)\right) $$

Herved:

$$ k_{\mathrm{slut}}=k_{\mathrm{start}}\cdot\left(1+\bar{a}-\mathrm{åop}\right)^{y}-q_{\mathrm{effektiv}}\cdot k_{\mathrm{start}}\cdot\left(\left(1+\bar{a}-\mathrm{åop}\right)^{y}-1\right) $$

Det kan nu huskes at CAGR også kan defineres som:

$$ \mathrm{CAGR}=\left(\frac{k_{\mathrm{slut}}}{k_{\mathrm{start}}}\right)^{1/y}-1 $$

Ligningen for slut kapitalen kan derfor omskrives til denne form:

$$ \begin{eqnarray}
   \frac{k_{\mathrm{slut}}}{k_{\mathrm{start}}}&=&\left(1+\bar{a}-\mathrm{åop}\right)^{y}-q_{\mathrm{effektiv}}\cdot\left(\left(1+\bar{a}-\mathrm{åop}\right)^{y}-1\right) \\
   \left(\frac{k_{\mathrm{slut}}}{k_{\mathrm{start}}}\right)^{1/y}&=&\left(\left(1+\bar{a}-\mathrm{åop}\right)^{y}-q_{\mathrm{effektiv}}\cdot\left(\left(1+\bar{a}-\mathrm{åop}\right)^{y}-1\right)\right)^{1/y} \\
   \mathrm{CAGR_{effektiv}}&=&\left(\left(1+\bar{a}-\mathrm{åop}\right)^{y}-q_{\mathrm{effektiv}}\cdot\left(\left(1+\bar{a}-\mathrm{åop}\right)^{y}-1\right)\right)^{1/y}-1
   \end{eqnarray} $$

Slut udtrykket er nu:

$$ \mathrm{CAGR_{effektiv}}=\left(\left(1-q_{\mathrm{effektiv}}\right)\cdot\left(1+\bar{a}-\mathrm{åop}\right)^{y}+q_{\mathrm{effektiv}}\right)^{1/y}-1
\label{eq3}\tag{1} $$

## Lagerbeskatning udledning

Kapital for et lagerbeskattet depot efter et år er givet ved:

$$ k'_{1}=k_{0}\cdot\left(1+a_{1}\right)-s\left(k_{0}\cdot a_{1}\right) $$

Igen ved at bruge den effektive skatteprocent:

$$ \begin{eqnarray}
   k'_{1}&=&k_{0}\cdot\left(1+a_{1}\right)-q_{\mathrm{effektiv},1}\cdot k_{0}\cdot a_{1} \\
   &=&k_{0}\cdot\left(1+a_{1}-q_{\mathrm{effektiv},1}\cdot a_{1}\right)
   \end{eqnarray} $$

Kapital efter to år er givet ved:

$$ k'_{2}=k'_{1}\cdot\left(1+a_{2}-q_{\mathrm{effektiv},2}\cdot a_{2}\right) $$

Ved at indsætte ligningen for kapital efter et år findes:

$$ k'_{2}=k_{0}\cdot\left(1+a_{1}-q_{\mathrm{effektiv},1}\cdot a_{1}\right)\cdot\left(1+a_{2}-q_{\mathrm{effektiv},2}\cdot a_{2}\right) $$

Det kan derfor ses at det generelle udtryk er:

$$ \begin{eqnarray}
   k'_{\mathrm{slut}}&=&k_{\mathrm{start}}\cdot\prod_{i=1}^{y}\left(1+a_{i}-q_{\mathrm{effektiv},i}\cdot a_{i}\right) \\
   &=&k_{\mathrm{start}}\cdot\prod_{i=1}^{y}\left(1+a_{i}\cdot\left(1-q_{\mathrm{effektiv},i}\right)\right)
   \end{eqnarray} $$

Igen kan ÅOP trækkes fra det procentielle afkast:

$$ k_{\mathrm{slut}}=k_{\mathrm{start}}\cdot\prod_{i=1}^{y}\left(1+\left(a_{i}-\mathrm{åop}\right)\cdot\left(1-q_{\mathrm{effektiv},i}\right)\right) $$

Nu kan den effektive CAGR findes:

$$ \begin{eqnarray}
   \frac{k_{\mathrm{slut}}}{k_{\mathrm{start}}}&=&\prod_{i=1}^{y}\left(1+\left(a_{i}-\mathrm{åop}\right)\cdot\left(1-q_{\mathrm{effektiv},i}\right)\right) \\
   \left(\frac{k_{\mathrm{slut}}}{k_{\mathrm{start}}}\right)^{1/y}&=&\left(\prod_{i=1}^{y}\left(1+\left(a_{i}-\mathrm{åop}\right)\cdot\left(1-q_{\mathrm{effektiv},i}\right)\right)\right)^{1/y} \\
   \mathrm{CAGR_{effektiv}}&=&\left(\prod_{i=1}^{y}\left(1+\left(a_{i}-\mathrm{åop}\right)\cdot\left(1-q_{\mathrm{effektiv},i}\right)\right)\right)^{1/y}-1
   \end{eqnarray} $$

For at få en brugbar formel bliver vi nød til at lave en approksimation nu.
Det kan approksimere at:

$$ \prod_{i=1}^{y}\left(1+\left(a_{i}-\mathrm{åop}\right)\cdot\left(1-q_{\mathrm{effektiv},i}\right)\right)\approx\left(1+\left(\bar{a}-\mathrm{åop}\right)\cdot\left(1-\bar{q}_{\mathrm{effektiv}}\right)\right)^{y} $$

Dette er en approksimation of kun eksakt hvis alle $$a_{i}$$ er samme værdi og alle $$q_{\mathrm{effektiv},i}$$ er samme værdi.
Herved:

$$ \widetilde{\mathrm{CAGR}}_{\mathrm{effektiv}}=\left(\left(1+\left(\bar{a}-\mathrm{åop}\right)\cdot\left(1-\bar{q}_{\mathrm{effektiv}}\right)\right)^{y}\right)^{1/y}-1 $$

Tilden indikere at det er en approksimativ ligning.
Ligningen bliver derfor til sidst:

$$ \widetilde{\mathrm{CAGR}}_{\mathrm{effektiv}}=\left(\bar{a}-\mathrm{åop}\right)\cdot\left(1-\bar{q}_{\mathrm{effektiv}}\right) \label{eq2}\tag{2} $$

## Diskussion af ligninger

I ligningerne (\ref{eq3}) og (\ref{eq2}) er $$\bar{a}$$ forventet gennemsnitligt årligt afkast før skat og ÅOP,
og $$q_{\mathrm{effektiv}}$$ er den effektiv skatteprocent, vil være mellem 27% og 42% for et normalt aktiedepot.

Det kan ses at ligningen for den effektive CAGR efter skat for et realisationsbeskattet depot er afhængig af antal år.
Lad os se hvordan den effektive CAGR afhænger af antal år for et givent afkast før skat over skatteprocenter mellem 0% og 100%.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/cagr7.svg"> 
</p>

Ovenstående graf viser ligningerne (\ref{eq3}) og (\ref{eq2}).
De stiplede linjer er 27% skat og 42% skat.
Det kan ses at den effektive CAGR for lagerbeskatning altid er mindre end den for realisationsbeskatning, hvilket er som forventet.
For et realisationsbeskattet depot vil den effektive CAGR gå mod CAGR før skat jo flere år der passere.
Dette er grundet *renters-rente* effekten man får ved realisationsbeskatning.

Et lignende plot kan laves, men nu med CAGR før skat på 15%.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/cagr15.svg"> 
</p>

Det kan bemærkes her at tendensen er den samme som for CAGR før skat på 7%,
men at den effektive CAGR hurtigere går mod CAGR før skat når antal år forøges.

For et lagerbeskattet depot vil den effektive CAGR være skatteprocenten mindre end CAGR før skat.
Hvor for et realisationsbeskattet depot vil den effektive CAGR afhænge af antal år der går,
og over tid komme tættere på CAGR før skat. 
Dette er accelereret af størrelse af CAGR før skat.

<!-- python_split -->

## Python detaljer

Starter med at importere alle de moduler der skal bruges til modellen.

{% highlight python %}
import matplotlib.pyplot as plt
import numpy as np
{% endhighlight %}

Definere en funktion for ligning (\ref{eq3}):

{% highlight python %}
def effektiv_cagr_realisation(cagr: float, skatteprocent: float, åop: float, år: int) -> float:
    """Udregn CAGR efter skat og ÅOP for et realisationsbeskattet depot.

    Args:
      cagr: CAGR før skat og ÅOP.
      skatteprocent: Skatteprocent.
      åop: ÅOP.
      år: Antal år.

    Returns:
      Effektiv CAGR efter skat og ÅOP.
    """
    return ((1 - skatteprocent) * (1 + cagr - åop) ** år + skatteprocent) ** (1 / år) - 1
{% endhighlight %}

Definere en funktion for ligning (\ref{eq2}):

{% highlight python %}
def effektiv_cagr_lager(cagr: float, skatteprocent: float, åop: float) -> float:
    """Udregn CAGR efter skat og ÅOP for et lagerbeskattet depot.

    Args:
      cagr: CAGR før skat og ÅOP.
      skatteprocent: Skatteprocent.
      åop: ÅOP.
      år: Antal år.

    Returns:
      Effektiv CAGR efter skat og ÅOP.
    """
    return (cagr - åop) * (1 - skatteprocent)
{% endhighlight %}

Laver graf for CAGR på 7% før skat og ÅOP for forskellige antal år:

{% highlight python %}
plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

q = np.linspace(0, 1, 1000)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 6))
ax1.plot([0.27, 0.27], [0.0, 0.07], "k--")
ax1.plot([0.42, 0.42], [0.0, 0.07], "k--")
for antal_år in range(10, 60, 10):
    real = effektiv_cagr_realisation(7 / 100, q, 0.12 / 100, antal_år)
    ax1.plot(q, real, label=f"real, {antal_år} år", linewidth=3)
lager = effektiv_cagr_lager(7 / 100, q, 0.12 / 100)
ax1.plot(q, lager, label="lager", linewidth=3)
ax1.set_xlabel(r"$q_\mathrm{effektiv}$")
ax1.set_ylabel(r"$\mathrm{CAGR}_\mathrm{effektiv}$")
ax1.set_title("CAGR 7%")
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.legend()
plt.tight_layout()
plt.savefig("cagr7.svg")
{% endhighlight %}

Laver graf for CAGR på 15% før skat og ÅOP for forskellige antal år:

{% highlight python %}
fig, ax1 = plt.subplots(1, 1, figsize=(6, 6))
ax1.plot([0.27, 0.27], [0.0, 0.15], "k--")
ax1.plot([0.42, 0.42], [0.0, 0.15], "k--")
for antal_år in range(10, 60, 10):
    real = effektiv_cagr_realisation(15 / 100, q, 0.12 / 100, antal_år)
    ax1.plot(q, real, label=f"real, {antal_år} år", linewidth=3)
lager = effektiv_cagr_lager(15 / 100, q, 0.12 / 100)
ax1.plot(q, lager, label="lager", linewidth=3)
ax1.set_xlabel(r"$q_\mathrm{effektiv}$")
ax1.set_ylabel(r"$\mathrm{CAGR}_\mathrm{effektiv}$")
ax1.set_title("CAGR 15%")
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.legend()
plt.tight_layout()
plt.savefig("cagr15.svg")
{% endhighlight %}

Den fulde kode kan findes her: [estimat_effektiv_cagr.py]({{ site.baseurl }}/assets/python_scripts/estimat_effektiv_cagr.py)

