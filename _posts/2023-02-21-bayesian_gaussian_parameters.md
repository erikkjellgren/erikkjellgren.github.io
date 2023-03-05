---
layout: post
title: Bayesian interference of Gaussian parameters
lang: en
lang-ref: Bayesian interference of Gaussian parameters
tag: computation
---

In a [previous post]({{ site.baseurl }}/2021/11/13/bayesian_drop_chance/) [Bayesian interference](https://en.wikipedia.org/wiki/Bayesian_inference) was used to parameter likelyhood of a [binomial distribution](https://en.wikipedia.org/wiki/Binomial_distribution).
The binomial distribution can be used to describe events with discrete probabilities.
However, a lot of interesting probabilistic events are continuous.
One of the most popular continous probability distributions is the [Gaussian distribution](https://en.wikipedia.org/wiki/Normal_distribution).
The Gaussian distribution is given as:

$$ P(x) = \frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2\right) $$

Again let us start from [Baye's theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem):

$$ P_\mathrm{posterior}(\theta|D) = \frac{P_\mathrm{likelihood}(D|\theta)P_\mathrm{prior}(\theta)}{P_\mathrm{marginal\ likelihood}(D)} $$

For the Gaussian distribution the data is $$D = \{x_i\}$$ and the model parameters are $$\theta = \{\mu,\sigma\}$$.

