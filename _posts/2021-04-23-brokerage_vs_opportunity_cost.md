---
layout: post
title: Brokerage vs. oppertunity cost
lang: en
lang-ref: Brokerage-vs.-oppertunity-cost
tag: dkfinance
---

Many brokers (at least in Denmark), have a pricing model of $$q\%$$ of the trading amount or minimum $$q$$ Euro.
Given a fixed amount to invest every month, we might think it is best to accumulate the cash to reach the minimum brokerage of $$q\%$$.
But then we lose the [oppertunity cost](https://en.wikipedia.org/wiki/Opportunity_cost), let us try to find the point where brokerage outweighs opportunity cost.

Given an available capital $$k$$, then after brokerage we have $$k_\mathrm{eff}$$ to spend.
I.e. our total capital is the effective capital plus the brokerage:

$$\begin{eqnarray}
k &=& k_{\mathrm{eff}}+\max\left(p,q\cdot k_{\mathrm{eff}}\right) \\
  &=& k_{\mathrm{eff}}+\begin{cases}
                        p & \mathrm{if}\,p>q\cdot k_{\mathrm{eff}}\\
                        q\cdot k_{\mathrm{eff}} & \mathrm{else}
                        \end{cases}
\end{eqnarray}$$

In the second case the brokerage is a percentage of the invested capital, and waiting for a period of time to make a larger investment will therefore not decrease the brokerage.
This case can now be ignored.

Now the effective capital can be found from the first case:

$$\begin{eqnarray}
k &=& k_{\mathrm{eff}}+p \\
k_{\mathrm{eff}} &=& k-p
\end{eqnarray}$$

Assuming that $$p>q\cdot k_{\mathrm{eff}}$$ will be true, then the brokerage for all prior months we have accumulated capital will be effectively zero since the brokerage will be constant, i.e. the brokerage for the current month is the same whether we accumulated capital or not.
Investing now instead of accumulating capital to reduce brokerage, will therefore only make sense if the expected return for one month is larger than that of the brokerage:

$$\begin{eqnarray}
\left(k-p\right)\cdot r_{m} &>& p \\
k\cdot r_{m}-p\cdot r_{m} &>& p \\
k\cdot r_{m} &>& p+p\cdot r_{m} \\
k &>& p+\frac{p}{r_{m}}
\end{eqnarray}$$

I.e. the oppertunity cost outweighs the brokerage if our capital is larger than $$p+\frac{p}{r_{m}}$$, assuming that $$p>q\cdot k_{\mathrm{eff}}$$.
In the above $$r_m$$ is the monthly return and is related to the yearly return by: $$r_m = \left(1+r_y\right)^{1/12} - 1$$.

In condition $$p>q\cdot k_{\mathrm{eff}}$$, there is $$k_{\mathrm{eff}}$$, this can be transformed to depend on $$k$$ only by setting case one larger than case two, and substituing in $$k_{\mathrm{eff}} = k-p$$:

$$\begin{eqnarray}
q\cdot\left(k-p\right) &<& p \\
q\cdot k &<& p+q\cdot p \\
k &<& p+\frac{p}{q}
\end{eqnarray}$$

If the above inequality is false, then brokerage cannot be reduced by waiting.

The optimal frequency of investing (assuming monthly) can now found:

$$N_\mathrm{opt} = \left\lceil\frac{p+\frac{p}{r_{m}}}{k}\right\rceil$$

Here the special brackets specify rounding up to nearest integer.
Now let us graph the results for different expected returns and $$p=2$$ Euro.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/brokerage_vs_oppertunity_cost.svg">
</p>

In the above figure, CAGR is [compound annual growth rate](https://en.wikipedia.org/wiki/Compound_annual_growth_rate), i.e. the expected yearly return.

Alternatively, the capital needed for the return to outweigh the brokerage can be graphed, as a function of the expected monthly return:

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/capital_vs_return.svg">
</p>

In the above graph the minimum capital required for the monthly return to outweigh the brokage can be seen, for any given exepcted yearly return.

The code used to make the graphs can be found here: [brokerage_vs_opportunity_cost.py]({{ site.baseurl }}/assets/python_scripts/brokerage_vs_opportunity_cost.py)
