---
layout: post
title: UK Premium Bonds, 'Expected' Return
lang: en
lang-ref: uk-premium-bonds-expected-return
tag: dkfinance
---

In the United Kingdom investors can invest in a class of bonds known as premium bonds.
Premium bonds does not have a fixed coupon-rate, but yield is instead distributed via. lottery.

The prizes distributed as of [May 2022](https://www.nsandi.com/get-to-know-us/monthly-prize-allocation) are:

| Prize value | Number of prizes |
|-------------|------------------|
| 1,000,000£  | 2                |
| 100,000£    | 6                |
| 50,000£     | 11               |
| 25,000£     | 24               |
| 10,000£     | 58               |
| 5000£       | 116              |
| 1000£       | 1963             |
| 500£        | 5889             |
| 100£        | 31,907           |
| 50£         | 31,907           |
| 25£         | 3,343,185        |

The [odds of getting a prize](https://www.nsandi.com/products/premium-bonds) is 1 in 24500.
This combined with the above table gives an estimate of a total amount of 1£ premium bonds being ~8,366,9166,000.

The expected annual return can be calculated as:

$$\langle r\rangle = 12\cdot\sum_{i} \frac{\#\mathrm{prize}_i\cdot \mathrm{prize}_i}{\mathrm{total\_bonds}}$$

Note that the factor 12, is because prizes are distributed every month, twelwe months a year.
This gives the expected return of $$\langle r\rangle = 1.41\%$$.

However, given the probabilitic nature of the return, and the slim posibility of extreme rewards, what can most investor expect from premium bonds.

The expected return for most investors can be investigated via. simulation.
There is two very relevant parameters, the time-frame and the amount invested in premium bonds.
To lower the dimensionality of the problem, lets arbitrarily set the time-frame to a decade.
Ten different amounts 25£, 59£, 136£, 315£, 733£, 1706£, 3969£, 9235£, 21488£, and 50000£ are chosen.
These amounts are logarithmically distributed between the minimum of 25£ and the maximum of 50000£.
For every amount 100000 simulations of getting return of a decade is performed.
Note, in simulation the probabilities are erroneously generated with replacement, however, this is expected to have a miniscule effect on the results.

The annualized return of the calculations is calculated as:

$$r=\frac{\frac{\mathrm{capital}_\mathrm{end}}{\mathrm{capital}_\mathrm{start}}-1}{\mathrm{years}}$$

It is calculated by simply dividing by the number of years, instead of using the equation for [compound annual growth rate](https://en.wikipedia.org/wiki/Compound_annual_growth_rate), because the payout is reinvested into premium bonds.

This yields the following graph of returns:

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/simulated_premium_bonds_return.svg">
</p>

In the above graph, the circles denotes the median value, and the whiskers covers the fractile between 2.5% to 97.5%, thus covering the most likely 95% cases.
The unsmoothness of the graph is mainly due to a limited amount of simulations, only 100000 per amount.

Paying attention to the low-end of the graph it can be seen that for most people investing less than 150£ will yield a return of 0%, even over a decade.
But for those that are 'lucky' the return in percentage will be huge.

Now looking at the high-end of the graph, it can immediatly be seen that the spread narrows as the amount invested is increased.
Qualitativly it looks like return converges towards the expected return of 1.41%.
But even after a decade with 50000£ invested the median return is 1.33%, and the 95% likelihood is [1.07%, 1.60%].
Most investors can 'expect' to get a lower return that the expectation value.

It can be noted that over the entire graph, the median return is lower than the expectation value for the return.
The expectation value seems to be an upper-bound to the median return.

Why the median return will always (for time-frames relevant to humans) be lower than the expectation value, lets consider how the different prize-pools contribute to the expected return.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/premium_bonds_return_breakdown.svg">
</p>

In the above graph the contribution to the expected return for the different prize-pools can be seen.
It can immediately be seen that the larger prizes has a non-vanishing contribution to the overall expected return.
For the median investor, these prize pools will never be cashed out, thus leading to the lowering of the median return compared to the expected return.

To get an idea of how unlikely the different prize pools are to get payed out to a specific individual (in aggregate the large prize pools has a 100% probability of being payed out), letus calculate the probability of never getting a specific prize over a decade periode with 50000£ invested.
This can be calculated as:

$$P=\left(1-\frac{\#\mathrm{prizes}}{\mathrm{total\_bonds}}\right)^{12\cdot 10\cdot 50000}$$

This will give the following graph for all of the different prizes.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/premium_bonds_prize_likelihood.svg">
</p>

The above graph shows the probability of never receiving a specifc prize of a decade periode with 50000£ invested.
It can immediatly be seen that all prizes from 5000£ and above are very unikely to get.

The 'expected' return of premium bonds using only the prizes between and including 25£ and 1000£ is 1.34%, this is very close to the median return from the simulations of 1.33%.
This explains why for finite periodes of time the median return is noticably lower than than the expected return, for structures such as premium bonds.

The full code used to do the simulation and generate the plots can be found here: [premium_bonds.py]({{ site.baseurl }}/assets/python_scripts/premium_bonds.py)

Note, the code might take a couple of hours to run.
