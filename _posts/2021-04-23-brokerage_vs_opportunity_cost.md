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

<!-- python_split -->

## Python details

Importing was is needed.

{% highlight python %}
import matplotlib.pyplot as plt
import numpy as np
{% endhighlight %}

Defining the function for investment frequency in months.

{% highlight python %}
def N_opt(k: float, r_m: float, p: float) -> float:
    """Calculates the number of months between each investment.

    Args:
      k: capital.
      r_m: monthly return.
      p: brokerage as fixed value.

    Returns:
      Montly frequency.
    """
    return np.ceil((p + p / r_m) / k)
{% endhighlight %}

Defining the function for minimum capital for a given expected return.

{% highlight python %}
def k_min(r_m: float, p: float) -> float:
    """Calculates minimum required capital 
    for return to outweigh brokerage.

    Args:
      k: capital.
      p: brokerage as fixed value.

    Returns:
      Minimum capital.
    """

    return p + p / r_m
{% endhighlight %}

Making the plots.

{% highlight python %}
plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))

ks = np.linspace(65, 540, 10000)
N5 = np.zeros(len(ks))
N7 = np.zeros(len(ks))
N9 = np.zeros(len(ks))
for j, k_ in enumerate(ks):
    N5[j] = N_opt(k_, (1 + 0.05) ** (1 / 12) - 1, 2)
    N7[j] = N_opt(k_, (1 + 0.07) ** (1 / 12) - 1, 2)
    N9[j] = N_opt(k_, (1 + 0.09) ** (1 / 12) - 1, 2)
ax1.plot(ks, N9, label="CAGR = 9%", linewidth=3)
ax1.plot(ks, N7, label="CAGR = 7%", linewidth=3)
ax1.plot(ks, N5, label="CAGR = 5%", linewidth=3)

ax1.set_xlabel("Monthly capital, Euro")
ax1.set_ylabel(r"$N_\mathrm{opt}$, months")
ax1.legend()
ax1.grid(which="minor")
ax1.grid(which="major")

plt.tight_layout()
plt.savefig("brokerage_vs_oppertunity_cost.svg")


fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))

r_y = np.linspace(0.02, 0.2, 10000)
r = (1 + r_y) ** (1 / 12) - 1
ax1.plot(r_y * 100, k_min(r, 2), linewidth=3)

ax1.set_ylabel("Minimum capitial, Euro")
ax1.set_xlabel(r"CAGR, %")
ax1.grid(which="minor")
ax1.grid(which="major")

plt.tight_layout()
plt.savefig("capital_vs_return.svg")
{% endhighlight %}

The full code can be found here: [brokerage_vs_opportunity_cost.py]({{ site.baseurl }}/assets/python_scripts/brokerage_vs_opportunity_cost.py)
