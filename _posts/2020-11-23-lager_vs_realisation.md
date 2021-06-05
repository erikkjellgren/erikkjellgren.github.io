---
layout: post
title: Danske investeringsforeninger vs. ETFer beskatning
lang: dk
lang-ref: Danske-investeringsforeninger-vs.-ETFer-beskatning
tag: dkfinance
---

Nogen Danske investeringsforeninger er realisationsbeskattet givet at de udfylde kriterier
vedrørende udbetaling af udbytte.
Modellen for udbytte fra investeringsforeningerne kan ses i [Danske investeringsforeninger, signifikans af udbytte]({% post_url 2020-11-16-investeringsforening_udbytte %}).
Denne sammenligning realisationsbeskattede investeringsforeninger ifht. ETFer bruger priser fra Saxo.
Investeringsforening er antaget en ÅOP på 0.55%.
ETFen er der antaget en ÅOP på 0.12% og brug af underkonto i Euro.

Den underliggende historiske data følger S&P500, dataene er hentet fra, [www.econ.yale.edu](http://www.econ.yale.edu/~shiller/data/ie_data.xls), 16-11-2020.
Se [SP500.csv]({{ site.baseurl }}/assets/python_scripts/data/SP500.csv) for den behandlede data.

Modellen kan nu opbygges.
Starter med at importere alle de moduler der skal bruges til modellen.
dkfinance_modeller er fra, [dkfinance_modeller](https://github.com/erikkjellgren/dkfinance_modeller)

{% highlight python %}
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

import dkfinance_modeller.aktieskat.depotmodel as depotmodel
import dkfinance_modeller.aktieskat.kurtage as kurtage
import dkfinance_modeller.aktieskat.skat as skat
import dkfinance_modeller.aktieskat.vaerdipapirer as værdipapirer
import dkfinance_modeller.aktieskat.valuta as valuta
import dkfinance_modeller.utility.formler as formler
{% endhighlight %}

Nu defineres depotet i modellen.

{% highlight python %}
def depoter() -> Tuple[depotmodel.DepotModel, depotmodel.DepotModel]:
    """Definere depoter.

    Returns:
      Depot med realationsbeskatning
    """
    etf1 = værdipapirer.ETF(kurs=100, åop=0.12 / 100, beskatningstype="lager")
    etf2 = værdipapirer.ETF(kurs=100, åop=0.55 / 100, beskatningstype="realisation")
    skatter = skat.Skat(beskatningstype="aktie")
    lagerbeskatning = depotmodel.DepotModel(
        kapital=300000.0,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44, underkonto=True),
        skatteklasse=skatter,
        minimumskøb=5000,
        ETFer=[etf1],
        ETF_fordeling=[1.0],
        valutafunktion=valuta.saxo_underkonto_kurtage,
    )
    realisationsbeskatning = depotmodel.DepotModel(
        kapital=300000.0,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="Dkk"),
        skatteklasse=skatter,
        minimumskøb=5000,
        ETFer=[etf2],
        ETF_fordeling=[1.0],
    )
    return lagerbeskatning, realisationsbeskatning
{% endhighlight %}

Depoterne defineres inde i en funktion for at de senere er nemmere at nulstille.

Nu kan propagationen for modellen bygges.

{% highlight python %}
data = np.genfromtxt("data/SP500.csv", delimiter=";")
real: List[List[float]] = [[], [], [], []]
lager: List[List[float]] = [[], [], [], []]
for j, antal_år in enumerate([1, 5, 10, 20]):
    for start in range(0, len(data) - 950 - antal_år * 12):
        lagerdepot, realisationsdepot = depoter()
        udbytte_årlig = 0.0
        kursstigning_årlig = 0.0
        for i in range(start + 950, start + 950 + 12 * antal_år):
            udbytteafkast_real = realisationsdepot.ETFer[0].kurs * data[i + 1, 4]
            kursafkast_real = realisationsdepot.ETFer[0].kurs * data[i + 1, 3]
            udbytteafkast_lager = lagerdepot.ETFer[0].kurs * data[i + 1, 4]
            kursafkast_lager = lagerdepot.ETFer[0].kurs * data[i + 1, 3]
            if i % 12 == 0:
                effektivt_udbytte = udbytte_årlig + max(0, 0.3 * kursstigning_årlig)
                realisationsdepot.afkast_månedlig(
                    [udbytteafkast_real + kursafkast_real - effektivt_udbytte], [effektivt_udbytte]
                )
                udbytte_årlig = 0.0
                kursstigning_årlig = 0.0
            else:
                realisationsdepot.afkast_månedlig([udbytteafkast_real + kursafkast_real], [0.0])
            lagerdepot.afkast_månedlig([udbytteafkast_lager + kursafkast_lager], [0.0])
            udbytte_årlig += udbytteafkast_real
            kursstigning_årlig += kursafkast_real
        real[j].append(realisationsdepot.total_salgsværdi())
        lager[j].append(lagerdepot.total_salgsværdi())
real_1år = np.array(real[0])
real_5år = np.array(real[1])
real_10år = np.array(real[2])
real_20år = np.array(real[3])
lager_1år = np.array(lager[0])
lager_5år = np.array(lager[1])
lager_10år = np.array(lager[2])
lager_20år = np.array(lager[3])
real_carg_1år = formler.CAGR(300000, real_1år, 1)
real_carg_5år = formler.CAGR(300000, real_5år, 5)
real_carg_10år = formler.CAGR(300000, real_10år, 10)
real_carg_20år = formler.CAGR(300000, real_20år, 20)
lager_carg_1år = formler.CAGR(300000, lager_1år, 1)
lager_carg_5år = formler.CAGR(300000, lager_5år, 5)
lager_carg_10år = formler.CAGR(300000, lager_10år, 10)
lager_carg_20år = formler.CAGR(300000, lager_20år, 20)

{% endhighlight %}

Den statistiske samling af slut depotbeholdninger samles ved at starte X forskellige måneder, startende fra 1949 December,
og propagere 1, 5, 10 eller 20 år frem for hver start måned.

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
   
For de forskellige depoter og antal investerings år kan 
fraktilerne af slut værdien af depotet plottes.

{% highlight python %}
q_real: List[List[float]] = [[], [], [], []]
q_lager: List[List[float]] = [[], [], [], []]
for i in range(0, 101):
    q_real[0].append(np.quantile(real_carg_1år, i * 0.01))  # type: ignore
    q_real[1].append(np.quantile(real_carg_5år, i * 0.01))  # type: ignore
    q_real[2].append(np.quantile(real_carg_10år, i * 0.01))  # type: ignore
    q_real[3].append(np.quantile(real_carg_20år, i * 0.01))  # type: ignore
    q_lager[0].append(np.quantile(lager_carg_1år, i * 0.01))  # type: ignore
    q_lager[1].append(np.quantile(lager_carg_5år, i * 0.01))  # type: ignore
    q_lager[2].append(np.quantile(lager_carg_10år, i * 0.01))  # type: ignore
    q_lager[3].append(np.quantile(lager_carg_20år, i * 0.01))  # type: ignore

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(6, 10), sharex=True)
for i, ax in enumerate([ax1, ax2, ax3, ax4]):
    ax.plot(np.linspace(0.0, 1, 101), q_real[i], label="Realisationsbeskatning", linewidth=3)
    ax.plot(np.linspace(0.0, 1, 101), q_lager[i], label="Lagerbeskatning", linewidth=3)
ax1.legend()
for ax, år in zip([ax1, ax2, ax3, ax4], [1, 5, 10, 20]):
    ax.set_xticks(np.linspace(0.0, 1.0, 11))
    ax.grid(which="minor")
    ax.grid(which="major")
    ax.set_ylabel("CAGR")
    ax.set_title(f"{år:1.0f} år investering")
ax1.set_ylim(-0.45, 0.45)
ax2.set_ylim(-0.1, 0.22)
ax3.set_ylim(-0.06, 0.15)
ax4.set_ylim(0.01, 0.14)
ax4.set_xlabel("Fraktil")
plt.tight_layout()
plt.savefig("fraktiler_lager_vs_real.svg")
{% endhighlight %}

Dette giver følgende plot.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/fraktiler_lager_vs_real.svg"> 
</p>

I figuren kan den totale værdi af depotet opgjort som CAGR efter skat ses.
For en investeringsperiode på under 5 år kan det ses at der stort set ingen forskel er 
mellem at vælge en Dansk investeringsforening eller en ETF.
For 1 år perioden kan det bemærkes at der er 30% risiko for at man har et tab!
For investerings perioder længere end 10 år vil realisationsbeskatning give
en gevinst ifht. billigere (læs: lavere ÅOP) ETFer i ca. halvdelen af tilfældene.

Forskellen mellem CAGR fra realisationsbeskatning og lagerbeskatning kan også sammenlignes.

{% highlight python %}
q: List[List[float]] = [[], [], [], []]
for i in range(0, 101):
    q[0].append(np.quantile(real_carg_1år - lager_carg_1år, i * 0.01))  # type: ignore
    q[1].append(np.quantile(real_carg_5år - lager_carg_5år, i * 0.01))  # type: ignore
    q[2].append(np.quantile(real_carg_10år - lager_carg_10år, i * 0.01))  # type: ignore
    q[3].append(np.quantile(real_carg_20år - lager_carg_20år, i * 0.01))  # type: ignore

fig, ax1 = plt.subplots(1, 1, figsize=(6, 5))
for i, år in enumerate([1, 5, 10, 20]):
    ax1.plot(np.linspace(0.0, 1, 101), q[i], label=f"{år:1.0f} år", linewidth=4, alpha=0.7 + 0.1 * i)
ax1.legend()
ax1.set_xticks(np.linspace(0.0, 1.0, 11))
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel(r"$\mathrm{CAGR_{realtionsbeskatning}} - \mathrm{CAGR_{lagerbeskatning}}$")
ax1.set_ylim(-0.03, 0.03)
ax1.set_xlabel("Fraktil")
plt.tight_layout()
plt.savefig("fraktiler_lager_vs_real_2.svg")
{% endhighlight %}

Dette giver følgende plot.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/fraktiler_lager_vs_real_2.svg"> 
</p>

Det kan her tydeligt ses at jo længere investeringshorisonten er, jo bedre er realisationsbeskatning.

Den fulde kode kan findes her: [investeringsforening_udbytte.py]({{ site.baseurl }}/assets/python_scripts/investeringsforening_udbytte.py)
