---
layout: post
title: Indeks og ÅOP for Nordnet Månedsopsparing og SKATs positiv liste
---

*Husk selv at checke op på webscrapede informationer, for at sikre de er rigtige.*

Givet lister som [SKATs positiv liste](https://skat.dk/skat.aspx?oid=2244641)
og [Nordnets månedsopsparing](https://www.nordnet.dk/dk/tjenester/manedsopsparing),
kan det være svært at overskue omkostninger og hvilke indeks de forskellige ETFer følger.

På https://www.justetf.com/en/ kan man finde informationer fra en lang liste af ETFer.
Ved at bruge Python kan man webscrape informationer, og kompilere dem i en tabel.

Tabelen for Nordnets månedsopsparing kan findes her:
[Nordnets månedsopsparing ETF liste](https://docs.google.com/spreadsheets/d/1FTxNdAT43Dkcix32ase-R8O1tQDkWkr3hvvkqLLOihY/edit?usp=sharing).

Listen for Nordnets månedsopsparing inkludere alle udenlandske ETFer med undtagelse af WisdomTree Brent Crude Oil (ISIN: DE000A1N49P6) og WisdomTree WTI Crude Oil (ISIN: DE000A0KRJX4).

Tabelen for SKATs positiv liste kan findes her:
[SKATs positiv ETF liste](https://docs.google.com/spreadsheets/d/181WgeIKI_c9z2DpjqcBxXkOwbcPLnrDjRT4JhHY8eB8/edit?usp=sharing).

For listen over ETFer på SKATs positiv liste er det kun ETFer fra Amundi, iShares, JPMorgan, Lyxor og Xtrackers.


<!-- python_split -->

## Python detaljer

Starter med at importere alle de moduler der skal bruges:
dkfinance_modeller er fra, [dkfinance_modeller](https://github.com/erikkjellgren/dkfinance_modeller)

{% highlight python %}
import dkfinance_modeller.utility.webscrape as webscrape
{% endhighlight %}

Webscraping fra SKATs positiv liste:

{% highlight python %}
f = open("data/template_skat_positiv_liste.csv", "r")
isiner = []
for i, line in enumerate(f):
    if i == 0:
        continue
    isiner.append(line.strip("\n"))
f.close()
out = open("skat_positiv_liste_info.csv", "w")
out.write("ISIN;Navn;Index;ÅOP;Replication;Domicil\n")
infoer = webscrape.få_etf_info(isiner, 4)
for info in infoer:
    if info["succes"]:
        out.write(
            f"{info['isin']};{info['navn']};{info['indeks']};"
            f"{info['åop']};{info['replication']};{info['domicile']}\n"
        )
out.close()
{% endhighlight %}

Webscraping fra Nordnets månedsopsparing:

{% highlight python %}
f = open("data/template_nordnet_liste.csv", "r")
isiner = []
skat = {}
for i, line in enumerate(f):
    if i == 0:
        continue
    isiner.append(line.strip("\n").split(";")[1])
    skat[line.strip("\n").split(";")[1]] = line.strip("\n").split(";")[0]
f.close()
out = open("nordnet_liste_info.csv", "w")
out.write("ISIN;Navn;Index;ÅOP;Replication;Domicil;Beskatning\n")
infoer = webscrape.få_etf_info(isiner, 4)
for info in infoer:
    if info["succes"]:
        out.write(
            f"{info['isin']};{info['navn']};{info['indeks']};"
            f"{info['åop']};{info['replication']};{info['domicile']};{skat[str(info['isin'])]}\n"
        )
out.close()
{% endhighlight %}

Den fulde kode kan findes her: [webscrape_skat_og_nordnet_lister.py]({{ site.baseurl }}/assets/python_scripts/webscrape_skat_og_nordnet_lister.py)