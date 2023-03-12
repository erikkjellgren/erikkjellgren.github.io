---
layout: post
title: Benchmark tracking certainty of funds
lang: en
lang-ref: benchmark-tracking-certainty
tag: dkfinance
---

In the decision of which funds to invest in an important parameter is how well the fund can track the benchmark index.
It is to be expected that variance of how well a specific fund can track an index does not go to zero even if we had infinite data.
As a simpel model the tracking of the benchmark could be modeled as [Gaussian distribution](https://en.wikipedia.org/wiki/Normal_distribution).
This gives two free parameters.
The mean value, $$\mu$$, how close the fund tracks the benchmark on average.
And the standard deviation, $$\sigma$$, how much the fund deviates from the benchmark at specific points in time.

The mean and standard devitation has been calculated for specific funds, [see this Reddit post](https://www.reddit.com/r/dkfinance/comments/10m1jm5/danske_invest_vs_sparindex/).
These quantities are very easy to determine (without error bars).
Now let us take this one step further, and give an estimate of the certainty of the mean and standard devitation, to find out if we can actually distinguish the perfermance of these specific funds.

The data from the Reddit post is the following:

| Year | [DKIGI](https://www.danskeinvest.dk/w/show_funds.product?p_nId=75&p_nFundgroup=75&p_nFund=1873) deviations | [SPVIGAKL](https://www.sparinvest.dk/fondsoversigt/dk0060747822/) deviations | [SPIEMIKL](https://www.nordnet.dk/markedet/investeringsforeninger-liste/16102899-sparindex-index-emerging) deviations |
| ---- | ----: | ----: | ----: |
| 2013 | -0.28 | -     | -     |
| 2014 | -0.28 | -     | -0.94 |
| 2015 | -0.52 | -     | -1.34 |
| 2016 | -0.42 | -     |  2.37 |
| 2017 | -0.19 | -     | -0.07 |
| 2018 | -0.20 | -0.54 |  0.16 |
| 2019 | -0.40 |  1.06 |  0.96 |
| 2020 |  0.34 |  1.01 | -2.02 |
| 2021 | -0.11 | -1.17 |  0.27 |
| 2022 | -0.82 | -0.07 |  2.63 |
