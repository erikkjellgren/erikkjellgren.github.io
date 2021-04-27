---
layout: post
title: Danske investeringsforeninger, signifikans af udbytte
---

*Brug ikke dette som finansiel rådgivning. Dette er kun en model.*

Her vil det undersøges hvor står betydning udbytte procenten har for Danske investeringsforeninger der ellers realisationsbeskattes.

Først skal den indre værdi af ETFen kontureres.
Her bliver der taget udgangspunk i data for S&P500 (fordi denne data er nemt tilgængelig), dataene er hentet fra, [www.econ.yale.edu](http://www.econ.yale.edu/~shiller/data/ie_data.xls), 16-11-2020.
Den procentvise stigning af ETFens kurs er nu den procentvise stigning af S&P500 plus det procentvise udbytte.
Se [SP500.csv]({{ site.baseurl }}/assets/python_scripts/data/SP500.csv) for den behandlede data.

Starter med at importere alle de moduler der skal bruges til modellen.
dkfinance_modeller er fra, [dkfinance_modeller](https://github.com/erikkjellgren/dkfinance_modeller)

{% highlight python %}
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

import dkfinance_modeller.aktieskat.depotmodel as depotmodel
import dkfinance_modeller.aktieskat.kurtage as kurtage
import dkfinance_modeller.aktieskat.skat as skat
import dkfinance_modeller.aktieskat.vaerdipapirer as værdipapirer
import dkfinance_modeller.utility.formler as formler
{% endhighlight %}

Nu defineres depotet i modellen.

{% highlight python %}
def depoter() -> depotmodel.DepotModel:
    """Definere depoter.

    Returns:
      Depot med realationsbeskatning
    """
    etf = værdipapirer.ETF(kurs=100, åop=0.55 / 100, beskatningstype="realisation")
    skatter = skat.Skat(beskatningstype="aktie")
    realisationsbeskatning = depotmodel.DepotModel(
        kapital=300000.0,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="Dkk"),
        skatteklasse=skatter,
        minimumskøb=5000,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    return realisationsbeskatning
{% endhighlight %}

Her er ÅOP valgt til at være 0.55% for at være en normal værdi for en Dansk investeringsforening.
Depotet defineres inde i en funktion for at den senere er nemmere at nulstille.

Nu kan propagationen for modellen bygges.

{% highlight python %}
data = np.genfromtxt("data/SP500.csv", delimiter=";")
real: List[List[float]] = [[], [], [], [], [], [], [], [], [], [], []]
for j, udbytte_procent in enumerate(np.linspace(0, 1, 11)):
    for start in range(0, 50 * 12):
        realisationsdepot = depoter()
        udbytte_årlig = 0.0
        kursstigning_årlig = 0.0
        for i in range(start + 950, start + 950 + 12 * 20):
            udbytteafkast = realisationsdepot.ETFer[0].kurs * data[i + 1, 4]
            kursafkast = realisationsdepot.ETFer[0].kurs * data[i + 1, 3]
            if i % 12 == 0:
                effektivt_udbytte = udbytte_årlig + max(0, udbytte_procent * kursstigning_årlig)
                realisationsdepot.afkast_månedlig(
                    [udbytteafkast + kursafkast - effektivt_udbytte], [effektivt_udbytte]
                )
                udbytte_årlig = 0.0
                kursstigning_årlig = 0.0
            else:
                realisationsdepot.afkast_månedlig([udbytteafkast + kursafkast], [0.0])
            udbytte_årlig += udbytteafkast
            kursstigning_årlig += kursafkast
        real[j].append(realisationsdepot.total_salgsværdi())
real = np.array(real)
carg = formler.CAGR(300000, real, 20)  # type: ignore
{% endhighlight %}
   
Den statistiske samling af slut depotbeholdninger samles ved at startet 600 forskellige måneder, startende fra 1949 December,
og propagere 20 år frem for hver start måned.
Dette gøres for kursstigning til udbytteprocent mellem 0% og 100%.
Det effektive udbytte for bliver opgjort på årlig basis efter følgende model:

$$ u_\mathrm{effektive} = u + \max\left(0, pk\right) $$

Med $$u$$ værende udbytte, $$k$$ værende kursstigning og 
$$p$$ værende den kursstigning til udbytteprocent.
Efter at have propageret 20 år frem gemmes den total depotværdi efter skat.

Efter at koden er kørt kan dataene analyseres.
Først sættes nogle graf parametre.

{% highlight python %}
plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)
{% endhighlight %}

For de forskellige udbytte procenter kan fordelingen af slut værdien af depotet plottes.

{% highlight python %}
fig, ax1 = plt.subplots(1, 1, figsize=(6, 6))
for k, percent in enumerate(np.linspace(0, 1, 11)):
    density = scipy.stats.gaussian_kde(carg[k, :])  # type: ignore # pylint: disable=E1126
    density.covariance_factor = lambda: 0.15
    density._compute_covariance()  # pylint: disable=W0212
    ax1.plot(
        np.linspace(0.0, 0.16, 200),
        density(np.linspace(0.0, 0.16, 200)),
        linewidth=4,
        alpha=1 - k * 0.075,
        label=f"Udbytte = {percent*100:1.0f}%",
    )
ax1.set_ylim(0, 26)
ax1.set_xlim(0.0, 0.16)
ax1.set_ylabel("Arbitrær værdi")
ax1.set_xlabel("CAGR")
plt.legend()
plt.tight_layout()
plt.savefig("distributioner.svg")
{% endhighlight %}

Dette giver følgende plot.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/distributioner.svg"> 
</p>

Man kan se at jo højere udbytte procenten er jo lavere vil afkastet være over en 20 årig periode.
Det skal specielt bemærkes at ved de lave udbytte procenter findes der situationer hvor man kan have haft et meget stort afkast
(hvis man er heldig).
0.03 CAGR ift. 0.14 CAGR.
Dette giver et hint af at realisationsbeskatning vil have en fordel i perioder med stærk vækst,
ift. udbytte beskattet afkast.

For de forskellige udbytte procenter kan fraktilerne af slut værdien af depotet plottes.

{% highlight python %}
q: List[List[float]] = [[], [], [], [], [], [], [], [], [], [], []]
for i in range(0, 21):
    for k in range(0, 11):
        q[k].append(np.quantile(carg[k, :], i * 0.05))  # type: ignore

fig, ax1 = plt.subplots(1, 1, figsize=(6, 6))
for k, percent in enumerate(np.linspace(0, 1, 11)):
    ax1.plot(np.linspace(0.0, 1, 21), q[k], label=f"Udbytte = {percent*100:1.0f}%", linewidth=3)
plt.legend()
ax1.set_xticks(np.linspace(0.0, 1.0, 11))
ax1.set_ylim(0.02, 0.14)
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("CAGR")
ax1.set_xlabel("Fraktil")
plt.tight_layout()
plt.savefig("fraktiler.svg")
{% endhighlight %}

Dette giver følgende plot.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/fraktiler.svg"> 
</p>

Det kan bemærkes at op til 0.5 fraktilen er alle udbytteprocenter mellem 0% til 30% næsten identiske.
Det er primært ved de "heldige" start tidspunkter at en udbytte procent lavere end 30% vil give en forskel.
Ved udbytte procenter over 30% falder afkastet relativt hurtigt.
Givet at udbytteprocenter mellem 0% og 30% giver forholdsvis ens afkast i halvdelen af tilfældene, 
vil en udbytteprocent på 30% i fremtidige analyse af Danske investeringsforeninger være et brugbart estimat.
30% udbytte er også fundet til at være gennemsnittet af Danske investeringsforening, se [reddit-post](https://www.reddit.com/r/dkfinance/comments/hv82ll/en_gang_for_alle_om_etfer_vs_danske/).

Den fulde kode kan findes her: [investeringsforening_udbytte.py]({{ site.baseurl }}/assets/python_scripts/investeringsforening_udbytte.py)
