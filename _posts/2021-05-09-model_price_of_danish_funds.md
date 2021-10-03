---
layout: post
title: Model for the price of Danish investment funds
lang: en
lang-ref: Model for the price of Danish investment funds
tag: dkfinance
---

In Denmark, all ETFs are taxed yearly by unrealized returns.
On the other hand, some Danish investment funds are taxed by realized gain, if they fulfill some criteria of paid out dividends.

The dividend paid out will be:

* earned dividends
* realized taxable gains

From, [majinvest.dk](https://majinvest.dk/invester-med-maj-invest/ofte-stillede-spoergsmaal/hvordan-udloddes-udbytte/), 2021-05-09.

## Model description

To model this behavior only the price of the fund is relevant, i.e. dividend from the underlying stocks can be ignored, because these dividends have to be paid out.
As a model for realized gain, the turnover rate can be used.
I.e. the difference between some baseline value and the current fund price will be realized by the speed of the turnover rate.
Therefore this will be subtracted from the price since it will be paid out as a dividend.

$$ k_{i}=\left(k_{i-1}-\left(k_{i-1}-b_{i}\right)\cdot T_{i}\right)\cdot R_{i} $$

Here $$R_i$$ is one plus the yearly return, $$T$$ is the turnover rate and $$k$$ is the fund price.
It can be noted that this simple form of the model does not have the exact wanted behavior if $$k_{i-1}<b_{i}$$, but it should still be reasonable.
This can also be written as:

$$ k_{i}=k_{i-1}\cdot\left(R_{i}-T_{i}\cdot R_{i}\right)+b_{i}\cdot T_{i}\cdot R_{i} $$

To model the baseline, three different models can be constructed.
The first being that the base-line is just the initial value of the fund:

$$ b_i=k_0 $$

The second model being the average of the previous prices of the fund:

$$ b_{i}=\frac{1}{i+1}\sum_{j=0}^{i}k_{j} $$

And the third model being a weighted average of the previous fund prices:

$$ b_i=\frac{\left(i+1\right)p}{\sum_{j=0}^{i}\frac{p}{k_{j}}}=\frac{(i+1)}{\sum_{j=0}^{i}k_{j}^{-1}} $$

Where the weighting is such that there is the same amount of inflow to the fund every year.

## Testing the model

To test the fitness of the model let us first consider two funds that track the same market, [Danske Invest, Nye Markeder, klasse DKK d](https://www.danskeinvest.dk/w/show_funds.product?p_nId=75&p_nFundgroup=75&p_nFund=1019) and [Sparinvest, INDEX Emerging Markets](https://www.sparinvestindex.dk/afdelinger/alle%20afdelinger/index%20emerging%20markets.aspx).
This is an interesting case because even tho they target the same market, Danske Invest has been falling in price (but with huge dividends) and Sparinvest has increased in price.
The historical fund prices have been found through [saxotrader.com](saxotrader.com), and as a market representation, the NASDAQ Emerging Markets Index has been used in EURO. All data is from March month, because the ex-dividend date of the funds is in February.

For the Sparinvest fund the result is:

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/sparinvest_em.svg">
</p>

and for the Danske Invest,

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/danskeinvest_em.svg">
</p>

For both funds the ongoing costs have been subtracted from the return of the NASDAQ Emerging Markets, the baseline for model 1 (b_case=1) was picked to be 100 and the turnover rate was picked to be 0.09.

Clearly, none of the models gives a perfect match, but it is very notable that even tho both funds have the same underlying return, the model qualitatively predicts the rising price of Sparinvest and the falling price of Danske Invest.
Model 1 (b_case=1) seems to be best overall.

As another test let us consider [Sparinvest, INDEX USA Growth](https://www.sparinvest.dk/afdelinger/indeks/index%20usa%20growth.aspx), again with prices taking from Saxo, but this time using NASDAQ-100 as the underlying index in EURO.
Given this is a growth ETF a turnover rate of 0.25 will be used.
This gives:

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/sparinvest_growth.svg">
</p>

Here the baseline for model 1 was picked to be 65, given the price at inception.
Again the model is in very good line with the actual price and model 1 is the superior model.

## Predictions of model 1 for equal yearly return

Now that model 1 has been found the be fairly accurate and the best of the three models, let us examine it in a bit more detail.

If we assume the same return every year, then after one year the price of the fund will be:

$$ k_{1} = k_{0}\cdot\left(R-T\cdot R\right)+b\cdot T\cdot R $$

After two years it will be:

$$\begin{eqnarray}
k_{2} &=& k_{1}\cdot\left(R-T\cdot R\right)+b\cdot T\cdot R \\
 &=& \left(k_{0}\cdot\left(R-T\cdot R\right)+b\cdot T\cdot R\right)\cdot\left(R-T\cdot R\right)+b\cdot T\cdot R \\
 &=& k_{0}\cdot\left(R-T\cdot R\right)^{2}+b\cdot T\cdot R\cdot\left(R-T\cdot R\right)+b\cdot T\cdot R
\end{eqnarray}$$

And after three years:

$$\begin{eqnarray}
k_{3} &=& k_{2}\cdot\left(R-T\cdot R\right)+b\cdot T\cdot R \\
 &=& \left(k_{0}\cdot\left(R-T\cdot R\right)^{2}+b\cdot T\cdot R\cdot\left(R-T\cdot R\right)+b\cdot T\cdot R\right)\cdot\left(R-T\cdot R\right)+b\cdot T\cdot R \\
 &=& k_{0}\cdot\left(R-T\cdot R\right)^{3}+b\cdot T\cdot R\cdot\left(R-T\cdot R\right)^{2}+b\cdot T\cdot R\cdot\left(R-T\cdot R\right)+b\cdot T\cdot R
\end{eqnarray}$$

It can now be seen that the general expression will be:

$$ k_N = k_{0}\cdot\left(R-T\cdot R\right)^{N}+b\cdot T\cdot R\cdot\sum_{i=0}^{N-1}\left(R-T\cdot R\right)^{i} $$

and by using the definition of model 1, $$b_i = k_0$$:

$$ k_N = k_{0}\cdot\left(\left(R-T\cdot R\right)^{N}+T\cdot R\cdot\sum_{i=0}^{N-1}\left(R-T\cdot R\right)^{i}\right) \label{model1}\tag{1} $$

Now let us examine how this model behaves:

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/model1_behaviour.svg">
</p>

In the above, a yearly return of 7% is assumed.

It can be seen that two different regions seem to exist, a region of faster and faster growth of the fund price, and a region of stagnating growth of the fund price.
From the expression of the fund price arising from model 1 it can be seen that:

$$ R-T\cdot R = 1 $$

or,

$$ T = 1 - \frac{1}{R} $$

might be a special case.
Inserting this into the Eq. (\ref{model1}) we find,

$$\begin{eqnarray}
\left.k_{N}\right|_{T=1-1/R} &=& k_{0}\cdot\left(1^{N}+\left(1-\frac{1}{R}\right)\cdot R\cdot\sum_{i=0}^{N-1}1^{i}\right) \\
 &=& k_{0}\cdot\left(1+\left(R-\frac{R}{R}\right)\cdot N\right) \\
 &=& k_{0}\cdot\left(1+R\cdot N-N\right) \\
 &=& k_{0}\cdot\left(R-1\right)\cdot N+k_{0}
\end{eqnarray}$$

Thus it can be seen that at this point the fund price is linear in time instead of exponential.
Now below this point, and by letting time go to inifity we find that:

$$\begin{eqnarray}
\lim_{N\rightarrow\infty}\left.k_{N}\right|_{T>1-1/R} &=& \lim_{N\rightarrow\infty}k_{0}\cdot\left(\left(R-T\cdot R\right)^{N}+T\cdot R\cdot\sum_{i=0}^{N-1}\left(R-T\cdot R\right)^{i}\right) \\
 &=& k_{0}\cdot T\cdot R\cdot\lim_{N\rightarrow\infty}\sum_{i=0}^{N-1}\left(R-T\cdot R\right)^{i}
\end{eqnarray}$$

And by using the [geometric series](https://en.wikipedia.org/wiki/Geometric_series):

$$ \lim_{N\rightarrow\infty}\sum_{i=0}^{N-1}\left(R-T\cdot R\right)^{i}=\frac{1}{1-R+T\cdot R} $$

Thus:

$$ \lim_{N\rightarrow\infty}\left.k_{N}\right|_{T>1-1/R}=\frac{k_{0}\cdot T\cdot R}{1-R+T\cdot R} $$

This means that if the turnover rate is below $$1-1/R$$ then the price of the fund will on average never go over a fixed value!
I.e. there is an upper limit to how much of the returns will be taxed as realized gain, and the rest will just be paid out as dividends.

<!-- python_split -->

## Python details

Importing was is needed.

{% highlight python %}
from typing import List

import matplotlib.pyplot as plt
import numpy as np
{% endhighlight %}

Making a function for the model.

{% highlight python %}
def fund_price(T: float, r: np.array, ks: List[float], b_case: int, k0: float = 100) -> np.ndarray:
    """Calculates the fund price of a Danish investment fund.

    Args:
      T: Turnover rate.
      r: List of yearly returns, in decimal notation, i.e. 0.07 for 7%.
      ks: Previous fund prices.
      b_case: base-line price model.
              1, is a fixed base price.
              2, is an average base price.
              3, is a price-weighted average price.
      k0: base-line price (only relevant for b_case = 1).

    Returns:
      Estimate of fund price.
    """
    r = np.array(r)
    R = 1 + r
    N = len(r)
    k_out = [ks[-1]]
    for i in range(N):
        if b_case == 1:
            b = k0
        elif b_case == 2:
            b = np.mean(ks)
        elif b_case == 3:
            b = len(ks) / np.sum(1 / np.array(ks))
        k_new = k_out[i] * (R[i] - T * R[i]) + b * T * R[i]
        k_out.append(k_new)
        ks.append(k_new)
    return np.array(k_out)
{% endhighlight %}

Making the plots.

{% highlight python %}
sparindex = np.array([100.5, 90.45, 115.2, 94.95, 116.10, 122.3, 126.45, 114.75, 151.55])
danskeinv = np.array([342, 288.5, 338.1, 263.2, 254.5, 226.4, 213.4, 162.1, 242.2])
# Last element in "old" is the first element in the above lists.
sparindex_old = np.array([100, 96.85, 100.5])
danskeinv_old = np.array([100, 135, 95.7, 135.5, 160.0, 251.8, 254, 225.6, 146.6, 277.8, 316.8, 332, 342])
EM = np.array([1056.59, 970.26, 993.1, 826.63, 978.22, 1212.95, 1096.36, 1052.68, 1320.98])
USDEURO = np.array([0.77, 0.72, 0.95, 0.91, 0.94, 0.80, 0.88, 0.89, 0.83])
EM = EM * USDEURO
EMp = (EM[1:] - EM[:-1]) / EM[:-1]

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

spar_m1 = fund_price(0.09, EMp - 0.5 / 100, [sparindex[0]], 1)
spar_m2 = fund_price(0.09, EMp - 0.5 / 100, sparindex_old.tolist(), 2)
spar_m3 = fund_price(0.09, EMp - 0.5 / 100, sparindex_old.tolist(), 3)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(spar_m1, "-o", linewidth=2, label="b_case=1")
ax1.plot(spar_m2, "-o", linewidth=2, label="b_case=2")
ax1.plot(spar_m3, "-o", linewidth=2, label="b_case=3")
ax1.plot(sparindex, "-o", linewidth=2, label="Acutal")
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("Fund price [DKK]")
ax1.set_xlabel("Year")
ax1.set_xticks(range(9))
ax1.set_xticklabels([2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
ax1.set_title("Sparinvest, INDEX Emerging Markets KL")
for tick in ax1.get_xticklabels():
    tick.set_rotation(45)
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("sparinvest_em.svg")

danske_m1 = fund_price(0.09, EMp - 1.63 / 100, [danskeinv[0]], 1)
danske_m2 = fund_price(0.09, EMp - 1.63 / 100, danskeinv_old.tolist(), 2)
danske_m3 = fund_price(0.09, EMp - 1.63 / 100, danskeinv_old.tolist(), 3)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(danske_m1, "-o", linewidth=2, label="b_case=1")
ax1.plot(danske_m2, "-o", linewidth=2, label="b_case=2")
ax1.plot(danske_m3, "-o", linewidth=2, label="b_case=3")
ax1.plot(danskeinv, "-o", linewidth=2, label="Acutal")
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("Fund price [DKK]")
ax1.set_xlabel("Year")
ax1.set_xticks(range(9))
ax1.set_xticklabels([2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
ax1.set_title("Danske Invest, Nye Markeder, klasse DKK d")
for tick in ax1.get_xticklabels():
    tick.set_rotation(45)
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("danskeinvest_em.svg")

spar_growth = np.array(
    [67.8, 59.3, 42.3, 60.5, 66, 77.15, 87.75, 100.6, 153.4, 134.6, 106.4, 97.65, 122.8, 134.3, 166.65]
)
USDEURO_long = np.array(
    [0.76, 0.64, 0.77, 0.73, 0.71, 0.76, 0.77, 0.72, 0.95, 0.91, 0.94, 0.80, 0.88, 0.89, 0.83]
)
nasdaq = np.array(
    [
        1726.03,
        1707.5,
        1064.7,
        1888.56,
        2359.96,
        2646.85,
        2804.11,
        3662.6,
        4399.23,
        4351.83,
        5373.48,
        6811.04,
        7015.69,
        8530.34,
        12668.51,
    ]
)
nasdaq = nasdaq * USDEURO_long
nasdaqp = (nasdaq[1:] - nasdaq[:-1]) / nasdaq[:-1]

spar_m1 = fund_price(0.25, nasdaqp - 0.5 / 100, [spar_growth[0]], 1, k0=65)
spar_m2 = fund_price(0.25, nasdaqp - 0.5 / 100, [spar_growth[0]], 2)
spar_m3 = fund_price(0.25, nasdaqp - 0.5 / 100, [spar_growth[0]], 3)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(spar_m1, "-o", linewidth=2, label="b_case=1")
ax1.plot(spar_m2, "-o", linewidth=2, label="b_case=2")
ax1.plot(spar_m3, "-o", linewidth=2, label="b_case=3")
ax1.plot(spar_growth, "-o", linewidth=2, label="Acutal")
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("Fund price [DKK]")
ax1.set_xlabel("Year")
ax1.set_xticks(range(15))
ax1.set_xticklabels(
    [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
)
ax1.set_title("Sparinvest, INDEX USA Growth KL")
for tick in ax1.get_xticklabels():
    tick.set_rotation(45)
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("sparinvest_growth.svg")

fig, ax1 = plt.subplots(1, 1, figsize=(6, 5))
Ts = np.linspace(0, 0.2, 9)
for t in Ts:
    ax1.plot(fund_price(t, [0.07] * 10, [100], 1), linewidth=3, label=f"T={t:2.2f}")
ax1.plot(fund_price(1 - 1 / 1.07, [0.07] * 10, [100], 1), linewidth=3, label=f"T={1-1/1.07:2.2f}")
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("Fund price [DKK]")
ax1.set_xlabel("Year")
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("model1_behaviour.svg")
{% endhighlight %}

The full code can be found here: [model_price_of_danish_fund.py]({{ site.baseurl }}/assets/model_price_of_danish_fund.py)
