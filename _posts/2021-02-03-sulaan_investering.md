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

Koden brugt til at lave graferne kan findes her: [sulaan_investering.py]({{ site.baseurl }}/assets/python_scripts/sulaan_investering.py)
