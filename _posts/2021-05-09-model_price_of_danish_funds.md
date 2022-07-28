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
The historical fund prices have been found through [saxotrader.com](https://www.saxotrader.com/), and as a market representation, the NASDAQ Emerging Markets Index has been used in EURO. All data is from March month, because the ex-dividend date of the funds is in February.

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

The full code used to generate the graphs can be found here: [model_price_of_danish_fund.py]({{ site.baseurl }}/assets/python_scripts/model_price_of_danish_fund.py)
