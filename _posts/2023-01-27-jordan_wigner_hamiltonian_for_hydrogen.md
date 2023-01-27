---
layout: post
title: Jordan-Wigner Hamiltonian for H2
lang: en
lang-ref: Jordan-Wigner Hamiltonian for H2
tag: computation
---

The first step of using quantum computers to perform quantum chemical simulations is to translate the fermionic Hamiltonian to a qubit Hamiltonian (represented by Pauli operators).

The fermionic Hamiltonian in spin basis is:

$$ H = \sum_{pq}h_{pq}a^\dagger_p a_q + \frac{1}{2}\sum_{pqrs}g_{pqrs}a^\dagger_p a^\dagger_q a_s a_r $$

Note here that for the second term the indicies $$s$$ and $$r$$ are flipped on the annihilation operators.
Here the integral elements are defined as:

$$ h_{pq} = \int\phi^\dagger_p(1)\hat{h}(1)\phi_q(1)\mathrm{d}r_1 $$

with the number indicating which electron the orbital is associted with, and, the two-electron integral being,

$$ g_{pqrs} = \int\phi^\dagger_p(1)\phi^\dagger_q(2)\hat{g}(1,2)\phi_r(1)\phi_s(2)\mathrm{d}r_1\mathrm{d}r_2 $$

From the [FCI of the hydrogen molecule]({{ site.baseurl }}/2023/01/25/constructing_fci_for_h2_lazily/) we know that the only surviving terms that contribute to the ground-state energy are:

$$ h_{11}a^\dagger_1 a_1,\quad h_{22}a^\dagger_2 a_2,\quad h_{33}a^\dagger_3 a_3,\quad h_{44}a^\dagger_4 a_4\\
\frac{1}{2}g_{1212}a^\dagger_1 a^\dagger_2 a_2 a_1,\quad \frac{1}{2}g_{2121}a^\dagger_2 a^\dagger_1 a_1 a_2,\quad \frac{1}{2}g_{3434}a^\dagger_3 a^\dagger_4 a_4 a_3,\quad \frac{1}{2}g_{4343}a^\dagger_4 a^\dagger_3 a_3 a_4\\
\frac{1}{2}g_{1234}a^\dagger_1 a^\dagger_2 a_4 a_3,\quad \frac{1}{2}g_{2143}a^\dagger_2 a^\dagger_1 a_3 a_4,\quad \frac{1}{2}g_{3412}a^\dagger_3 a^\dagger_4 a_2 a_1,\quad \frac{1}{2}g_{4321}a^\dagger_4 a^\dagger_3 a_1 a_2 $$

For reference let us remember that the Hartree-Fock energy for the hydrogen molecule (bondlength=1.401 bohr) is -1.83046 Hartree, and the FCI energy is -1.85105 Hartree

One way of translating this fermionic Hamiltonian is to use the [Jordan-Wigner represtentation]({{ site.baseurl }}/2023/01/06/jordan_wigner_representation/).

## One-electron operators Jordan-Wigner

Let us start by considering the $$h_{22}a^\dagger_2 a_2$$.
The Jordan-Wigner representation of the fermionic operators is:

$$ \begin{align}
a_2 &= \frac{1}{2}(Z\otimes X\otimes I\otimes I) + \frac{i}{2}(Z\otimes Y\otimes I\otimes I)\\
a^\dagger_2 &= \frac{1}{2}(Z\otimes X\otimes I\otimes I) - \frac{i}{2}(Z\otimes Y\otimes I\otimes I)
\end{align} $$

Now taking the product of the fermionic operators in Jordan-Wigner representation:

$$ \begin{align}
    h_{22}a_2^\dagger a_2 &= h_{22}\left[\frac{1}{2}\left(Z\otimes X\otimes I\otimes I\right) - \frac{i}{2}\left(Z\otimes Y\otimes I\otimes I\right)\right]\\
    &\quad\quad\quad\left[\frac{1}{2}\left(Z\otimes X\otimes I\otimes I\right) + \frac{i}{2}\left(Z\otimes Y\otimes I\otimes I\right)\right]\\
    &=\frac{h_{22}}{4}\left[\left(Z\otimes X\otimes I\otimes I\right)\left(Z\otimes X\otimes I\otimes I\right)\right]\\
    &+\frac{ih_{22}}{4}\left[\left(Z\otimes X\otimes I\otimes I\right)\left(Z\otimes Y\otimes I\otimes I\right)\right]\\
    &-\frac{ih_{22}}{4}\left[\left(Z\otimes Y\otimes I\otimes I\right)\left(Z\otimes X\otimes I\otimes I\right)\right]\\
    &+\frac{h_{22}}{4}\left[\left(Z\otimes Y\otimes I\otimes I\right)\left(Z\otimes Y\otimes I\otimes I\right)\right]
\end{align} $$

The algebraic trick is now to use the following relation ([from here](https://digitalcommons.unf.edu/cgi/viewcontent.cgi?article=1025\&context=etd)):

$$ \left(A_1\otimes A_2\otimes ...\otimes A_k\right)\left(B_1\otimes B_2\otimes ...\otimes B_k\right) = \left(A_1B_1\right)\otimes\left(A_2B_2\right)\otimes ...\otimes\left(A_kB_k\right) $$

Now using this relation to expand the first term:

$$ \begin{align}
   \frac{h_{22}}{4}\left[\left(Z\otimes X\otimes I\otimes I\right)\left(Z\otimes X\otimes I\otimes I\right)\right] &= \frac{h_{22}}{4}\left[\left(ZZ\right)\otimes\left(XX\right)\otimes\left(II\right)\otimes\left(II\right)\right]\\
   &= \frac{h_{22}}{4}\left[I\otimes I\otimes I\otimes I\right]
\end{align} $$

Similarly, it can be found that:

$$ \frac{h_{22}}{4}\left[\left(Z\otimes Y\otimes I\otimes I\right)\left(Z\otimes Y\otimes I\otimes I\right)\right] = \frac{h_{22}}{4}\left[I\otimes I\otimes I\otimes I\right] $$

The remaining two terms can also be expanded and reduced:

$$ \begin{align}
    &\frac{ih_{22}}{4}\left[\left(Z\otimes X\otimes I\otimes I\right)\left(Z\otimes Y\otimes I\otimes I\right)\right] -\frac{ih_{22}}{4}\left[\left(Z\otimes Y\otimes I\otimes I\right)\left(Z\otimes X\otimes I\otimes I\right)\right]\\
    &=\frac{ih_{22}}{4}\left[(ZZ)\otimes (XY)\otimes I\otimes I + (ZZ)\otimes (YX)\otimes I\otimes I\right]\\
    &=\frac{ih_{22}}{4}\left[I\otimes (iZ)\otimes I\otimes I - I\otimes (-iZ)\otimes I\otimes I\right]\\
    &=-\frac{h_{22}}{2}\left[Z\otimes I\otimes I\otimes I\right]
\end{align} $$

Here it was used that $$XY=iZ$$ and $$YX=-iZ$$.

Now putting all the terms together the Jordan-Wigner representation of this fermionic operator is:

$$ h_{22}a_2^\dagger a_2 = \frac{h_{22}}{2}\left(I\otimes I\otimes I\otimes I - I\otimes Z\otimes I\otimes I\right) $$

By very similar algebra it can also be found that:

$$ \begin{align}
    h_{11}a^\dagger_1 a_1 &= \frac{h_{11}}{2}\left(I\otimes I\otimes I\otimes I - Z\otimes I\otimes I\otimes I\right)\\
    h_{33}a^\dagger_3 a_3 &= \frac{h_{33}}{2}\left(I\otimes I\otimes I\otimes I - I\otimes I\otimes Z\otimes I\right)\\
    h_{44}a^\dagger_4 a_4 &= \frac{h_{44}}{2}\left(I\otimes I\otimes I\otimes I - I\otimes I\otimes I\otimes Z\right)
\end{align} $$

## Two-electron operators Jordan-Wigner

Now let us consider one of the two-electron terms:

$$ \begin{align}
    a^\dagger_1 a^\dagger_2 a_2 a_1 &=
    \left[\frac{1}{2}\left(X\otimes I\otimes I\otimes I\right)- \frac{i}{2}\left(Y\otimes I\otimes I\otimes I\right)\right]\\
    &\quad\left[\frac{1}{2}\left(Z\otimes X\otimes I\otimes I\right)- \frac{i}{2}\left(Z\otimes Y\otimes I\otimes I\right)\right]\\
    &\quad\left[\frac{1}{2}\left(X\otimes I\otimes I\otimes I\right)+ \frac{i}{2}\left(Y\otimes I\otimes I\otimes I\right)\right]\\
    &\quad\left[\frac{1}{2}\left(Z\otimes X\otimes I\otimes I\right)+ \frac{i}{2}\left(Z\otimes Y\otimes I\otimes I\right)\right]\\
\end{align} $$

Multiplying this out will give up to 16 terms!
The algebra is exactly the same as was used for the one-electron operator, so instead of doing this by hand, I have cheated and made a Python script that will do the algebra.
The Python script can be found here: [pauli_string_twoe_terms.py]({{ site.baseurl }}/assets/python_scripts/pauli_string_twoe_terms.py)

The first four of the two-electron operators gets the from:

$$ \begin{align}
    a^\dagger_1 a^\dagger_2 a_2 a_1 &= \frac{1}{4}\left(I\otimes I\otimes I\otimes I -Z\otimes I\otimes I\otimes I -I\otimes Z\otimes I\otimes I + Z\otimes Z\otimes I\otimes I\right)\\
    a^\dagger_2 a^\dagger_1 a_1 a_2 &= \frac{1}{4}\left(I\otimes I\otimes I\otimes I -I\otimes Z\otimes I\otimes I -Z\otimes I\otimes I\otimes I + Z\otimes Z\otimes I\otimes I\right)\\
    a^\dagger_3 a^\dagger_4 a_3 a_4 &= \frac{1}{4}\left(I\otimes I\otimes I\otimes I -I\otimes I\otimes Z\otimes I -I\otimes I\otimes I\otimes Z + I\otimes I\otimes Z\otimes Z\right)\\
    a^\dagger_4 a^\dagger_3 a_3 a_4 &= \frac{1}{4}\left(I\otimes I\otimes I\otimes I -I\otimes I\otimes I\otimes Z -I\otimes I\otimes Z\otimes I + I\otimes I\otimes Z\otimes Z\right)
\end{align} $$

The last four gives alot more terms, and I will refrain from typing them out.
If the specific form is of interest, just try to run the Python script.

As a sanity check it can be seen that the Jordan-Wigner representation is exactly what is expected when looking at [the equations from Microsoft](https://learn.microsoft.com/en-us/azure/quantum/user-guide/libraries/chemistry/concepts/jordan-wigner).

## Jordan-Wigner Hartree-Fock Hamiltonian

As a sanity check (and because it is much easy to write out), let us start by considering the Hartree-Fock Hamiltonian in Jordan-Wigner representation.
Diagonalizing the Hartee-Fock Hamiltonian should give us the Hartee-Fock energy as the ground state.

The only surviving terms for the Hartree-Fock approximation are:

$$ h_{11}a^\dagger_1 a_1,\quad h_{22}a^\dagger_2 a_2,\quad \frac{1}{2}g_{1212}a^\dagger_1 a^\dagger_2 a_2 a_1,\quad \frac{1}{2}g_{2121}a^\dagger_2 a^\dagger_1 a_1 a_2 $$

Putting everything together the Hamiltonian becomes:

$$ \begin{align}
H^{\mathrm{JW},\mathrm{HF}} &= \frac{h_{11}}{2}\left(I\otimes I\otimes I\otimes I - Z\otimes I\otimes I\otimes I\right) + \frac{h_{22}}{2}\left(I\otimes I\otimes I\otimes I - I\otimes Z\otimes I\otimes I\right)\\
&+\frac{g_{1212}}{8}\left(I\otimes I\otimes I\otimes I -Z\otimes I\otimes I\otimes I -I\otimes Z\otimes I\otimes I + Z\otimes Z\otimes I\otimes I\right)\\
&+\frac{g_{2121}}{8}\left(I\otimes I\otimes I\otimes I -I\otimes Z\otimes I\otimes I -Z\otimes I\otimes I\otimes I + Z\otimes Z\otimes I\otimes I\right)
\end{align} $$

Now collecting terms according to their Pauli strings:

$$ \begin{align}
H^{\mathrm{JW},\mathrm{HF}} &= f_1(I\otimes I\otimes I\otimes I) + f_2(Z\otimes I\otimes I\otimes I)\\
&+ f_3(I\otimes Z\otimes I\otimes I) + f_4(Z\otimes Z\otimes I\otimes I)
\end{align} $$

With the factors being:

$$ \begin{align}
f1 &= \frac{h_{11}}{2} + \frac{h_{22}}{2} + \frac{g_{1212}}{8} + \frac{g_{2121}}{8}\\
f2 &= -\frac{h_{11}}{2} - \frac{g_{1212}}{8} - \frac{g_{2121}}{8}\\
f3 &= -\frac{h_{22}}{2} - \frac{g_{1212}}{8} - \frac{g_{2121}}{8}\\
f4 &= \frac{g_{1212}}{8} + \frac{g_{2121}}{8}\\
\end{align} $$

Doing the number-crunching the Hamiltonian matrix will have the from:

$$ H^{\mathrm{JW},\mathrm{HF}} = \left(\begin{matrix}
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & -1.3 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & -1.3 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & -1.3 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & -1.3 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & -1.3 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & -1.3 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & -1.3 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & -1.3 & 0.0 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & -1.8 & 0.0 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & -1.8 & 0.0 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & -1.8 & 0.0\\
0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & 0.0 & -1.8
\end{matrix}\right) $$

Luckily, as expected it is a diagonal matrix with the lowest eigenvalue being equal to the Hartree-Fock energy (more decimal places would not fit on the screen).

One thing we should immediately note (that we might not have considered when doing the symbolic math), is that the dimension of the matrix is 16.
Naively, with two-electrons in four spin-orbitals we would only expected a dimension of 6 (this is including the triplet determinants).
Usually we only work in a subspace of Fock-space, f.eks. restricting the number of electrons to be two.
The framework we are considering right now work with the entire Fock-space.
Let us count the number of states that are in the entire Fock-space for four spin-orbitals to convince ourself this is the case.

| # electrons | States |
|:-----------:|:------:|
| 0 | $$\left\|0000\right>$$ |
| 1 | $$\left\|1000\right>$$, $$\left\|0100\right>$$, $$\left\|0010\right>$$, $$\left\|0001\right>$$ |
| 2 | $$\left\|1100\right>$$, $$\left\|1010\right>$$, $$\left\|1001\right>$$, $$\left\|0110\right>$$, $$\left\|0101\right>$$, $$\left\|0011\right>$$ |
| 3 | $$\left\|1110\right>$$, $$\left\|1101\right>$$, $$\left\|1011\right>$$, $$\left\|0111\right>$$ |
| 4 | $$\left\|1111\right>$$ |

The solution we find is therefore the lowest energy of any combination electrons (foreshadowing, this might cause problems).

## FCI Jordan-Wigner Hamiltonian

Now let us construct the Jordan-Wigner Hamiltonian for the FCI problem.
We will include the terms mentioned in the beginning of this post, here they are again for convinience:

$$ h_{11}a^\dagger_1 a_1,\quad h_{22}a^\dagger_2 a_2,\quad h_{33}a^\dagger_3 a_3,\quad h_{44}a^\dagger_4 a_4\\
\frac{1}{2}g_{1212}a^\dagger_1 a^\dagger_2 a_2 a_1,\quad \frac{1}{2}g_{2121}a^\dagger_2 a^\dagger_1 a_1 a_2,\quad \frac{1}{2}g_{3434}a^\dagger_3 a^\dagger_4 a_4 a_3,\quad \frac{1}{2}g_{4343}a^\dagger_4 a^\dagger_3 a_3 a_4\\
\frac{1}{2}g_{1234}a^\dagger_1 a^\dagger_2 a_4 a_3,\quad \frac{1}{2}g_{2143}a^\dagger_2 a^\dagger_1 a_3 a_4,\quad \frac{1}{2}g_{3412}a^\dagger_3 a^\dagger_4 a_2 a_1,\quad \frac{1}{2}g_{4321}a^\dagger_4 a^\dagger_3 a_1 a_2 $$

Again there is alot of terms, and putting everything together by hand is cumbersome.
Python is thus to come to the rescue again.
The Python script to construct the Jordan-Wigner Hamiltonian for the hydrogen molecule can be found her: [construct_jw_hamiltonian_hydrogen.py]({{ site.baseurl }}/assets/python_scripts/construct_jw_hamiltonian_hydrogen.py)

Which Hamiltonian that is wanted can be changed in the top of the script by modifying the variable 'hamiltonian_type'.
'CID' corrosponds to the Hamiltonian we are constructing right now (only the double excitation contribute to the ground-state energy for the hydrogen molecule in a minimal basis).

Building and diagonalizing this Hamiltonian gives the eigenvalues, [-2.3064  -2.3064  -2.08493 -1.85105 -1.72841 -1.72841 -1.72841 -1.72841
 -1.50695 -1.50695 -1.25248 -1.25248 -0.47593 -0.47593 -0.23389  0.     ].

First let us note that the last eigenvalue is 0.
This is from the state $$\left|0000\right>$$, zero electrons will give an electronic energy of 0.

When considering the first few eigenvalues problems can immediately be seen, the first three eigenvalues have a lower energy than we expect.
The FCI ground-state energy is the fourth eigenvalue!

Even tho we have been 'smart' and restricting the operators to operators we know contribute to the ground-state energy, we are still looking for the solution in the full Fock-space.
I.e. we are considering all possible electronic states, but have heavily restricted what interactions we are including in the Hamiltonian by throwing out most of our integrals.

Let us consider the energy of the state
$$\left|1111\right>$$ when we are only 'allowed' to use the integrals that contribute to the ground-state energy of the hydrogen molecule:

$$ \begin{align}
E_{\mathrm{spurious},\left|1111\right>} &= \left<1111\left|H^\mathrm{CID}\right|1111\right>\\
&= h_{11} + h_{22} + h_{33} + h_{44} + \frac{1}{2}\left(g_{1212} + g_{2121} + g_{3434} + g_{4343}\right)\\
&= -2.08493
\end{align} $$

Which is exactly the third eigenvalue we have found.
It should be obvious why these lower energies are spurious or meaningless.

If no tricks are used to reduce the Hamiltonian, i.e. all possible terms are included, then the diagonalization will give the eigenvalues, [-1.85105 -1.25248 -1.25248 -1.24623 -0.88365 -0.88365 -0.88365 -0.79816 -0.79816 -0.47593 -0.47593 -0.23389 -0.       0.00128  0.00128  0.93153]

Now the FCI ground-state energy is as expected -1.85105.
