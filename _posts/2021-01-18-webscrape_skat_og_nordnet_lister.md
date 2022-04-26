---
layout: post
title: Indeks og ÅOP for Nordnet Månedsopsparing og SKATs positiv liste
lang: dk
lang-ref: Indeks-og-ÅOP-for-Nordnet-Månedsopsparing-og-SKATs-positiv-liste
tag: dkfinance
---

*Husk selv at checke op på webscrapede informationer, for at sikre de er rigtige.*

Givet lister som [SKATs positiv liste](https://skat.dk/skat.aspx?oid=2244641)
og [Nordnets månedsopsparing](https://www.nordnet.dk/dk/tjenester/manedsopsparing),
kan det være svært at overskue omkostninger og hvilke indeks de forskellige ETFer følger.

På [https://www.justetf.com/en/](https://www.justetf.com/en/) kan man finde informationer fra en lang liste af ETFer.
Ved at bruge Python kan man webscrape informationer, og kompilere dem i en tabel.

Tabelen for Nordnets månedsopsparing kan findes her:
[Nordnets månedsopsparing ETF liste](https://docs.google.com/spreadsheets/d/1FTxNdAT43Dkcix32ase-R8O1tQDkWkr3hvvkqLLOihY/edit?usp=sharing).

Listen for Nordnets månedsopsparing inkludere alle udenlandske ETF'er der kan findes via. [https://www.justetf.com/en/](https://www.justetf.com/en/).

Tabelen for SKATs positiv liste kan findes her:
[SKATs positiv ETF liste](https://docs.google.com/spreadsheets/d/181WgeIKI_c9z2DpjqcBxXkOwbcPLnrDjRT4JhHY8eB8/edit?usp=sharing).

For listen over ETFer på SKATs positiv liste er det kun ETFer fra Amundi, iShares, JPMorgan, Lyxor og Xtrackers.

Koden der blev brugt til webscraping kan findes her: [webscrape_skat_og_nordnet_lister.py]({{ site.baseurl }}/assets/python_scripts/webscrape_skat_og_nordnet_lister.py)
