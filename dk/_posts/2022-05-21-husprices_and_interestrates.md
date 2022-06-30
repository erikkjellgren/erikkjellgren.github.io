---
layout: post
title: Huspriser og renter
lang: dk
lang-ref: huspriser-og-renter
tag: dkfinance
---

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
Det er valgt at starte i 1994, da [mixlån](https://da.wikipedia.org/wiki/Mixl%C3%A5n) blev afskaffet i 1993, og lånestrukturen derefter blev den vi kender igennem realkreditten.

## Løn indeks konstruktion

Løn indekset er konstrueret ved at bruge data fra, [djoef.dk](https://www.djoef.dk/r-aa-dgivning/l-oe-n/l-oe-nforhandling/loenudvikling19922015forprivatansatte.aspx#IL-oe-nudvikling--19922016--for--privatansatte--dj-oe-fere), 21-05-2022.
Her er tallene eksl. anciennitetsafledte brugt, og det er antaget at den annualiserede stigning har været den samme for alle fire kvartaler.

For perioden efter 2016 1. kv., er der hentet data fra [statistikbanken.dk](https://www.statistikbanken.dk/statbank5a/selectvarval/define.asp?PLanguage=0&subword=tabsel&MainTable=SBLON1&PXSId=214666&tablestyle=&ST=SD&buttons=0), 21-05-2022.
Her er der valgt "Sektorer i alt" og "Erhverv i alt".

For 2016 1. kv., 2. kv. og 3. kv. er der ingen data i de to sæt løn indekset er baseret på.
Disse er derfor antaget til at være 2.1% annualiseret.

Det samlede sæt af annualiserede lønstigninger kan findes her, [loenstigning.txt]({{ site.baseurl }}/assets/python_scripts/data/loenstigning.txt).

Lønstignings indekset er så konstrueret ved at starte ved 1, også stige hvert kvartal, med den kvartalvise stigning, fundet via.

$$ s_\mathrm{kvartal} = \left( 1 + s_\mathrm{årlig} \right)^{3/12} - 1 $$

## Huspris indeks konstruktion

Huspris indekserne er taget fra [boliga.dk](https://www.boliga.dk/boligpriser), 21-05-2022.

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

$$ k_{1}=k_{\mathrm{lån}}\cdot\left(1+r\right)-k_{\mathrm{afbetaling}}\cdot\left(1+r\right) $$

Lånet vokser med renten, $$r$$, bemærk at renten også er inkluderet i afbetalingen, da det antages at der afbetales d. 1 i måneden,
hvor det tilbageværende kapital af lånet er for sidste dag i måneden, derfor "spares" noget af renten for måneden.

Efter to måneder vil der derfor være:

$$ \begin{eqnarray}
   k_{2}&=&k_{1}\cdot\left(1+r\right)-k_{\mathrm{afbetaling}}\cdot\left(1+r\right) \\
   &=&\left(k_{\mathrm{l\mathring{a}n}}\cdot\left(1+r\right)-k_{\mathrm{afbetaling}}\cdot\left(1+r\right)\right)\cdot\left(1+r\right)-k_{\mathrm{afbetaling}}\cdot\left(1+r\right) \\
   &=&k_{\mathrm{l\mathring{a}n}}\cdot\left(1+r\right)^{2}-k_{\mathrm{afbetaling}}\cdot\left(1+r\right)^{2}-k_{\mathrm{afbetaling}}\cdot\left(1+r\right) \\
\end{eqnarray} $$

Det kan nu ses at det generelle udtryk derfor er:

$$ k_{n}=k_{\mathrm{\mathrm{lån}}}\cdot\left(1+r\right)^{n}-k_{\mathrm{afbetaling}}\cdot\sum_{l=0}^{n}\left(1+r\right)^{l} $$

Det vides at den geometriske serie er givet ved:

$$ \sum_{l=0}^{n-1}x^{l}=\left(\frac{1-x^{n}}{1-x}\right) $$

Ved at $$x\rightarrow 1+r$$ findes det nu at:

$$ k_{n}=k_{\mathrm{lån}}\cdot\left(1+r\right)^{n}-k_{\mathrm{afbetaling}}\cdot\left(\frac{1-\left(1+r\right)^{n}}{-r}\right) $$

Lånet vil være tilbage betalt når $$k_{n}=0$$:

$$ 0=k_{\mathrm{lån}}\cdot\left(1+r\right)^{n}-k_{\mathrm{afbetalling}}\cdot\left(\frac{1-\left(1+r\right)^{n}}{-r}\right) $$

Den månedlige afbetaling bliver nu:

$$ \begin{eqnarray}
    k_{\mathrm{afbetalling}} &=& k_{\mathrm{lån}}\cdot\frac{\left(1+r\right)^{n}}{\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)} \\
    &=& k_{\mathrm{lån}}\cdot\frac{-r\cdot\left(1+r\right)^{n}}{1-\left(1+r\right)^{n}} \\
    &= & k_{\mathrm{lån}}\cdot\frac{-r}{\left(1-\left(1+r\right)^{n}\right)\cdot\left(1+r\right)^{-n}} \\
    &=& k_{\mathrm{lån}}\cdot\frac{r}{1-\left(1+r\right)^{-n}}
\end{eqnarray} $$

Den totale omkostning (lån + renter) ved lånet er nu:

$$ k_{\mathrm{total}}=k_{\mathrm{lån}}\cdot\frac{r\cdot n}{1-\left(1+r\right)^{-n}} $$

Modellen for omkostningskorrigeret huspris vil derfor blive:

$$ \begin{eqnarray}
   k_{\mathrm{omkostning}} &=& 0.8\cdot k_{\mathrm{huspris}}\cdot\frac{r\cdot n}{1-\left(1+r\right)^{-n}}+0.2\cdot k_{\mathrm{huspris}} \\
   &=& \left(0.8\cdot \frac{r\cdot n}{1-\left(1+r\right)^{-n}}+0.2\right)\cdot k_{\mathrm{huspris}} \label{eq1}\tag{1}
\end{eqnarray} $$

Indekset er herefter normeret således at det er 1, ved 1. kv. 1994.

Til at estimere realkreditlåns renten er den lange rente brugt som proxy.
Dataen for den lange rente er taget fra [data.oecd.org](https://data.oecd.org/interest/long-term-interest-rates.htm), 21-05-2022.
Den hentede data kan findes her [langrente.txt]({{ site.baseurl }}/assets/python_scripts/data/langrente.txt).

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

$$ k_{\mathrm{huspris}}=k_{\mathrm{omkostning}}\left(0.8\cdot \frac{r\cdot n}{1-\left(1+r\right)^{-n}}+0.2\right)^{-1} $$

Dette kan nu plottes:

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/huspris_rente_funktion.svg">
</p>

I ovenstående figur kan husprisernes afhængighed af renten ses, givet at man har et budget til alle omkostning på 1.

Det kan ses at hvis renterne stiger "permanent" 2% vil priserne falde 20%, og hvis der er en "permanent" stigning på 4% vil priserne falde 35%.

Dette er selvfølgelig ikke overraskende, ved en belåningsgrad på 80% har renterne stor indflydelse på hvor meget man har råd til at låne.

Koden brugt til at lave graferne kan findes her: [huspriser.py]({{ site.baseurl }}/assets/python_scripts/huspriser.py)
