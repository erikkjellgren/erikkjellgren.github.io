---
layout: post
title: Huspriser og renter
---

*Brug ikke dette som finansiel rådgivning. Dette er kun en model.*

Over de sidste 25 år har huspriserne i gennemsnit steget med en faktor 3.5.
Men hvilke drivere har være de primære til denne prisstigning, og kan disse fortsætte fremadrettet.
De primære drivere for stigning af huspriser er:

* Renter på boliglån 
* Lønstigninger
* Forøgelse af belåningsgrad
* Geografiske forskelle

I denne model vil belåningsgraden være antaget til at være konstant.
Givet at den er antaget at være konstant, så er den faktiske belåningsgrads ikke relevant.
Geografiske forskelle vil i første omgang ikke blive taget højde for, men vil til sidst blive diskuteret.

Modellen vil gøre brug af data fra 1994 og fremadrettet. 
Det er valgt at starte i 1994, da [mixlån](https://da.wikipedia.org/wiki/Mixl%C3%A5n), blev afskaffet i 1993, og lånestrukturen derefter blev den vi kender igennem realkreditten.

## Løn indeks konstruktion

Løn indekset er konstrueret ved at bruge data fra, [djoef.dk](https://www.djoef.dk/r-aa-dgivning/l-oe-n/l-oe-nforhandling/loenudvikling19922015forprivatansatte.aspx#IL-oe-nudvikling--19922016--for--privatansatte--dj-oe-fere), 07-04-2021.
Her er tallene eksl. anciennitetsafledte brugt, og det er antaget at den annualiserede stigning har været den samme for alle fire kvartaler.

For 2016 1. kv., 2. kv. og 3. kv. er der ingen data i de to sæt løn indekset er baseret på.
Disse er derfor antaget til at være 2.1% annualiseret.

For perioden efter 2016 1. kv., er der hentet data fra [statistikbanken.dk](https://www.statistikbanken.dk/statbank5a/selectvarval/define.asp?PLanguage=0&subword=tabsel&MainTable=SBLON1&PXSId=214666&tablestyle=&ST=SD&buttons=0), 07-04-2021.
Her er der valgt "Sektorer i alt" og "Erhverv i alt".

Det samlede sæt af annualiserede lønstigninger kan findes her, [loenstigning.txt]({{ site.baseurl }}/assets/python_scripts/data/loenstigning.txt).

Lønstignings indekset er så konstrueret ved at starte ved 1, også stige hvert kvartal, med den kvartalvise stigning, fundet via.

$$ s_\mathrm{kvartal} = \left( 1 + s_\mathrm{årlig} \right)^{3/12} - 1 $$

## Huspris indeks konstruktion

Huspris indekserne er taget fra [boliga.dk](https://www.boliga.dk/boligpriser), 09-04-2021.

Indekset for [Danmark](https://www.boliga.dk/boligpriser/resultater?area=72000&type=0&data=0),
[København](https://www.boliga.dk/boligpriser/resultater?area=77101&type=0&data=0),
[Odense](https://www.boliga.dk/boligpriser/resultater?area=77461&type=0&data=0),
[Aarhus](https://www.boliga.dk/boligpriser/resultater?area=77751&type=0&data=0),
[Aalborg](https://www.boliga.dk/boligpriser/resultater?area=77851&type=0&data=0),
[Lolland](https://www.boliga.dk/boligpriser/resultater?area=77360&type=0&data=0) og
[Langeland](https://www.boliga.dk/boligpriser/resultater?area=77482&type=0&data=0).

Indekserne er normeret således at 1. kv. 1994 er defineret til at være 1.

## Huskøbsomkostninger indeks konstruktion

Huskøbsomkostninger indekset er konstrueret med antagelse om 80% realkreditlån og 20% selvbetaling. 

For lånet skal der beregnes en total omkostning (lån + renter).
Der startes med at kigge hvor på hvor meget af lånet der er tilbage efter en måned:

$$ k_{1}=k_{\mathrm{lån}}\left(1+r\right)-k_{\mathrm{afbetaling}}\left(1+r\right) $$

Lånet vokser med renten, $$r$$, bemærk at renten også er inkluderet i afbetalingen, da det antages at der afbetales d. 1 i måneden,
hvor det tilbageværende kapital af lånet er for sidste dag i måneden, derfor "spares" noget af renten for måneden.

Efter to måneder vil der derfor være:

$$ \begin{eqnarray}
   k_{2}&=&k_{1}\left(1+r\right)-k_{\mathrm{afbetaling}}\left(1+r\right) \\
   &=&\left(k_{\mathrm{l\mathring{a}n}}\left(1+r\right)-k_{\mathrm{afbetaling}}\left(1+r\right)\right)\left(1+r\right)-k_{\mathrm{afbetaling}}\left(1+r\right) \\
   &=&k_{\mathrm{l\mathring{a}n}}\left(1+r\right)^{2}-k_{\mathrm{afbetaling}}\left(1+r\right)^{2}-k_{\mathrm{afbetaling}}\left(1+r\right) \\
   \end{eqnarray} $$

Det kan nu ses at det generelle udtryk derfor er:

$$ k_{n}=k_{\mathrm{\mathrm{lån}}}\left(1+r\right)^{n}-k_{\mathrm{afbetaling}}\sum_{l=1}^{n}\left(1+r\right)^{l} $$

Det vides at den geometriske serie er givet ved:

$$ \sum_{l=0}^{n-1}x^{l}=\left(\frac{1-x^{n}}{1-x}\right) $$

Denne kan skrives om til:

$$ \sum_{l=1}^{n}x^{l}=\left(\frac{1-x^{n}}{1-x}\right)-1+x^{n} $$

Ved at $$x\rightarrow 1+r$$ findes det nu at:

$$ k_{n}=k_{\mathrm{lån}}\left(1+r\right)^{n}-k_{\mathrm{afbetaling}}\left(\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1+\left(1+r\right)^{n}\right) $$

Lånet vil være tilbage betalt når $$k_{n}=0$$:

$$ 0=k_{\mathrm{lån}}\left(1+r\right)^{n}-k_{\mathrm{afbetalling}}\left(\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1+\left(1+r\right)^{n}\right) $$

Den månedlige afbetaling bliver nu:

$$ k_{\mathrm{afbetalling}}=\frac{k_{\mathrm{lån}}\left(1+r\right)^{n}}{\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1+\left(1+r\right)^{n}} $$

Den totale omkostning (lån + renter) ved lånet er nu:

$$ k_{\mathrm{total}}=\frac{k_{\mathrm{lån}}\left(1+r\right)^{n}\cdot n}{\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1+\left(1+r\right)^{n}} $$

Modellen for omkostningskorrigeret huspris vil derfor blive:

$$ \begin{eqnarray}
   k_{\mathrm{omkostning}} &=& \frac{0.8k_{\mathrm{huspris}}\left(1+r\right)^{n}\cdot n}{\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1+\left(1+r\right)^{n}}+0.2k_{\mathrm{huspris}} \\
   &=& \left(\frac{0.8\left(1+r\right)^{n}\cdot n}{\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1+\left(1+r\right)^{n}}+0.2\right)k_{\mathrm{huspris}} \label{eq1}\tag{1}
   \end{eqnarray} $$

Indekset er herefter normeret således at det er 1, ved 1. kv. 1994.

Til at estimere realkreditlåns renten er diskontoen brugt som proxy. 
Dataen for diskontoen er taget fra [nationalbanken.statistikbank.dk](https://nationalbanken.statistikbank.dk/nbf/98214).
Den hentede data kan findes her [diskonto.txt]({{ site.baseurl }}/assets/python_scripts/data/diskonto.txt).

## Diskussion af resultater

Resultaterne af modellen kan ses i nedenstående graf, bemærk at basis huskøbsomkostninger indekset og huspris indekset er baseret på huspriserne for hele Danmark.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/huspris_indekser.svg"> 
</p>

Det kan ses med det samme at hus priserne er steget markant siden 1994.
Dog kan vi se at huskøbsomkostninger indekset følger løn indekset over hele perioden, undtaget omkring 2007, som vi nu ved var en boligboble.
Modellen fanger altså boligpriserne var for høje i den periode.

Forskellen mellem huskøbsomkostninger indekset og huspris indekset kan tolkes til at være den rente-drevne stigning af boligpriserne.
Her skal det husket at renterne nu er så lave at de ikke kan forventes at falde fremadrette, så ud fra denne model kan det altså ikke forventes at boligpriserne vil fortsætte med at være så eksplosive.

Hvis renterne forventes at blive ved med at være tæt på nul det næste lange stykke tid, er der til gengæld heller ikke noget evidens for at boligmarkedet som aggregat er i en boble.

En vigtig men skjult antagelse i modellen er at den indirekte antager at alting var korrekt prissat i 1. kv. 1994. 
Denne antagelse er dog desværre svær at komme uden om.

Indtil videre er der ikke taget højde for geografiske effekter i boligpriserne.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/geografiske_forskelle.svg"> 
</p>

Som det tydeligt kan ses har geografien kæmpe betydning for udviklingen af boligpriserne.
Områder som Lolland og Langeland, som generelt anses til at være udkants Danmark oplever stagnerede huspriser, hvor København til gengæld oplever meget hurtigt voksende boligpriser.

En mulig forklaring på dette kunne være affolkning af udkantsområderne og tilflytning til de stører byer.
Om denne tese kan underbygges med data vil dog ikke undersøges i denne analyse.

En ting der kan bemærkes er dog at de tre næststørste byer (Aarhus, Aalborg og Odense), ligger omkring landsgennemsnittet i boligprisstigninger.
Hvilket kan tolkes til at det kun er København der oplever urbaniserings-effekten, eller at huspriserne kunne være for høje i København.
Den præsenterede model kan dog ikke sige noget specifikt om København.

I modellen er effekten af renter med taget eksplicit.
Så til sidst lad os kigge på hvad rente-stigninger kunne betyde for boligpriserne.

Ved at starte fra ligning (\ref{eq1}) kan det ses i modellen at huspriserne afhænger af renterne på følgende måde:

$$ k_{\mathrm{huspris}}=k_{\mathrm{omkostning}}\left(\frac{0.8\left(1+r\right)^{n}\cdot n}{\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1+\left(1+r\right)^{n}}+0.2\right)^{-1} $$

Dette kan nu plottes:

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/huspris_rente_funktion.svg"> 
</p>

I ovenstående figur kan husprisernes afhængighed af renten ses, givet at man har et budget til alle omkostning på 1.

Det kan ses at hvis renterne stiger "permanent" 2% vil priserne falde 20%, og hvis der er en "permanent" stigning på 4% vil priserne falde 35%.

Dette er selvfølgelig ikke overraskende, ved en belåningsgrad på 80% har renterne stor indflydelse på hvor meget man har råd til at låne.

<!-- python_split -->

## Python detaljer

Starter med at importere alle de moduler der skal bruges:
dkfinance_modeller er fra, [dkfinance_modeller](https://github.com/erikkjellgren/dkfinance_modeller)

{% highlight python %}
import matplotlib.pyplot as plt
import numpy as np

import dkfinance_modeller.utility.formler as formler
{% endhighlight %}

Konstruere huspris indekset og løn indekset.

{% highlight python %}
huspris = np.genfromtxt("data/huspriser_danmark.txt")
huspris_indeks = huspris / huspris[0]

labels = np.genfromtxt("data/labels.txt", dtype=str, delimiter=",")

diskonto = np.genfromtxt("data/diskonto.txt", delimiter=",")
diskonto_min = np.zeros(len(diskonto))
mindste = 10
for i, rente in enumerate(diskonto):
    mindste = min(mindste, rente)
    diskonto_min[i] = mindste

lønstigning = np.genfromtxt("data/loenstigning.txt")
lønstigning = (1 + lønstigning / 100) ** (3 / 12) - 1
løn_indeks = [1]
for stigning in lønstigning[1:]:
    løn_indeks.append(løn_indeks[-1] * (1 + stigning))
{% endhighlight %}

Konstruere omkostning indekset.

{% highlight python %}
husomkostninger = []
husomkostninger_min = []
for rente, rente_min, pris in zip(diskonto, diskonto_min, huspris):
    husomkostninger.append(
        formler.afbetalling(klån=pris * 0.8, n=30, r=rente / 100 + 10 ** -6) * 30 + 0.2 * pris
    )
    husomkostninger_min.append(
        formler.afbetalling(klån=pris * 0.8, n=30, r=rente_min / 100 + 10 ** -6) * 30 + 0.2 * pris
    )
husomkostninger_indeks = husomkostninger / husomkostninger[0]
husomkostninger_min_indeks = husomkostninger_min / husomkostninger_min[0]
{% endhighlight %}

Bygger graferne.

{% highlight python %}
plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, (ax2, ax1) = plt.subplots(2, 1, figsize=(6, 7), sharex=True)
ax1.plot(labels, husomkostninger_min_indeks, "r--", label="Huskøbsomkostninger indeks (minimum diskonto)")
ax1.plot(labels, husomkostninger_indeks, "k-", label="Huskøbsomkostninger indeks")
ax1.plot(labels, huspris_indeks, "m-", label="Huspris indeks")
ax1.plot(labels, løn_indeks, "g-", label="Løn indeks")
ax1.legend(frameon=False)

ax2.plot(labels, diskonto_min, "r--", label="Diskonto minimum")
ax2.plot(labels, diskonto, "k--", label="Diskonto")
ax2.set_ylim(-0.2, 5.5)
ax2.set_ylabel("Diskonto")
ax2.legend(frameon=False)

for i, tick in enumerate(ax1.get_xticklabels()):
    tick.set_rotation(90)
    if i % 4 != 0:
        tick.set_fontsize(0)
        tick.set_color("white")

ax1.set_xlim(-1, len(labels) + 1)
ax1.set_ylim(0.9, 4.0)
ax1.set_ylabel("Indeks værdi")
plt.tight_layout()
plt.savefig("huspris_indekser.svg")

huspris = np.genfromtxt("data/huspriser_danmark.txt")
københavn = np.genfromtxt("data/huspriser_koebenhavn.txt")
odense = np.genfromtxt("data/huspriser_odense.txt")
aarhus = np.genfromtxt("data/huspriser_aarhus.txt")
aalborg = np.genfromtxt("data/huspriser_aalborg.txt")
langeland = np.genfromtxt("data/huspriser_langeland.txt")
lolland = np.genfromtxt("data/huspriser_lolland.txt")
fig, ax1 = plt.subplots(1, 1, figsize=(6, 4), sharex=True)
ax1.plot(labels, huspris_indeks, "m-", label="Danmark indeks")
ax1.plot(labels, københavn / københavn[0], "k--", label="København indeks")
ax1.plot(labels, odense / odense[0], "b--", label="Odense indeks")
ax1.plot(labels, aarhus / aarhus[0], "g--", label="Aarhus indeks")
ax1.plot(labels, aalborg / aalborg[0], "r--", label="Aalborg indeks")
ax1.plot(labels, langeland / langeland[0], "c--", label="Langeland indeks")
ax1.plot(labels, lolland / lolland[0], "y--", label="Lolland indeks")
ax1.legend(frameon=False)

for i, tick in enumerate(ax1.get_xticklabels()):
    tick.set_rotation(90)
    if i % 4 != 0:
        tick.set_fontsize(0)
        tick.set_color("white")

ax1.set_xlim(-1, len(labels) + 1)
ax1.set_ylim(0.8, 8)
ax1.set_ylabel("Indeks værdi")
plt.tight_layout()
plt.savefig("geografiske_forskelle.svg")


relativ_huspris = []
for rente in np.linspace(0, 10, 1000):
    relativ_huspris.append(
        (formler.afbetalling(klån=1, n=30, r=rente / 100 + 10 ** -6) * 30 * 0.8 + 0.2) ** (-1)
    )

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(np.linspace(0, 10, 1000), relativ_huspris, linewidth=4)
ax1.set_ylabel("Relativ Huspris")
ax1.set_xlabel("Rente %")
ax1.grid(which="minor")
ax1.grid(which="major")
plt.tight_layout()
plt.savefig("huspris_rente_funktion.svg")
{% endhighlight %}

Den fulde kode kan findes her: [huspriser.py]({{ site.baseurl }}/assets/python_scripts/huspriser.py)
