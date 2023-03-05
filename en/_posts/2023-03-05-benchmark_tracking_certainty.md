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

The mean and standard devitation has been calculated for specific funds, [see this reddit post](https://www.reddit.com/r/dkfinance/comments/10m1jm5/danske_invest_vs_sparindex/).
These quantities are very easy to determine (without error bars).
Now let us take this one step further, and give an estimate of the certainty of the mean and standard devitation, to find out if we can actually distingues the perfermance of these specific funds.
