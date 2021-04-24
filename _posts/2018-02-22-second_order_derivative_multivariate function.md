---
layout: post
title: Second order partial derivative for multivariate function, derivation
---

Consider a function:

$$ f\left(x_{1}\left(\lambda_{1},\lambda_{2},..,\lambda_{M}\right),x_{2}\left(\lambda_{1},\lambda_{2},..,\lambda_{M}\right),..,x_{N}\left(\lambda_{1},\lambda_{2},..,\lambda_{M}\right)\right) $$

The first partial derivative is given as:

$$ \frac{\partial}{\partial\lambda_{i}}f\left(x_{1},x_{2},..,x_{N}\right)=\frac{\partial f}{\partial x_{1}}\frac{\partial x_{1}}{\partial\lambda_{i}}+\frac{\partial f}{\partial x_{2}}\frac{\partial x_{2}}{\partial\lambda_{i}}+...+\frac{\partial f}{\partial x_{N}}\frac{\partial x_{N}}{\partial\lambda_{i}} $$

The above equation can be formulated as:

$$ \frac{\partial}{\partial\lambda_{i}}f\left(x_{1},x_{2},..,x_{N}\right)=\sum_{k}^{N}\frac{\partial f}{\partial x_{k}}\frac{\partial x_{k}}{\partial\lambda_{i}} $$

Now consider the second derivative:

$$ \frac{\partial^{2}}{\partial\lambda_{j}\partial\lambda_{i}}f\left(x_{1},x_{2},..,x_{N}\right)=\frac{\partial}{\partial\lambda_{j}}\left(\frac{\partial f}{\partial x_{1}}\frac{\partial x_{1}}{\partial\lambda_{i}}+\frac{\partial f}{\partial x_{2}}\frac{\partial x_{2}}{\partial\lambda_{i}}+...+\frac{\partial f}{\partial x_{N}}\frac{\partial x_{N}}{\partial\lambda_{i}}\right) $$

This is equal to:

$$ \frac{\partial^{2}}{\partial\lambda_{j}\partial\lambda_{i}}f\left(x_{1},x_{2},..,x_{N}\right)=\frac{\partial}{\partial\lambda_{j}}\left(\frac{\partial f}{\partial x_{1}}\frac{\partial x_{1}}{\partial\lambda_{i}}\right)+\frac{\partial}{\partial\lambda_{j}}\left(\frac{\partial f}{\partial x_{2}}\frac{\partial x_{2}}{\partial\lambda_{i}}\right)+...+\frac{\partial}{\partial\lambda_{j}}\left(\frac{\partial f}{\partial x_{N}}\frac{\partial x_{N}}{\partial\lambda_{i}}\right) $$

Since all of the terms should be treated the same way, lets just focus on the first term.
Lets define $$f_{x_{1}}=\frac{\partial f}{\partial x_{1}}$$ and $$x_{1,\lambda_{i}}=\frac{\partial x_{1}}{\partial\lambda_{i}}$$:

$$ \frac{\partial}{\partial\lambda_{j}}\left(\frac{\partial f}{\partial x_{1}}\frac{\partial x_{1}}{\partial\lambda_{i}}\right)=\frac{\partial}{\partial\lambda_{j}}\left(f_{x_{1}}x_{1,\lambda_{i}}\right) $$

Now by using [the product rule](https://en.wikipedia.org/wiki/Product_rule):

$$ \frac{\partial}{\partial\lambda_{j}}\left(\frac{\partial f}{\partial x_{1}}\frac{\partial x_{1}}{\partial\lambda_{i}}\right)=\frac{\partial f_{x_{1}}}{\partial\lambda_{j}}x_{1,\lambda_{i}}+f_{x_{1}}\frac{\partial x_{1,\lambda_{i}}}{\partial\lambda_{j}} $$

It can be seen that the first term is equal to the first order partial derivative:

$$ \frac{\partial f_{x_{1}}}{\partial\lambda_{j}}=\sum_{l}^{N}\frac{\partial f_{x_{1}}}{\partial x_{l}}\frac{\partial x_{l}}{\partial\lambda_{j}} $$

Thus:

$$ \frac{\partial}{\partial\lambda_{j}}\left(\frac{\partial f}{\partial x_{1}}\frac{\partial x_{1}}{\partial\lambda_{i}}\right)=\sum_{l}^{N}\frac{\partial f_{x_{1}}}{\partial x_{l}}\frac{\partial x_{l}}{\partial\lambda_{j}}x_{1,\lambda_{i}}+f_{x_{1}}\frac{\partial x_{1,\lambda_{i}}}{\partial\lambda_{j}} $$

Now by back-inserting the definitions:

$$ \frac{\partial}{\partial\lambda_{j}}\left(\frac{\partial f}{\partial x_{1}}\frac{\partial x_{1}}{\partial\lambda_{i}}\right)=\sum_{l}^{N}\left[\frac{\partial^{2}f}{\partial x_{l}\partial x_{1}}\frac{\partial x_{l}}{\partial\lambda_{j}}\right]\frac{\partial x_{1}}{\partial\lambda_{i}}+\frac{\partial f}{\partial x_{1}}\frac{\partial^{2}x_{1}}{\partial\lambda_{j}\partial\lambda_{i}} $$

Thus, the final equation for the second order partial derivative for a multivariate function:

$$ \frac{\partial^{2}}{\partial\lambda_{j}\partial\lambda_{i}}f\left(x_{1},x_{2},..,x_{N}\right)=\sum_{k}^{N}\sum_{l}^{N}\left[\frac{\partial^{2}f}{\partial x_{l}\partial x_{k}}\frac{\partial x_{l}}{\partial\lambda_{j}}\right]\frac{\partial x_{k}}{\partial\lambda_{i}}+\sum_{k}^{N}\frac{\partial f}{\partial x_{k}}\frac{\partial^{2}x_{k}}{\partial\lambda_{j}\partial\lambda_{i}} $$
