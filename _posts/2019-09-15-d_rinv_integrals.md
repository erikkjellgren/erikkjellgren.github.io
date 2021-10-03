---
layout: post
title: Constructing molecular integrals with derivative on the r_inv operator by partial integration
lang: en
lang-ref: Constructing molecular integrals with derivative on the r_inv operator by partial integration
tag: computation
---

In quantum chemstry integrals of the following form are sometimes needed:

$$ F_x = \left<\phi_i\left|\nabla^x r^{-1}\right|\phi_j\right> $$

But these integrals are often not directly available.

What instead is available is integrals of the form:

$$ f_x = \left<\nabla^x\phi_i\left|r^{-1}\right|\phi_j\right> $$

$$ f_{x,y} = \left<\nabla^x\phi_i\left|r^{-1}\right|\nabla^y\phi_j\right> $$

Let us therefore try to formulate $$F_x$$ in terms of $$f_x$$ and $$f_{x,y}$$.
Now switching the integral notation to the more "regular" notation:

$$ F_x = \int_\Omega \phi_i \phi_j \nabla^x r^{-1} \mathrm{d}r $$

Doing [integration by parts](https://en.wikipedia.org/wiki/Integration_by_parts):

$$ F_x = \left[ \phi_i \phi_j \nabla^{x-1} r^{-1} \right]_{\partial\Omega} - \int_\Omega \nabla \left(\phi_i \phi_j \right) \nabla^{x-1} r^{-1} \mathrm{d}r $$

The wave function goes to zero at infinity, therefore the first term is zero:

$$ F_x = - \int_\Omega \nabla \phi_i \phi_j  \nabla^{x-1} r^{-1} \mathrm{d}r - \int_\Omega \phi_i \nabla \phi_j  \nabla^{x-1} r^{-1} \mathrm{d}r $$

Doing integration by parts again:

$$ F_x = -\left(\left[ \nabla \phi_i \phi_j\nabla^{x-2} r^{-1} \right]_{\partial\Omega}
         -  \int_\Omega \nabla \left(\nabla \phi_i \phi_j\right)  \nabla^{x-2} r^{-1} \mathrm{d}r \right)
         -\left(\left[ \phi_i \nabla \phi_j\nabla^{x-2} r^{-1} \right]_{\partial\Omega}
         -  \int_\Omega \nabla \left( \phi_i \nabla \phi_j \right)  \nabla^{x-2} r^{-1} \mathrm{d}r \right) $$

The wave function goes to zero at infinity, therefore the first term is zero:

$$ F_x = -\left(-\int_\Omega \nabla^2 \phi_i \phi_j  \nabla^{x-2} r^{-1} \mathrm{d}r
         -  \int_\Omega \nabla \phi_i \nabla \phi_j  \nabla^{x-2} r^{-1} \mathrm{d}r\right)
         -\left(-\int_\Omega \nabla \phi_i \nabla \phi_j \nabla^{x-2} r^{-1} \mathrm{d}r
         -  \int_\Omega \phi_i \nabla^2 \phi_j \nabla^{x-2} r^{-1} \mathrm{d}r \right) $$

Simplifying:

$$ F_x = \int_\Omega \nabla^2 \phi_i \phi_j  \nabla^{x-2} r^{-1} \mathrm{d}r
         +  \int_\Omega \phi_i \nabla^2 \phi_j \nabla^{x-2} r^{-1} \mathrm{d}r
         +  2\int_\Omega \nabla \phi_i \nabla \phi_j  \nabla^{x-2} r^{-1} \mathrm{d}r $$

We therefore now have:

$$ F_1 = \left<\phi_i\left|\nabla r^{-1}\right|\phi_j\right> = - \int_\Omega \nabla \phi_i \phi_j  r^{-1} \mathrm{d}r - \int_\Omega \phi_i \nabla \phi_j r^{-1} \mathrm{d}r $$

and,

$$ F_2 = \left<\phi_i\left|\nabla^2 r^{-1}\right|\phi_j\right> = \int_\Omega \nabla^2 \phi_i \phi_j r^{-1} \mathrm{d}r
         +  \int_\Omega \phi_i \nabla^2 \phi_j r^{-1} \mathrm{d}r
         +  2\int_\Omega \nabla \phi_i \nabla \phi_j r^{-1} \mathrm{d}r $$

I.e. the integrals have been constructed without taking the derivative of $$r^{-1}$$.
If hihger derivatives are needed, simply just do partial integration again.
