---
layout: post
title: Second quantization in matrix formulation
lang: en
lang-ref: Second quantization in matrix formulation
tag: computation
---

Coming from a theoretical chemistry background, I have mostly learned second quantization from [Molecular Electronic-Structure Theory](https://onlinelibrary.wiley.com/doi/book/10.1002/9781119019572).

From the algebra is taught with the ON vector, $$\left|10\right>$$ denoting the first orbital being occupied and the second orbital being unoccupied.
In the simplest form the algebra is defined as (for a single orbital state):

$$ \begin{eqnarray}
   a\left|1\right> &=& \left|0\right> \\
   a\left|0\right> &=& 0 \\
   a^\dagger\left|1\right> &=& 0 \\
   a^\dagger\left|0\right> &=& \left|1\right>
   \end{eqnarray} $$

Here, $$a$$ denoting the annihilation operator, and $$a^\dagger$$ denoting the creation operator.
I later learned that the creation and annihilation operators can be expressed in terms of Pauli matrices.
Having learned second quantization without ever thinking about a matrix representation, this was very confusing.

## Single orbital second quantization

Let us start by considering a single orbital state to introduce the matrix-vector notation of second quantization.
In second quantization an orbital occupation is represented as vector with the notation:

$$ \phi_\mathrm{occ} = \left(\begin{matrix}
0\\
1
\end{matrix}\right)= \left|1\right> $$

and,

$$ \phi_\mathrm{unocc} = \left(\begin{matrix}
1\\
0
\end{matrix}\right) = \left|0\right> $$

The take-away from this notation is that $$\left|0\right>$$ is a two-element vector, and not just a $$1$$ or $$0$$.
Now let us consider how the annihilation and creation operators can be defined as matrices that will fullfill the algebraric rules we know from second quantization.
Removing an electron from an orbital can be done using the annihilation operator (see these [lecture notes](https://www.phys.hawaii.edu/~yepez/Spring2013/lectures/Lecture2_Quantum_Gates_Notes.pdf) for an overview of the operators):

$$ a = \left(\begin{matrix}
0 & 1\\
0 & 0
\end{matrix}\right) $$

Using this on the occupied orbital, and the unoccupied orbital gives:

$$ \begin{eqnarray}
   a\left|1\right> &=& \left(\begin{matrix}
   0 & 1\\
   0 & 0
   \end{matrix}\right)\left(\begin{matrix}
   0\\
   1
   \end{matrix}\right) = \left(\begin{matrix}
   1\\
   0
   \end{matrix}\right) = \left|0\right> \\
   a\left|0\right> &=& \left(\begin{matrix}
   0 & 1\\
   0 & 0
   \end{matrix}\right)\left(\begin{matrix}
   1\\
   0
   \end{matrix}\right)= \left(\begin{matrix}
   0\\
   0
   \end{matrix}\right)= \mathbf{0}
   \end{eqnarray} $$


Note that $$\mathbf{0}$$ is different from
$$\left|0\right>$$.

Creating an electron in an orbital can be done using the creation operator:

$$ a^\dagger = \left(\begin{matrix}
0 & 0\\
1 & 0
\end{matrix}\right) $$

Using this on the occupied orbital, and the unoccupied orbital gives:

$$ \begin{eqnarray}
   a^\dagger\left|1\right> &=& \left(\begin{matrix}
   0 & 0\\
   1 & 0
   \end{matrix}\right)\left(\begin{matrix}
   0\\
   1
   \end{matrix}\right) = \left(\begin{matrix}
   0\\
   0
   \end{matrix}\right) = \mathbf{0} \\
   a^\dagger\left|0\right> &=& \left(\begin{matrix}
   0 & 0\\
   1 & 0
   \end{matrix}\right)\left(\begin{matrix}
   1\\
   0
   \end{matrix}\right) = \left(\begin{matrix}
   0\\
   1
   \end{matrix}\right) = \left|1\right>
   \end{eqnarray} $$

It should be noted that from this notation, working on $$\mathbf{0}$$ with either the annihilation or creation operator will still return $$\mathbf{0}$$:

$$ \begin{eqnarray}
   a\mathbf{0} &=& \left(\begin{matrix}
   0 & 1\\
   0 & 0
   \end{matrix}\right)\left(\begin{matrix}
   0\\
   0
   \end{matrix}\right) = \left(\begin{matrix}
   0\\
   0
   \end{matrix}\right) = \mathbf{0} \\
   a^\dagger\mathbf{0} &=& \left(\begin{matrix}
   0 & 0\\
   1 & 0
   \end{matrix}\right)\left(\begin{matrix}
   0\\
   0
   \end{matrix}\right) = \left(\begin{matrix}
   0\\
   0
   \end{matrix}\right) = \mathbf{0}
   \end{eqnarray} $$

## Multi orbitals second quantization

Most systems of interest have quite a few more orbitals than a single one.
To describe multiple orbitals with this vector notation, a multi-orbital state can be contructed as [Kronecker product](https://en.wikipedia.org/wiki/Kronecker_product) of multiple single orbital states.
For systems of more than two orbital the notation is:

$$ \psi = \left(\begin{matrix}
0\\
1
\end{matrix}\right)\otimes\left(\begin{matrix}
0\\
1
\end{matrix}\right) = \left|1\right>\otimes\left|1\right> = \left|11\right> $$

For two orbitals four different states can be constructed:

$$ \begin{eqnarray}
\left|11\right> &=& \left(\begin{matrix}
0\\
1
\end{matrix}\right)\otimes\left(\begin{matrix}
0\\
1
\end{matrix}\right) = \left(\begin{matrix}
0\\
0\\
0\\
1
\end{matrix}\right) \\
\left|10\right> &=& \left(\begin{matrix}
0\\
1
\end{matrix}\right)\otimes\left(\begin{matrix}
1\\
0
\end{matrix}\right) = \left(\begin{matrix}
0\\
0\\
1\\
0
\end{matrix}\right) \\
\left|01\right> &=& \left(\begin{matrix}
1\\
0
\end{matrix}\right)\otimes\left(\begin{matrix}
0\\
1
\end{matrix}\right) = \left(\begin{matrix}
0\\
1\\
0\\
0
\end{matrix}\right) \\
\left|00\right> &=& \left(\begin{matrix}
1\\
0
\end{matrix}\right)\otimes\left(\begin{matrix}
1\\
0
\end{matrix}\right) = \left(\begin{matrix}
1\\
0\\
0\\
0
\end{matrix}\right)
\end{eqnarray} $$

A detail that was unnecessary for a single orbital, is that the acting of the annihilation and creation operators need to satisfy the anti-symmetry of the wave-function.
Without justification, this can be achived by using a phase-factor:

$$ \Gamma = (-1)^{\sum_{i=1}^{\alpha-1}n_i} $$

Where $$n\left|1\right> = 1$$ and, $$n\left|0\right> = 0$$. The above phase-factor is for $$a_\alpha$$ or $$a^\dagger_\alpha$$.
The phase-factor is $$1$$ if there is an even number of occupied orbitals prior to orbital $$\alpha$$, and $$-1$$ if there is an uneven number.

For a two orbital state, the state-vector has a dimension of four.
In order for the annihilation and creation operators to work on this state-vector, the annihilation and creation operators need to be formulated as four-times-four matrices.
This can be achived by taking the Kronecker producter with the identity matrix.
The annihilation operators $$a_1$$ and $$a_2$$ can now be constructed as:

$$ \begin{eqnarray}
a_1 &=& \Gamma \left(a\otimes I\right) \\
a_2 &=& \Gamma\left( I\otimes a\right)
\end{eqnarray} $$

Here $$I$$ is the two-times-two identity matrix.
Acting on the state $$\left|11\right>$$ these two operators become:

$$ \begin{eqnarray}
a_1 &=& \left(\begin{matrix}
0 & 1\\
0 & 0
\end{matrix}\right) \otimes \left(\begin{matrix}
1 & 0\\
0 & 1
\end{matrix}\right) = \left(\begin{matrix}
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1\\
0 & 0 & 0 & 0\\
0 & 0 & 0 & 0
\end{matrix}\right) \\
a_2 &=& -\left(\left(\begin{matrix}
1 & 0\\
0 & 1
\end{matrix}\right) \otimes \left(\begin{matrix}
0 & 1\\
0 & 0
\end{matrix}\right)\right) = -\left(\begin{matrix}
0 & 1 & 0 & 0\\
0 & 0 & 0 & 0\\
0 & 0 & 0 & 1\\
0 & 0 & 0 & 0
\end{matrix}\right)
\end{eqnarray} $$

Using $$a_1$$ on the state
$$\left|11\right>$$ now gives:

$$ a_1\left|11\right> = \left(\begin{matrix}
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1\\
0 & 0 & 0 & 0\\
0 & 0 & 0 & 0
\end{matrix}\right)\left(\begin{matrix}
0\\
0\\
0\\
1
\end{matrix}\right) = \left(\begin{matrix}
0\\
1\\
0\\
0
\end{matrix}\right) = \left|01\right>$$

It can be noted that this gives the same as:

$$ \left(a\left|1\right>\right)\otimes \left|1\right> = \left|0\right>\otimes \left|1\right> = \left|01\right> $$

Using $$a_2$$ on state
$$\left|11\right>$$ gives:

$$ a_2\left|11\right> = -\left(\begin{matrix}
0 & 1 & 0 & 0\\
0 & 0 & 0 & 0\\
0 & 0 & 0 & 1\\
0 & 0 & 0 & 0
\end{matrix}\right)\left(\begin{matrix}
0\\
0\\
0\\
1
\end{matrix}\right) = -\left(\begin{matrix}
0\\
0\\
1\\
0
\end{matrix}\right) = -\left|10\right> $$

It should be clear now how second quantization can be formulated to be used as matrix-vector algebra.
