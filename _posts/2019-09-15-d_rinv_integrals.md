---
layout: post
title: Constructing molecular integrals with derivative on the r_inv operator by partial integration
lang: en
lang-ref: Constructing molecular integrals with derivative on the r_inv operator by partial integration
tag: quantum
---

In quantum chemstry integrals of the following form are sometimes needed:

$$ F_a = \left<\phi_i\left|\nabla^a r^{-1}\right|\phi_j\right> $$

But these integrals are often not directly available.

What instead is available is integrals of the form:

$$ f_a = \left<\nabla^a\phi_i\left|r^{-1}\right|\phi_j\right> $$

$$ f_{a,b} = \left<\nabla^a\phi_i\left|r^{-1}\right|\nabla^b\phi_j\right> $$

Let us therefore trb to formulate $$F_a$$ in terms of $$f_a$$ and $$f_{a,b}$$.
Now switching the integral notation to the more "regular" notation:

$$ F_a = \int_\Omega \phi_i \phi_j \nabla^a r^{-1} \mathrm{d}r $$

Doing [integration by parts](https://en.wikipedia.org/wiki/Integration_by_parts):

$$ F_a = \left[ \phi_i \phi_j \nabla^{a-1} r^{-1} \right]_{\partial\Omega} - \int_\Omega \nabla \left(\phi_i \phi_j \right) \nabla^{a-1} r^{-1} \mathrm{d}r $$

The wave function goes to zero at infinity, therefore the first term is zero:

$$ F_a = - \int_\Omega \nabla \phi_i \phi_j  \nabla^{a-1} r^{-1} \mathrm{d}r - \int_\Omega \phi_i \nabla \phi_j  \nabla^{a-1} r^{-1} \mathrm{d}r $$

Doing integration by parts again:

$$ F_a = -\left(\left[ \nabla \phi_i \phi_j\nabla^{a-2} r^{-1} \right]_{\partial\Omega}
         -  \int_\Omega \nabla \left(\nabla \phi_i \phi_j\right)  \nabla^{a-2} r^{-1} \mathrm{d}r \right)
         -\left(\left[ \phi_i \nabla \phi_j\nabla^{a-2} r^{-1} \right]_{\partial\Omega}
         -  \int_\Omega \nabla \left( \phi_i \nabla \phi_j \right)  \nabla^{a-2} r^{-1} \mathrm{d}r \right) $$

The wave function goes to zero at infinity, therefore the first term is zero:

$$ F_a = -\left(-\int_\Omega \nabla^2 \phi_i \phi_j  \nabla^{a-2} r^{-1} \mathrm{d}r
         -  \int_\Omega \nabla \phi_i \nabla \phi_j  \nabla^{a-2} r^{-1} \mathrm{d}r\right)
         -\left(-\int_\Omega \nabla \phi_i \nabla \phi_j \nabla^{a-2} r^{-1} \mathrm{d}r
         -  \int_\Omega \phi_i \nabla^2 \phi_j \nabla^{a-2} r^{-1} \mathrm{d}r \right) $$

Simplifying:

$$ F_a = \int_\Omega \nabla^2 \phi_i \phi_j  \nabla^{a-2} r^{-1} \mathrm{d}r
         +  \int_\Omega \phi_i \nabla^2 \phi_j \nabla^{a-2} r^{-1} \mathrm{d}r
         +  2\int_\Omega \nabla \phi_i \nabla \phi_j  \nabla^{a-2} r^{-1} \mathrm{d}r $$

We therefore now have:

$$ F_1 = \left<\phi_i\left|\nabla r^{-1}\right|\phi_j\right> = - \int_\Omega \nabla \phi_i \phi_j  r^{-1} \mathrm{d}r - \int_\Omega \phi_i \nabla \phi_j r^{-1} \mathrm{d}r $$

and,

$$ F_2 = \left<\phi_i\left|\nabla^2 r^{-1}\right|\phi_j\right> = \int_\Omega \nabla^2 \phi_i \phi_j r^{-1} \mathrm{d}r
         +  \int_\Omega \phi_i \nabla^2 \phi_j r^{-1} \mathrm{d}r
         +  2\int_\Omega \nabla \phi_i \nabla \phi_j r^{-1} \mathrm{d}r $$

I.e. the integrals have been constructed without taking the derivative of $$r^{-1}$$.
How to use these formulas with integrals available from [PySCF](https://pyscf.org/) can be seen [here](https://github.com/erikkjellgren/Shared_scripts/blob/main/notebooks/PySCF-rinv-derivatives-integrals.ipynb).
If hihger derivatives are needed, simply just do partial integration again.
