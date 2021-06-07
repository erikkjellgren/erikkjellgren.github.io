---
layout: post
title: Overlap mellem Danske investeringsforeninger
lang: dk
lang-ref: overlap of danish funds
tag: dkfinance
---

Givet udvalget af Danske investeringsforeninger fra [Sparindex](https://sparindex.dk/) og [Danske Invest](https://www.danskeinvest.dk/w/show_pages.front?p_nId=75), 
kan det være svært at overskue hvor forskellige fundene er.

Som et mål for enshed kan man udregne overlappet mellem to fonde.
Overlappet mellem fond $$A$$ og fond $$B$$ vil blive regnet som:

$$ S_{AB} = \sum_{i} \sqrt{w_{A,i}\cdot w_{B,i}} $$

Her er $$w_{A,i}$$ vægten af aktie $$i$$ i fond $$A$$.
Denne metrik har den egenskab at den er $$1$$ hvis de to fonde er identiske og $$0$$ hvis de to fonde ikke indeholder nogen ens aktier.

## Behandling af data
Dataen for beholdningerne af fondene er hentet direkte fra [Sparindex](https://sparindex.dk/) og [Danske Invest](https://www.danskeinvest.dk/w/show_pages.front?p_nId=75)
Den rå hentede data kan findes her: [danish_funds_assets](https://github.com/erikkjellgren/erikkjellgren.github.io/tree/main/assets/python_scripts/data/danish_funds_assets).

For at to fondes aktiver kan matches skal alle aktiverne gives en unik identifikation, til dette blev Yahoo-Finance tickers valg til at identificere aktiverne.
Dette blev gjort ved simplificere navne i.e. fjerne *LTD*, *A/S*, etc. og søge via. et [Yahoo-Finance query](https://query2.finance.yahoo.com/v1/finance/).
Denne metode har fordelen A- og B-shares vil få tildelt samme ticker, samt at tickers også vil komme fra den samme børs given et specifi.
Herved undgår man at få kunstigt lavt overlap ved at fondene køber aktierne fra forskellige børser.

Scriptet til at hente dataen fra Yahoo-Finance kan findes her: [get_yahoo_tickers.py]({{ site.baseurl }}/assets/python_scripts/get_yahoo_tickers.py)

Aktie navne med tildelte ticker kan findes her: [name2yahooticker.txt]({{ site.baseurl }}/assets/python_scripts/data/name2yahooticker.txt)

For en del af de aktier der ikke kunne tildeles en ticker via. ovenstående methode blev disse tildelt manuelt, listen over disse kan findes her: [manual_added_name2yahooticker.txt]({{ site.baseurl }}/assets/python_scripts/data/manual_added_name2yahooticker.txt)

For de aktie der ikke blev tildelt en ticker kan listen findes her: [notfound_name2yahooticker.txt]({{ site.baseurl }}/assets/python_scripts/data/notfound_name2yahooticker.txt)


## Overlap af fondene

De udregnede overlap af fondene kan ses i nedenstående figur.
Det skal bemærkes at de akkumulerende fonde der har en distribuerende version er ekskluderet fra figuren.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/overlap_of_danish_funds.svg"> 
</p>

I ovenstående figur kan fond-navnene være svære at læse.
Figuren kan ses i stor her: [Overlap Fonde Stor Figur]({{ site.baseurl }}/assets/plots/overlap_of_danish_funds.svg)
Version af figuren der er farveblind venlig kan findes her: [Farveblind Version Stor Figur]({{ site.baseurl }}/assets/plots/overlap_of_danish_funds_colorblind_friendly.svg)

Fondene er "clustered" via [linkage](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html)
Scriptet for figuren kan findes her: [overlap_of_danish_funds.py]({{ site.baseurl }}/assets/python_scripts/overlap_of_danish_funds.py)

Man kan tydelig se den forventede struktur med grupper som Europa, Danmark, Japan og nye markeder. 
Det er værd at bemærke at USA og de globale fonde generelt har meget stort overlap.

Det er også værd at bemærke at Danske Invest har mange fonde der er næsten identiske!
