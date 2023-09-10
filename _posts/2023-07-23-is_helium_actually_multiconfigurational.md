---
layout: post
title: Is helium actually multi-configurational?
lang: en
lang-ref: Is helium actually multi-configurational?
tag: quantum
---

This post is inspired by a [paper](https://pubs.acs.org/doi/full/10.1021/acs.jpca.1c00397) by [Ali Alavi](https://scholar.google.com/citations?hl=en&user=gBDKS3UAAAAJ&view_op=list_works&sortby=pubdate) and a talk by [Frank Neese](https://scholar.google.com/citations?hl=en&user=HEyKeR4AAAAJ&view_op=list_works&sortby=pubdate) at [ICQC 2023](https://icqc2023.org/).

The goal of the work by Frank Neese and Ali Alavi is to be able to describe a wave function with as few as possible [configuration state functions](https://en.wikipedia.org/wiki/Configuration_state_function) (CSF).
If a wave function is very well described by a few CFSs, then it is calculationally very cheaper than doing the full [configuration interaction](https://en.wikipedia.org/wiki/Configuration_interaction) (CI) expansion.

Instead of trying to minimize the multi-configurationality of a molecule, let us instead try to maximize it in order to try to build some intuition of what it means for a molecule to be multi-configurational.

# Atomic Helium

To keep things very simple let us consider the helium atom in the 6-31G basis, this is two electrons in two spatial orbitals.
In CSF basis the full CI expansion will be:

$$ \left|\Psi^\mathrm{FCI}\right> = c_0\left|1100\right> + \frac{c_1}{\sqrt{2}}\left(\left|1001\right>-\left|0110\right>\right) + c_2\left|0011\right> $$

Since we are doing a full CI expansion all of our orbital parameters are redundant, meaning they cannot be lowered to change the electronic energy.
But let us anyway introduce the orbital rotation parameterization:

$$ \left|\Psi_0\right> = \exp\left(-\boldsymbol{\kappa}\right)\left|\Psi^\mathrm{FCI}\right> $$

with $$\boldsymbol{\kappa}$$ being the orbital rotation parameter matrix.
For a very detailed explanation of this parameterization see [Molecular Electronic-Structure Theory](https://onlinelibrary.wiley.com/doi/book/10.1002/9781119019572) chapter 3.

For our particular system (helium in 6-31G) the orbital rotation matrix takes the form:

$$ \boldsymbol{\kappa} = \begin{pmatrix}
0 & \kappa\\
-\kappa & 0
\end{pmatrix} $$

thus, there is only a single orbital rotation parameter ($$\kappa$$) to vary.
The orbital coefficients now take the form:

$$ \boldsymbol{C}\left(\kappa\right) = \boldsymbol{S}^{-1/2}\exp\left(-\boldsymbol{\kappa}\right) $$

where $$\boldsymbol{S}$$ is the overlap matrix in atomic orbital basis.
Other choices could have been made, but the starting point does not matter if we do an investigation of the entire range of $$\kappa$$.

Let us now consider $$\kappa$$ between zero and $$\pi$$, and see how this affects the CI coefficients.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/he_mc_vs_kappa.svg">
</p>

In the above graph, the optimal CI coefficients can be seen as a function of the orbital rotation parameter.
The orbital rotation parameter that is the Hartree-Fock molecular orbitals has been marked with a stripped line.

In Hartree-Fock we only consider the CSF $$\left|1100\right>$$,
so it is not surprising that the Hartree-Fock molecular orbitals are at the maximum value for the CI coefficient for this particular CSF.

A much more interesting point is $$\kappa\approx 1.6$$.
Here we can see all of the CSFs have a significant contribution to the overall wave function.
Thus, we can conclude for this particular set of orbitals **helium is indeed multi-configurational**.

After this dishonest conclusion, let us consider a measurement of the optimal orbitals.
Here the optimal orbitals are those that let the wave function be described by as few as possible CFSs.

In the CI expansion, the coefficients have the constraint that,

$$ \sum_i c_i^2 = 1 $$

we can thus interpret the CI coefficients squared as a probability.
A measure of the complexity of the system, or multi-configurationality of the system could be the [Shannon entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)):

$$ H = \sum_i p_i\log\left(p_i\right) = \sum_i c_i^2\log\left(c_i^2\right) $$

here the last equality is from the interpretation of the CI coefficients squared being probabilities.
It should be noted that $$ H=0 $$ if a CSF has a coefficient of one, and that $$H$$ is maximized when all the coefficients have equal value.

Now let us calculate the entropy as a function of the orbital rotation parameter.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/he_entropy_vs_kappa.svg">
</p>

On the above graph, the entropy as a function of the orbital rotation parameter can be seen.
Just as expected the entropy goes close to zero at the Hartree-Fock solution as goes high where there is a mix of CSFs.
It could be tempting to conclude now that Hartree-Fock orbitals are great for minimizing the entropy, however, this is only true if the Hartree-Fock CFS is the dominant one in the CI expansion.

# Molecular Hydrogen

Now let us consider another, slightly more interesting, two electrons in two spatial orbital systems.
Namely, the hydrogen molecule in the STO-3G basis.

Because this is still two electrons in two spatial orbitals the full CI expansion is exactly the same as for the helium atom.

For the hydrogen molecule, there is a single bond.
Let us see what happens to the entropy as this bond length is varied.
The entropy is a function of the orbitals, so let us find the lowest possible entropy for a range of bond lengths.
I.e. determining,

$$ H^\mathrm{opt}\left(r_\text{H-H}\right) = \min_{\kappa}H\left(\kappa, r_\text{H-H}\right) = \min_{\kappa}\sum_i c_i\left(\kappa, r_\text{H-H}\right)^2\log\left(c_i\left(\kappa, r_\text{H-H}\right)^2\right) $$

Now let us calculate the minimal entropy as a function of the hydrogen-hydrogen bond length.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/h2_mc_scan.svg">
</p>

On the above graph, the minimum entropy (blue curve) can be seen for a range of hydrogen-hydrogen bond lengths.
The potential energy curve (red curve) of molecular hydrogen is shown on top, to help visualize where in the dissociation of the hydrogen molecule the entropy is highest.

It can be seen that there are three different regions.
The first region is at small bond lengths, which gives a low entropy.
The second region is medium-range bond lengths (around 1.6 Ångstrom), which gives a peak in the entropy.
The third region is large bond lengths, which again gives a low entropy.

Let us disregard the first region.
The closer the hydrogen atoms go together, the more helium-like the system comes, thus nothing new to learn here.
Instead, let us now focus on a bond length of 1.6 Ångstrom.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/h2_kappa_medium.svg">
</p>

In the above graph, two different plots can be seen.
The top plot shows the CI coefficients as a function of the orbital rotation parameter.
In contrast to helium, no single CSF gets a coefficient close to the value of one for the entire range of orbital rotation values.
The bottom plot shows the entropy as a function of kappa.
The entropy stays large for all values of the orbital rotation parameter.
**This is an example of a truly multi-configurational system**, no single CSF is a good approximation to the full CI wave function.

Finally, let us calculate the CI coefficients as a function of the orbital rotation parameter for the very stretched hydrogen molecule, a bond length of 3 Ångstrom.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/h2_kappa_long.svg">
</p>

The above graph shows the same as the previous graph but for the stretched hydrogen molecule.
The notable feature here is that the Hartree-Fock orbitals (from a closed-shell restricted Hartree-Fock (RHF) calculation) do not give the lowest entropy.
If a CI calculation is performed on top of closed-shell RHF the molecule would seem multiconfigurational.
Both $$\left|1100\right>$$ and $$\left|0011\right>$$ has very significant coefficients.

If smarter orbitals are constructed ($$\kappa\approx1.6$$ on the graph) the stretched hydrogen molecule can to a very good approximation be described by a single CSF,
$$\frac{1}{\sqrt{2}}\left(\left|1001\right>-\left|0110\right>\right)$$.
