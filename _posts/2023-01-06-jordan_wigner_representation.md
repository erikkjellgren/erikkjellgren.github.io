---
layout: post
title: Jordan-Wigner representation
lang: en
lang-ref: Jordan-Wigner representation
tag: computation
---

Current quantum computers work with unitrary gates.
In order to represent operators relevant for quantum chemistry on a quantum computer, unitrary operators are thus needed.
The condition for a unitrary operator is:

$$ UU^\dagger = I $$

It can easily be checked if this condition is fulfilled for the annihilation and creation operators:

$$ \begin{eqnarray}
aa^\dagger &=& \left(\begin{matrix}
0 & 1\\
0 & 0
\end{matrix}\right)\left(\begin{matrix}
0 & 0\\
1 & 0
\end{matrix}\right) = \left(\begin{matrix}
1 & 0\\
0 & 0
\end{matrix}\right) \neq I \\
a^\dagger \left(a^\dagger\right)^\dagger &=& \left(\begin{matrix}
0 & 0\\
1 & 0
\end{matrix}\right)\left(\begin{matrix}
0 & 1\\
0 & 0
\end{matrix}\right) = \left(\begin{matrix}
0 & 0\\
0 & 1
\end{matrix}\right) \neq I
\end{eqnarray} $$

It can thus be seen that the annihilation and creation operators are not unitrary.
Instead we can consider the [Pauli operators](https://en.wikipedia.org/wiki/Pauli_matrices):

$$ \begin{eqnarray}
X &=& \left(\begin{matrix}
0 & 1\\
1 & 0
\end{matrix}\right) \\
Y &=& \left(\begin{matrix}
0 & -i\\
i & 0
\end{matrix}\right) \\
Z &=& \left(\begin{matrix}
1 & 0\\
0 & -1
\end{matrix}\right)
\end{eqnarray} $$

It can easily be verified that these operators are indeed unitrary:

$$ \begin{eqnarray}
XX^\dagger &=& \left(\begin{matrix}
0 & 1\\
1 & 0
\end{matrix}\right)\left(\begin{matrix}
0 & 1\\
1 & 0
\end{matrix}\right) = \left(\begin{matrix}
1 & 0\\
0 & 1
\end{matrix}\right) = I \\
YY^\dagger &=& \left(\begin{matrix}
0 & -i\\
i & 0
\end{matrix}\right)\left(\begin{matrix}
0 & -i\\
i & 0
\end{matrix}\right) = \left(\begin{matrix}
1 & 0\\
0 & 1
\end{matrix}\right) = I \\
ZZ^\dagger &=& \left(\begin{matrix}
1 & 0\\
0 & -1
\end{matrix}\right)\left(\begin{matrix}
1 & 0\\
0 & -1
\end{matrix}\right) = \left(\begin{matrix}
1 & 0\\
0 & 1
\end{matrix}\right) = I
\end{eqnarray} $$

Now let us consider the following construction:

$$ \frac{X+iY}{2} = \frac{\left(\begin{matrix}
0 & 1\\
1 & 0
\end{matrix}\right)+i\left(\begin{matrix}
0 & -i\\
i & 0
\end{matrix}\right)}{2} = \frac{\left(\begin{matrix}
0 & 1\\
1 & 0
\end{matrix}\right)+\left(\begin{matrix}
0 & 1\\
-1 & 0
\end{matrix}\right)}{2} = \frac{\left(\begin{matrix}
0 & 2\\
0 & 0
\end{matrix}\right)}{2} = \left(\begin{matrix}
0 & 1\\
0 & 0
\end{matrix}\right) = a $$

It can be seen that the annihilation operator can be expressed in terms of the Pauli operators.
The same is true for the creation operator:

$$ a^\dagger=\frac{X-iY}{2} $$

Now instead of using the phase-factor $$\Gamma$$ the sign change can be handled using $$Z$$ (I have not justified this).
The two annihaltion operators working on the state $$\left|11\right>$$ can now be constructed as:

$$ a_1 = \left(\frac{X+iY}{2}\right)\otimes I $$

and

$$ a_2 = Z\otimes \left(\frac{X+iY}{2}\right) $$

Let us try to expand out $$a_2$$ to see it gives what is expected:

$$ a_2 = Z\otimes \left(\frac{X+iY}{2}\right) = \left(\begin{matrix}
1 & 0\\
0 & -1
\end{matrix}\right)\otimes\left(\begin{matrix}
0 & 1\\
0 & 0
\end{matrix}\right) = \left(\begin{matrix}
0 & 1 & 0 & 0\\
0 & 0 & 0 & 0\\
0 & 0 & 0 & -1\\
0 & 0 & 0 & 0
\end{matrix}\right)$$

Using this $$a_2$$ on the state
$$\left|11\right>$$ now gives:

$$ a_2\left|11\right> = \left(\begin{matrix}
0 & 1 & 0 & 0\\
0 & 0 & 0 & 0\\
0 & 0 & 0 & -1\\
0 & 0 & 0 & 0
\end{matrix}\right)\left(\begin{matrix}
0\\
0\\
0\\
1
\end{matrix}\right) = \left(\begin{matrix}
0\\
0\\
-1\\
0
\end{matrix}\right) = -\left|10\right>$$

Which is the same as when using the phase-factor.
The annihilation and creation operator has now been expressed in terms of unitrary matrices.

## Translating the one-electron Hamiltonian

The one-electron part of the molecular Hamiltonian is given as:

$$ \hat{h} = \sum_{pq}h_{pq}a^\dagger_p a_q $$

Let us consider the state $$\left|1100\right>$$,
this could be $$\mathrm{H}_2$$ in a minimal basis, then this expands out to:

$$ \hat{h} = h_{11}a^\dagger_1 a_1 + h_{31}a^\dagger_3 a_1  + h_{41}a^\dagger_4 a_1 + h_{22}a^\dagger_2 a_2 + h_{32}a^\dagger_3 a_2  + h_{42}a^\dagger_4 a_2 $$

The rest of the terms will be zero due to annihilation of an empty orbital or creation into an occupied orbital.
The surviving operators for this specific example is thus, $$a_1$$, $$a_2$$, $$a^\dagger_1$$, $$a^\dagger_2$$, $$a^\dagger_3$$ and, $$a^\dagger_4$$.

As an example let us condsider $$h_{42}a^\dagger_4 a_2$$ (working on $$\left|1100\right>$$).
The annihilation operator will get the form:

$$ a_2 = Z\otimes a\otimes I \otimes I = Z\otimes \left(\frac{X+iY}{2}\right)\otimes I \otimes I $$

and the creation operator will get the form:

$$ a^\dagger_4 = Z\otimes Z\otimes I \otimes a^\dagger = Z\otimes Z\otimes I \otimes \left(\frac{X-iY}{2}\right) $$

Thus:

$$ h_{42}a^\dagger_4 a_2 = h_{42}\left(Z\otimes Z\otimes I \otimes \left(\frac{X-iY}{2}\right)\right)\left(Z\otimes \left(\frac{X+iY}{2}\right)\otimes I \otimes I\right) $$

Surely, some manipulation can be done that I have yet to figure out to arrive at the expression in [reference](https://learn.microsoft.com/en-us/azure/quantum/user-guide/libraries/chemistry/concepts/jordan-wigner).
