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

The results from the model kan be seen in the graph below.
Note that the results are based on an average of the Danish market.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/huspris_indekser_en.svg">
</p>

It can immediately be seen that the housing prices has increased by a significant amount since 1994.
However, the house purchase costs index follows the wage index much more close over the periode, except during the housing bouble around 2007.
The model thus captures that the housing prices were elevated in that periode.

The difference between the house purchase costs index and the house price index kan be interpreted to be driven by falling interest rates.
In this interpretation it can be expected that the housing prices will deaccelerate, since the interest rates are so low they cannot be expected to fall further.

If the interest rates can be expected to stay close to zero for a prolonged periode, then the model suggests that the housing prices are not in a bouble but will just stay at the current levels.

It should be remembered that a hidden but very important assumption in the model is that everything is corretly prices in Q1 1994.
This assumption is very hard to circumvent.

So far the effect of geographical differences on the housing prices has not been considered.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/geografiske_forskelle_en.svg">
</p>

As can clearly be seen the geographical location has a huge impact on the development of the housing prices.
Areas such as Lolland and Langeland, remoate areas of Denmark, has completely stagnating housing prices.
Whereas, the capital Copenhagen has had exploding housing prices.

A possible explination of this could be urbanisation.
If this hypothesis can be substantiated by data is out-of-scope for this analysis.

One thing to note, is that three largest cities after Copenhagen (Aarhus, Aalbrog and Odense), are all around the nation average.
This can be interpreted in two ways.
Firstly, mainly Copenhagen that is subjected to the positive side of the urbanisation-effect.
Secondly, the housing prices in Copenhagen are in a bouble.
These two different interpretations cannot be differentiated by the presented model in this post.

In the model the effect of interest rates are handled explicitly.
As a final discussion point let us look at how sensitive the housing prices are to the interest rates accourding to the presented model.

By starting from equation (\ref{eq1}) it can be seen that the housing prices depends on the interest rates in the following way:

$$ k_{\mathrm{housing\ price}}=k_{\mathrm{total\ costs}}\left(0.8\cdot \frac{r\cdot n}{1-\left(1+r\right)^{-n}}+0.2\right)^{-1} $$

This can now be graphed:

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/huspris_rente_funktion_en.svg">
</p>

In the above figure the housing prices dependence on the interest rate can be seen.
This is then normalised to unity at an interest rate of zero percentage.

It can be seen if the interest rate increased "permantly" to 2% (from 0%) then the housing prices will fall ~20%, and if the interest increase "permantly" 4% then the housing prices will fall ~35%.

The code used to make the graphs can be found here: [huspriser_en.py]({{ site.baseurl }}/assets/python_scripts/huspriser_en.py)
