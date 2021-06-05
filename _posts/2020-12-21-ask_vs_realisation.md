---
layout: post
title: ASK vs realisationsbeskatning
lang: dk
lang-ref: ASK-vs-realisationsbeskatning
tag: dkfinance
---

Aktiesparekonto (ASK) har begge lav beskatningsprocent på 17%,
men er tilgængelig lagerbeskattet.
I princippet vil realisationsbeskatning med aktiebeskatning på 27%/42% kunne give et højere afkast over en lang periode
pga renters rente.
Her vil der blive undersøgt hvor lang denne periode faktisk er.

Først skal den gevinst af depoterne kontureres.
Her bliver der taget udgangspunk i data for S&P500 (fordi denne data er nemt tilgængelig), dataene er hentet fra, [www.econ.yale.edu](http://www.econ.yale.edu/~shiller/data/ie_data.xls), 16-11-2020.
Den procentvise stigning af ETFens kurs er nu den procentvise stigning af S&P500 plus det procentvise udbytte.
Se [SP500.csv]({{ site.baseurl }}/assets/python_scripts/data/SP500.csv) for den behandlede data.

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

Depoterne er konstrueret med 0.0% ÅOP for at emulere det bedste scenarie for realisationsbeskatning.
Altså hvis man investere direkte i aktier i stedet for at købe ETFer og investeringsforeninger.

Nu defineres depottet i modellen.

{% highlight python %}
def depoter(
    start_kapital: float
) -> Tuple[depotmodel.DepotModel, depotmodel.DepotModel, depotmodel.DepotModel]:
    """Definere depoter.

    Args:
      start_kapital: Start kapital for depoterne.

    Returns:
      Depot med lagerbeskatning, og to depoter med realationsbeskatning.
    """
    etf1 = værdipapirer.ETF(kurs=100, åop=0.0 / 100, beskatningstype="lager")
    etf2 = værdipapirer.ETF(kurs=100, åop=0.0 / 100, beskatningstype="realisation")
    etf3 = værdipapirer.ETF(kurs=100, åop=0.0 / 100, beskatningstype="realisation")
    skatter1 = skat.Skat(beskatningstype="ask")
    skatter2 = skat.Skat(beskatningstype="aktie")
    skatter3 = skat.Skat(beskatningstype="ask")
    skatter3.skatteprocenter = [0.42]
    ask = depotmodel.DepotModel(
        kapital=start_kapital,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44),
        skatteklasse=skatter1,
        minimumskøb=1000,
        ETFer=[etf1],
        ETF_fordeling=[1.0],
    )
    normal = depotmodel.DepotModel(
        kapital=start_kapital,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44, underkonto=True),
        skatteklasse=skatter2,
        minimumskøb=1000,
        ETFer=[etf2],
        ETF_fordeling=[1.0],
        valutafunktion=valuta.saxo_underkonto_kurtage,
    )
    normal_worst_case = depotmodel.DepotModel(
        kapital=start_kapital,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44, underkonto=True),
        skatteklasse=skatter3,
        minimumskøb=1000,
        ETFer=[etf3],
        ETF_fordeling=[1.0],
        valutafunktion=valuta.saxo_underkonto_kurtage,
    )
    return ask, normal, normal_worst_case
{% endhighlight %}

Her er der to forskellige realisationsbeskattede depoter. 
Det ene har 27%/42% beskatning med den fulde progressionsgrænse,
dette er best-case for realisationsbeskatning og relevant hvis dette er det fulde depot.
Det andet har altid 42% beskatning og modellere at der er et sideliggende depot der bruger hele progressionsgrænsen.
Dette vil være worst-case for realisationsbeskatning

Modellen bliver nu defineret.

{% highlight python %}
def kør_model(  # pylint: disable=R0914
    start_kapital: float
) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
    """Definere depoter.

    Args:
      start_kapital: Start kapital for depoterne.

    Returns:
      Fraktiler for CAGR for forskellige depot typer.
    """
    data = np.genfromtxt("data/SP500.csv", delimiter=";")
    ask: List[List[float]] = [[], [], []]
    normal: List[List[float]] = [[], [], []]
    normal_worst_case: List[List[float]] = [[], [], []]
    for j, antal_år in enumerate([20, 30, 40]):
        for start in range(0, len(data) - 950 - antal_år * 12):
            askdepot, normaldepot, normaldepot_worst_case = depoter(start_kapital)
            for i in range(start + 950, start + 950 + 12 * antal_år):
                udbytteafkast = askdepot.ETFer[0].kurs * data[i + 1, 4]
                kursafkast = askdepot.ETFer[0].kurs * data[i + 1, 3]
                askdepot.afkast_månedlig([kursafkast], [udbytteafkast])
                normaldepot.afkast_månedlig([kursafkast], [udbytteafkast])
                normaldepot_worst_case.afkast_månedlig([kursafkast], [udbytteafkast])
                if i % 12 == 0:
                    normaldepot.skatteklasse.progressionsgrænse *= 1 + 0.02
            ask[j].append(askdepot.total_salgsværdi())
            normal[j].append(normaldepot.total_salgsværdi())
            normal_worst_case[j].append(normaldepot_worst_case.total_salgsværdi())

    ask_cagr = []
    normal_cagr = []
    normal_worst_case_cagr = []
    for år, depot1, depot2, depot3 in zip([20, 30, 40], ask, normal, normal_worst_case):
        ask_cagr.append(formler.CAGR(start_kapital, np.array(depot1), år))
        normal_cagr.append(formler.CAGR(start_kapital, np.array(depot2), år))
        normal_worst_case_cagr.append(formler.CAGR(start_kapital, np.array(depot3), år))
    ask_q = []
    normal_q = []
    normal_worst_case_q = []
    for cagr1, cagr2, cagr3 in zip(ask_cagr, normal_cagr, normal_worst_case_cagr):
        q1 = []
        q2 = []
        q3 = []
        for j in range(0, 1001):
            q1.append(np.quantile(cagr1, j * 0.001))
            q2.append(np.quantile(cagr2, j * 0.001))
            q3.append(np.quantile(cagr3, j * 0.001))
        ask_q.append(q1)
        normal_q.append(q2)
        normal_worst_case_q.append(q3)
    return ask_q, normal_q, normal_worst_case_q
{% endhighlight %}

Sammenligningen mellem ASK og realisationsbeskatning køres nu og plottes.

{% highlight python %}
plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

ask_fraktil, mormal_fraktil, normal_worst_case_fraktil = kør_model(102300)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 8), sharex=True)
for depot, navn in zip([ask_fraktil, mormal_fraktil, normal_worst_case_fraktil], ["ASK", "27%/42%", "42%"]):
    for ax, serie in zip([ax1, ax2, ax3], depot):
        ax.plot(np.linspace(0.0, 1, 1001), serie, label=navn, linewidth=3)
ax1.legend()
for ax, år_inv in zip([ax1, ax2, ax3], [20, 30, 40]):
    ax.set_xticks(np.linspace(0.0, 1.0, 11))
    ax.grid(which="minor")
    ax.grid(which="major")
    ax.set_ylabel("CAGR")
    ax.set_title(f"{år_inv:1.0f} år investering")
ax3.set_xlabel("Fraktil")
plt.tight_layout()
plt.savefig("ask_vs_real.svg")
{% endhighlight %}

Dette giver følgende plot.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/ask_vs_real.svg"> 
</p>

På grafen ses CAGR efter omkostninger for de tre forskellige depoter.
Alt efter hvor meget af progressionsgrænsen der bliver opbrugt af andre depoter,
vil realisationsbeskatningen ligge mellem 27%/42% og 42%.
Det kan bemærkes at selv efter 40 år vil ASK være en fordel ift. at investere realisationsbeskattet.

Det er ikke overraskende at ASK giver bedre afkast selv efter lange perioder +40 år.
Dette kan sammenlignes med hvad man får via. en gennemsnitsmodel.

Den simple form for lagerbeskatning er:

$$ L = k\cdot\left(1+a\cdot\left(1-s\right)\right)^{y} $$

med $$k$$ start kapital, $$a$$ afkast per år, $$s$$ skatteprocent og $$y$$ år.

Den simple form for realisationsbeskatning er:

$$ R = k\cdot\left(1+a\right)^{y}-\left(k\cdot\left(1+a\right)^{y}-k\right)\cdot q $$

med $$q$$ skatteprocent.

Disse to kan nu sættes lig med hinanden for at finde hvilket år skiftet går ved:

$$ \begin{eqnarray}
   k\cdot\left(1+a\cdot\left(1-s\right)\right)^{y}&=&k\cdot\left(1+a\right)^{y}-\left(k\cdot\left(1+a\right)^{y}-k\right)\cdot q \\
   k\cdot\left(1+a-a\cdot s\right)^{y}&=&k\cdot\left(\left(1+a\right)^{y}-\left(1+a\right)^{y}\cdot q+q\right) \\
   \left(1+a-a\cdot s\right)^{y}&=&\left(1+a\right)^{y}\cdot\left(1-q\right)+q
   \end{eqnarray} $$

Jeg tror at den ovenstående kan ses til at være en [transcendental equation](https://en.wikipedia.org/wiki/Transcendental_equation), så den løses kun numerisk herfra.

Definere nu ligningen således den løses approksimativt og plotter løsningen:

{% highlight python %}
def gennemsnit_ask_vs_real(cagr):
    """
    Regner forskellen i depot størrelse mellem et lagerbeskattet,
    og et realisationsbeskattet depot.
    Dette er baseret på en gennemsnits model for afkast.

    Args:
      cagr: CAGR

    Returns:
      Forskellen mellem lagerbeskattet og realisationsbeskattet.
    """
    s = 0.17
    q = 0.42
    y = np.linspace(0, 200, 10000)
    return (1 + cagr - cagr * s) ** y - (1 + cagr) ** y * (1 - q) - q


As = []
years = []
for m in range(20, 201):
    As.append(m / 1000)
    f = gennemsnit_ask_vs_real(m / 1000)
    years.append(len(f[f - 10 ** -12 > 0]) / 10000 * 200)
fig, ax1 = plt.subplots(1, 1, figsize=(6, 4), sharex=True)
ax1.plot(As, years, linewidth=3)
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("År")
ax1.set_xlabel("CAGR før skat")
plt.tight_layout()
plt.savefig("ask_vs_real_gennemsnit.svg")
{% endhighlight %}

Dette giver følgende plot.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/ask_vs_real_gennemsnit.svg"> 
</p>

Det kan ses at for CAGR (før skat) på 7.5% ville det tage lidt over 40 år før renters-rente fra realisationsbeskatning ville give en fordel.
Dette underbygger at for den komplicerede model at det findes at ASK "altid" kan betale sig.

Den fulde kode kan findes her: [ask_vs_realisation.py]({{ site.baseurl }}/assets/python_scripts/ask_vs_realisation.py)
