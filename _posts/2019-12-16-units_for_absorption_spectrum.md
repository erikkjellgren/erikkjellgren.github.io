---
layout: post
title: Unit for one-photon absorbtion spectrum
---

Following the source:

A. Rizzo, S. Coriani,  and K. Ruud, Computational Strategies for Spectroscopy. From Small Molecules  to  Nano Systems, edited by V. Barone (John Wiley and Sons, 2012) Chap. 2, pp.77–135.

It is given in Eq. (2.35) that:

$$ \varepsilon(\omega) = \frac{2 e^2 \pi^2 N_A}{1000 \ln(10) 4\pi \epsilon_0 n m_e c}\sum_i\frac{\omega f_i}{\omega_i}g_i(\omega, \gamma_i) $$

Now $$g_i$$ is assumed to be normalized, thus it will carry the inverse unit of the broadening factor, $$\gamma_i$$, which have the same unit as $$\omega$$.
The oscillator strength, $$f_i$$ is unit-less, and the fraction $$\frac{\omega}{\omega_i}$$ must also be unit-less.
Inserting the numerical value of all the constants in SI units.
Here $$N_A=6.022140760\times 10^{23}\mathrm{\frac{1}{mol}}$$ is Avogadros number.
$$e=1.602176620\times10^{-19}\mathrm{C}$$ is a charge of an electron.
$$\epsilon_0=8.854187818\times 10^{-12} \mathrm{\frac{F}{m}}$$ is the vacuum permativiy.
$$n$$ is the refraction index which is unit-less and here approximated to be $$1$$.
$$m_e=9.109383560\times 10^{-31} \mathrm{kg}$$ is the mass of an electron.
$$c=299792458 \mathrm{\frac{m}{s}}$$ is the speed of light.
It can be understood from the text the $$1000$$ have to do with unit conversion, it will therefore be removed since the unit conversion will be handled here:

$$ \varepsilon(\omega) = \frac{2 e^2 \pi^2 N_A}{\ln(10) 4\pi \epsilon_0 n m_e c}\sum_i\frac{\omega f_i}{\omega_i}g_i(\omega, \gamma_i) $$

Now inserting all the constants gives:

$$ \varepsilon(\omega) = 4.361314937\times 10^{18} \mathrm{\frac{m^2}{s\cdot mol}}\sum_i\frac{\omega f_i}{\omega_i}g_i(\omega, \gamma_i) $$

If it is now assumed that the broadening factor $$\gamma_i$$ is given in atomic units, this can then be converted to angular frequency in Hz.

$$ \varepsilon(\omega) = 4.361314937\times 10^{18} \mathrm{\frac{m^2}{s\cdot mol}}\sum_i\frac{\omega f_i}{\omega_i}g_i(\omega, \gamma_i)[\mathrm{au^{-1}}] $$

Now converting to Hz:

$$  \varepsilon(\omega) = 4.361314937\times 10^{18} \mathrm{\frac{m^2}{s\cdot mol}}\sum_i\frac{\omega f_i}{\omega_i}g_i(\omega, \gamma_i)[\mathrm{au^{-1}}]\frac{1}{2\pi\cdot 6.57968\times 10^{15}\mathrm{\frac{Hz}{au}}} $$

Putting together all the numerics (note that we now understand $$g_i$$ as being unit-less):

$$ \varepsilon(\omega) = 105.4952262 \mathrm{\frac{m^2}{ mol}}\sum_i\frac{\omega f_i}{\omega_i}g_i(\omega[\mathrm{au}], \gamma_i[\mathrm{au}]) $$

Converting to the wanted unit of $$\mathrm{\frac{L}{mol\cdot cm}}$$:

$$ \varepsilon(\omega) = 105.4952262 \mathrm{\frac{m^2}{ mol}\frac{1000\frac{L}{m^3}}{100\frac{cm}{m}}}\sum_i\frac{\omega f_i}{\omega_i}g_i(\omega[\mathrm{au}], \gamma_i[\mathrm{au}]) $$

Thus:

$$ \varepsilon(\omega) = 1054.952262 \mathrm{\frac{L}{ mol\cdot cm}}\sum_i\frac{\omega f_i}{\omega_i}g_i(\omega[\mathrm{au}], \gamma_i[\mathrm{au}]) $$

It is not immediately obvious that this is the same result as Eq. (2.57) that states:

$$ \varepsilon(\omega)\mathrm{\left[\frac{L}{mol\cdot cm}\right]} = 7.03301\times 10^2 \omega[\mathrm{au}] \sum_i g_i(\omega[\mathrm{au}]) \left| \mu_i[\mathrm{au}] \right|^2 $$

In the above equation there is the square of the length of the dipole moment, it can be used that:

$$  \left| \mu_i \right|^2 = \frac{3\hbar e^2 f_i}{2 m_e \omega_i} $$

Which in atomic units reduces to:

$$ \left| \mu_i[\mathrm{au}] \right|^2 = \frac{3 f_i}{2 \omega_i} $$

Thus giving:

$$ \varepsilon(\omega)\mathrm{\left[\frac{L}{mol\cdot cm}\right]} = 1.0549515\times 10^3 \sum_i\frac{\omega f_i}{\omega_i} g_i(\omega[\mathrm{au}]) $$

Which is now the same.
