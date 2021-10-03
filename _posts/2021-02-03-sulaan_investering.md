---
layout: post
title: Investering af SU lån
lang: dk
lang-ref: Investering-af-SU-lån
tag: dkfinance
---

Under uddannelse er det muligt at tage SU-lån.
Hvis man tager SU-lån kun til investering, hvad kan man så forvente efter lånet er blevet tilbage betalt?
Dette vil blive undersøgt i den følgende model.

## Model beskrivelse

For modellen er følger den underliggende historiske data S&P500, dataene er hentet fra, [www.econ.yale.edu](http://www.econ.yale.edu/~shiller/data/ie_data.xls), 16-11-2020.
Se [SP500.csv]({{ site.baseurl }}/assets/python_scripts/data/SP500.csv) for den behandlede data.

To forskellige længder optagelse af lån hver måned bliver simuleret, 3 år og 5 år.
5 år er repræsentativ for en bachelor + kandidat uddannelse.
I praktisk er der 1 måned mellem bachelor og kandidat hvor man ikke er under uddannelse, og burde have en rente derefter.
Denne periode er negligeret i modellen, og det vil blive regnet som om at de 5 år er en lang uddannelse.

Under uddannelse er renten 4%, hvorefter den er X% i modellen.
Lige nu er renten på SU lån efter uddannelse 1%, men lånet er ikke fast forrentet, så det kan i princippet ændre sig i fremtiden.

Afbetalingen af SU lånet er regnet således at det lige præcis vil gå op til den givne afbetalingsperiode (der afhænger af størrelsen af lånet).

Fra renterne på SU lånet vil der være 27% rente-fradrag.

For alle X% renter, vil der blive simuleret en best-case situation og en worst-case situation.
Best-case er hvor hele progressionsgrænsen for aktie-beskatningen er tilgængelig til det investerede beløb fra lånet.
Worst-case er hvor det er antaget af hele progressionsgrænsen er opbrugt af andre investeringer, således vil beløbet fra SU-lånet blive beskattet med 42% aktie-beskatningen.
I modellen antages det at der bliver investeret i en lagerbeskattet ETF.

## Diskussion af resultater

Resultaterne af modellen kan ses i nedenstående graf.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/sulaan_profit.svg">
</p>

Ovenstående graf viser det forventede afkast efter tilbagebetaling af SU lånet.
De 'fulde' linjer er hvor den fulde progressionsgrænse (for aktie-beskatningen) vil være tilgængelig til SU lånet.
Den stiplede linje er hvor hele progressionsgrænse er brugt andet sted.
De forskellige farver repræsentere renten på lånet efter afsluttet uddannelse.

Givet at investerings perioden er ~20 år, og at dem som vælger at investere SU lån formentlig også har andre investeringer vil den følgende diskussion fokusere på de stiplede linjer.

For begge uddannelseslængder vil det historisk altid kunne betale sig at tage SU lån til investering givet en rente på 1% efter afsluttet uddannelse.

Man skal bemærke at jo kortere uddannelsen er, jo større er risiko, da afbetalingsperioden vil være kortere.
Dette kan ses ved at hvis renten stiger til bare 3%, vil der være ~20% risiko for tab ved at investere SU lånet over en 3 årig uddannelse.
Hvor investering af lånet over en 5 årig uddannelse, først vil have risiko for tab ved renter over 3%, givet at aktiemarkedet opfører sig som det har gjort historisk.

Givet den lange investeringshorisont der kommer med investering af et SU lån, er den største risiko, rente risikoen.
Selvom det renten ikke vil se ud til at stige de kommende år, kan det være svært at vide hvad der vil ske bare 5 år ud i fremtiden.
Hvilket kan have stor betydning, da SU lån ikke er fast-forrentet.


<!-- python_split -->

## Python detaljer

Starter med at importere alle de moduler der skal bruges:
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
import dkfinance_modeller.laan.laanmodel as laanmodel
{% endhighlight %}

Definere aktie-depoterne

{% highlight python %}
def depoter() -> Tuple[depotmodel.DepotModel, depotmodel.DepotModel]:
    """Definere depoter.

    Returns:
      Depot med lagerbeskatning.
    """
    etf1 = værdipapirer.ETF(kurs=100, åop=0.12 / 100, beskatningstype="lager")
    etf2 = værdipapirer.ETF(kurs=100, åop=0.12 / 100, beskatningstype="lager")
    skatter1 = skat.Skat(beskatningstype="aktie")
    skatter2 = skat.Skat(beskatningstype="ask")
    skatter2.skatteprocenter = [0.42]
    normal_depot = depotmodel.DepotModel(
        kapital=0.0,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44, underkonto=True),
        skatteklasse=skatter1,
        minimumskøb=1000,
        ETFer=[etf1],
        ETF_fordeling=[1.0],
        valutafunktion=valuta.saxo_underkonto_kurtage,
    )
    normal_worst_case = depotmodel.DepotModel(
        kapital=0.0,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44, underkonto=True),
        skatteklasse=skatter2,
        minimumskøb=1000,
        ETFer=[etf2],
        ETF_fordeling=[1.0],
        valutafunktion=valuta.saxo_underkonto_kurtage,
    )
    return normal_depot, normal_worst_case
{% endhighlight %}

Kører modellen.

{% highlight python %}
data = np.genfromtxt("data/SP500.csv", delimiter=";")
normal: List[List[float]] = [[], [], [], [], [], [], [], []]
worst_case: List[List[float]] = [[], [], [], [], [], [], [], []]
for k, uddannelse_længde in enumerate([3 * 12, 5 * 12]):
    for j, rente in enumerate([1.0, 3.0, 5.0, 7.0]):
        for start in range(0, len(data) - 950 - 22 * 12):
            depot, depot_worst_case = depoter()
            tab = [0.0, 0.0]
            sulån = laanmodel.SUlån(uddannelse_længde, 16, rente)
            i = start
            for afdrag, fradrag in sulån.propager_måned():
                if depot.total_salgsværdi() >= -min(0, afdrag + fradrag) and tab[0] == 0.0:
                    if afdrag + fradrag < 0.0:
                        depot.frigør_kapital(-(afdrag + fradrag))
                    depot.kapital += afdrag + fradrag
                    kursafkast = depot.ETFer[0].kurs * (data[i + 1, 4] + data[i + 1, 3])
                    depot.afkast_månedlig([kursafkast], [0.0])
                else:
                    if tab[0] == 0.0:
                        tab[0] = depot.total_salgsværdi()
                    tab[0] += afdrag + fradrag
                if depot_worst_case.total_salgsværdi() >= -min(0, afdrag + fradrag) and tab[1] == 0.0:
                    if afdrag + fradrag < 0.0:
                        depot_worst_case.frigør_kapital(-(afdrag + fradrag))
                    depot_worst_case.kapital += afdrag + fradrag
                    kursafkast = depot_worst_case.ETFer[0].kurs * (data[i + 1, 4] + data[i + 1, 3])
                    depot_worst_case.afkast_månedlig([kursafkast], [0.0])
                else:
                    if tab[1] == 0.0:
                        tab[1] = depot_worst_case.total_salgsværdi()
                    tab[1] += afdrag + fradrag
                if i % 12 == 0:
                    depot.skatteklasse.progressionsgrænse *= 1 + 0.02
                i += 1
            if tab[0] == 0.0:
                normal[4 * k + j].append(depot.total_salgsværdi())
            else:
                normal[4 * k + j].append(tab[0])
            if tab[1] == 0.0:
                worst_case[4 * k + j].append(depot_worst_case.total_salgsværdi())
            else:
                worst_case[4 * k + j].append(tab[1])
{% endhighlight %}

Konstruerer grafen.

{% highlight python %}
plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

normal_q = []
worst_case_q = []
for i in range(8):
    q1 = []
    q2 = []
    for j in range(0, 1001):
        q1.append(np.quantile(normal[i], j * 0.001))
        q2.append(np.quantile(worst_case[i], j * 0.001))
    normal_q.append(q1)
    worst_case_q.append(q2)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 10), sharex=True)
ax1.plot(np.linspace(0.0, 1, 1001), normal_q[0], "tab:blue", label="1%", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), worst_case_q[0], "tab:blue", linestyle="--", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), normal_q[1], "tab:orange", label="3%", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), worst_case_q[1], "tab:orange", linestyle="--", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), normal_q[2], "tab:green", label="5%", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), worst_case_q[2], "tab:green", linestyle="--", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), normal_q[3], "tab:red", label="7%", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), worst_case_q[3], "tab:red", linestyle="--", linewidth=3)

ax2.plot(np.linspace(0.0, 1, 1001), normal_q[4], "tab:blue", label="1%", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), worst_case_q[4], "tab:blue", linestyle="--", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), normal_q[5], "tab:orange", label="3%", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), worst_case_q[5], "tab:orange", linestyle="--", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), normal_q[6], "tab:green", label="5%", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), worst_case_q[6], "tab:green", linestyle="--", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), normal_q[7], "tab:red", label="7%", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), worst_case_q[7], "tab:red", linestyle="--", linewidth=3)

ax1.legend()
ax1.set_title("3 årig uddannelse")
ax2.set_title("5 årig uddannelse")
ax1.grid(which="minor")
ax1.grid(which="major")
ax2.grid(which="minor")
ax2.grid(which="major")
ax1.set_ylim(-0.6 * 10 ** 5, 2 * 10 ** 5)
ax2.set_ylim(-1.2 * 10 ** 5, 3.5 * 10 ** 5)
ax2.set_xlabel("Fraktil")
ax1.set_ylabel("Profit DKK")
ax2.set_ylabel("Profit DKK")
plt.tight_layout()
plt.savefig("sulaan_profit.svg")
{% endhighlight %}

Den fulde kode kan findes her: [sulaan_investering.py]({{ site.baseurl }}/assets/python_scripts/sulaan_investering.py)
