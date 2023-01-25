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
