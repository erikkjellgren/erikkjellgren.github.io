---
layout: post
title: House prices and interest rates
lang: en
lang-ref: huspriser-og-renter
tag: dkfinance
---

Over the past 25 years the house prices have appreciated by a factor of ~3.5.
But what drivers have been the primiary for this prise appreciation, and can this continue going forward?
The primiary drivers for appreciation of house prices is:

* Interest rates on mortgages
* Wage increases
* Increase in loan-to-value ratio
* Geographical differences

In this model the loan-to-value ratio will be assumed to be constant in time.
Given that the loan-to-value ratio is assumed to be constant, then the numerical value of this number is not very relevant.
Geographical differences will in the first part be ignored, but will be discussed in the end.

The model will use data from 1994 and going forward.
1994 is chosen as starting point, since [mixloan](https://da.wikipedia.org/wiki/Mixl%C3%A5n) was phased out in 1993, and the loanstructure still in use in Denmark was introduced.

## Wage index contruction

The wage index is constructed using data from, [djoef.dk](https://www.djoef.dk/r-aa-dgivning/l-oe-n/l-oe-nforhandling/loenudvikling19922015forprivatansatte.aspx#IL-oe-nudvikling--19922016--for--privatansatte--dj-oe-fere), 21-05-2022.
The numbers used are those that are not seniority-derived, and it is assumed that the increase over a single year is equal for all four quarters

For the periode after 2016 Q3, the data is downloaded from [statistikbanken.dk](https://www.statistikbanken.dk/statbank5a/selectvarval/define.asp?PLanguage=0&subword=tabsel&MainTable=SBLON1&PXSId=214666&tablestyle=&ST=SD&buttons=0), 21-05-2022.
Here the sections chosen is "Sektorer i alt" and "Erhverv i alt".

For 2016 Q1, Q2, and Q3, there is no data for wages in the two data sets the wage index is contructed from.
These quarters are, therefore, assumed to be 2.1% annualized.

The total constructed data set for annualized wage increased kan be found here, [loenstigning.txt]({{ site.baseurl }}/assets/python_scripts/data/loenstigning.txt).

The quarterly wage increase index is now contructed by normalizing the first point to be unity, and then applying the quarterly increase from the annual increase using the equation below:

$$ s_\mathrm{kvartal} = \left( 1 + s_\mathrm{årlig} \right)^{3/12} - 1 $$

## Housing price index contruction

The housing price index is downloaded from [boliga.dk](https://www.boliga.dk/boligpriser), 21-05-2022.

The index for [Danmark](https://www.boliga.dk/boligpriser/resultater?area=72000&type=0&data=0),
[København](https://www.boliga.dk/boligpriser/resultater?area=77101&type=0&data=0),
[Odense](https://www.boliga.dk/boligpriser/resultater?area=77461&type=0&data=0),
[Aarhus](https://www.boliga.dk/boligpriser/resultater?area=77751&type=0&data=0),
[Aalborg](https://www.boliga.dk/boligpriser/resultater?area=77851&type=0&data=0),
[Lolland](https://www.boliga.dk/boligpriser/resultater?area=77360&type=0&data=0), and
[Langeland](https://www.boliga.dk/boligpriser/resultater?area=77482&type=0&data=0).

The indicies are normalized to being unity at 1994 Q1.

## House purchase costs index contruction

The house purchase costs index is constructed with the assumption of 80% realcreditloan and 20% downpayment.

For the loan the total costs need to be calculated (loan + interest).
Starting from how much of the loan is left after one month:

$$ k_{1}=k_{\mathrm{loan}}\cdot\left(1+r\right)-k_{\mathrm{repayment}}\cdot\left(1+r\right) $$

The loan growth by the amount of the interest, $$r$$, note that the interest is also included in the repayment amount, because it is assumed that the repayment falls in the 1st in the month.

After two months the remianing principal will be:

$$ \begin{eqnarray}
   k_{2}&=&k_{1}\cdot\left(1+r\right)-k_{\mathrm{repayment}}\cdot\left(1+r\right) \\
   &=&\left(k_{\mathrm{l\mathring{a}n}}\cdot\left(1+r\right)-k_{\mathrm{repayment}}\cdot\left(1+r\right)\right)\cdot\left(1+r\right)-k_{\mathrm{repayment}}\cdot\left(1+r\right) \\
   &=&k_{\mathrm{l\mathring{a}n}}\cdot\left(1+r\right)^{2}-k_{\mathrm{repayment}}\cdot\left(1+r\right)^{2}-k_{\mathrm{repayment}}\cdot\left(1+r\right) \\
\end{eqnarray} $$

It can now be seen that the general expression is:

$$ k_{n}=k_{\mathrm{\mathrm{loan}}}\cdot\left(1+r\right)^{n}-k_{\mathrm{repayment}}\cdot\sum_{l=0}^{n}\left(1+r\right)^{l} $$

It is known that the geometric series is given by:

$$ \sum_{l=0}^{n-1}x^{l}=\left(\frac{1-x^{n}}{1-x}\right) $$

By substituting $$x\rightarrow 1+r$$ it can now be found that:

$$ k_{n}=k_{\mathrm{loan}}\cdot\left(1+r\right)^{n}-k_{\mathrm{repayment}}\cdot\left(\frac{1-\left(1+r\right)^{n}}{-r}\right) $$

The loan will be payed out when $$k_{n}=0$$:

$$ 0=k_{\mathrm{loan}}\cdot\left(1+r\right)^{n}-k_{\mathrm{repayment}}\cdot\left(\frac{1-\left(1+r\right)^{n}}{-r}\right) $$

The monthly repayment is now:

$$ \begin{eqnarray}
    k_{\mathrm{repayment}} &=& k_{\mathrm{loan}}\cdot\frac{\left(1+r\right)^{n}}{\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)} \\
    &=& k_{\mathrm{loan}}\cdot\frac{-r\cdot\left(1+r\right)^{n}}{1-\left(1+r\right)^{n}} \\
    &= & k_{\mathrm{loan}}\cdot\frac{-r}{\left(1-\left(1+r\right)^{n}\right)\cdot\left(1+r\right)^{-n}} \\
    &=& k_{\mathrm{loan}}\cdot\frac{r}{1-\left(1+r\right)^{-n}}
\end{eqnarray} $$

The total house purchase costs (principal + interest) of the loan is now:

$$ k_{\mathrm{total}}=k_{\mathrm{loan}}\cdot\frac{r\cdot n}{1-\left(1+r\right)^{-n}} $$

Modellen for omkostningskorrigeret huspris vil derfor blive:
The model for total house purchase costs corrigated housing price is now:

$$ \begin{eqnarray}
   k_{\mathrm{total\ costs}} &=& 0.8\cdot k_{\mathrm{housing\ price}}\cdot\frac{r\cdot n}{1-\left(1+r\right)^{-n}}+0.2\cdot k_{\mathrm{housing\ price}} \\
   &=& \left(0.8\cdot \frac{r\cdot n}{1-\left(1+r\right)^{-n}}+0.2\right)\cdot k_{\mathrm{housing\ price}} \label{eq1}\tag{1}
\end{eqnarray} $$

The index is normalized to unity at 1994 Q1.

To estimate the interestrate of the realcredit loan the long-interestrate is used as a proxy.
The data from the long-interestrate is downloaded from [data.oecd.org](https://data.oecd.org/interest/long-term-interest-rates.htm), 21-05-2022.
The downloaded data can be found here [langrente.txt]({{ site.baseurl }}/assets/python_scripts/data/langrente.txt).

## Discussion of results

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

$$ k_{\mathrm{housing\ price}}=k_{\mathrm{total\ costs}}\left(0.8\cdot \frac{r\cdot n}{1-\left(1+r\right)^{-n}}+0.2\right)^{-1} $$

Dette kan nu plottes:

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/huspris_rente_funktion.svg">
</p>

I ovenstående figur kan husprisernes afhængighed af renten ses, givet at man har et budget til alle omkostning på 1.

Det kan ses at hvis renterne stiger "permanent" 2% vil priserne falde 20%, og hvis der er en "permanent" stigning på 4% vil priserne falde 35%.

Dette er selvfølgelig ikke overraskende, ved en beloaningsgrad på 80% har renterne stor indflydelse på hvor meget man har råd til at loane.

Koden brugt til at lave graferne kan findes her: [huspriser.py]({{ site.baseurl }}/assets/python_scripts/huspriser.py)
