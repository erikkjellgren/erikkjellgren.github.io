---
layout: post
title: Constructing FCI for H2 lazily
lang: en
lang-ref: Constructing FCI for H2 lazily
tag: quantum
---

The hydrogen molecule in a minimal basis (STO-3G as an example) will have a full CI Hamiltonian that is only four by four (using determinants that are singlet).

The four determintants in second quantization langauge are
$$\left|1100\right>$$, $$\left|1001\right>$$, $$\left|0110\right>$$, and, $$\left|0011\right>$$.

I.e. the full wavefunction will be:

$$ \left|\Psi\right> = c_1\left|1100\right> + c_2\left|1001\right> + c_3\left|0110\right> + c_4\left|0011\right> $$

The ground state energy can be found by diagonalizing the expectation value of the Hamiltonian with this wavefunction:

$$ \left<\Psi\left|H\right|\Psi\right> = \mathbf{H}\mathbf{c} = E\mathbf{c} $$

Here it is assumed that determinants are orthonormal.

From second quantization (see, [Molecular Electronic-Structure Theory](https://www.wiley.com/en-us/Molecular+Electronic+Structure+Theory-p-9781118531471)), we know these simple algebraric rules of second quantization the following:

An annihilation operator working on an occupied orbital will return and unoccupied:

$$ a_1\left|1\right> = \left|0\right>  $$

An annihilation operator working on an unoccupied orbital will return the oblivion state:

$$ a_1\left|0\right> = 0  $$

A creation operator working on an unoccupied orbital will return and unoccupied:

$$ a^\dagger_1\left|0\right> = \left|1\right>  $$

A creation operator working on an occupied orbital will return the oblivion state:

$$ a^\dagger_1\left|0\right> = 0  $$

And the last of the basis algebraic rules, if there is an uneven number of occupied orbitals to the left of the orbital being worked on a sign change will happen:

$$ a_4\left|1111\right> = -\left|1110\right> $$

To understand what is happening when evaluating something of the form
$$\left<\Phi\left|O\right|\Phi\right>$$, I think it is good to remember that:

$$ \left|1001\right> = a^\dagger_1 a^\dagger_4\left|0000\right> $$

The state $$\left|0000\right>$$ is also what is known as the vacuum state, $$\left|vac\right>$$.
And that the bra can be written as:

$$ \left<1001\right| = \left<0000\right| a_4 a_1 $$

Now when evaluating matrix elements between determinants we can just let all the operators work to to the right, keep track of the sign, and if we do not end up in the oblivion state we know we have a contribution.
As an example let us consider ground-state
($$\left|1100\right>$$) wih the ground-state, and use $$h_{22}a^\dagger_2 a_2$$ as the operator:

$$ \begin{eqnarray}
\left<1100\left|h_{22} a^\dagger_2 a_2\right|1100\right> &=& \left<vac\left|a_2 a_1 h_{22} a^\dagger_2 a_2 a^\dagger_1 a^\dagger_2\right|vac\right> \\
&=& h_{22}\left<0000\left|a_2 a_1 a^\dagger_2 a_2 a^\dagger_1 a^\dagger_2\right|0000\right> \\
&=& h_{22}\left<0000\left|a_2 a_1 a^\dagger_2 a_2 a^\dagger_1\right|0100\right> \\
&=& h_{22}\left<0000\left|a_2 a_1 a^\dagger_2 a_2\right|1100\right> \\
&=& -h_{22}\left<0000\left|a_2 a_1 a^\dagger_2\right|1000\right> \\
&=& h_{22}\left<0000\left|a_2 a_1 \right|1100\right> \\
&=& h_{22}\left<0000\left|a_2 \right|1000\right> \\
&=& h_{22}\left<0000\left| \right|0000\right> \\
&=& h_{22}
\end{eqnarray} $$

In the last step it is used that the determinants are orthonormal, thus
$$\left<0000\left| \right|0000\right>=1$$.
Here it should be noted that we will always end up with the vacuum-state on both the bra and ket, or we will get the oblivion state.
The whole procedure it thus to figure out the sign on $$h_{22}$$ or if the whole thing is zero.
It is now known that $$h_{22}$$ (if non-zero) will have a contribution to the matrix element that is the ground-state on the ground-state.

This is very cumbersome to do by hand and formulas that will make it easier also exists, but let us stick to this very simple method, and get some help from Python.
All we need is a function() that will evaluate a string of creation and annihilation operators on the ket vacuum-state.

First the operators can be constructed, here I am calling the annihilation 'a' and the creation 'c':

{% highlight python %}
class a:
    def __init__(self, idx):
        self.idx = idx
        self.dagger = False


class c:
    def __init__(self, idx):
        self.idx = idx
        self.dagger = True
{% endhighlight %}

All this does right now is to keep track of what orbital it works on the 'self.dagger' will be used to check if the operator is creation or annihilation.
Now let us write a function to apply the operators:

{% highlight python %}
def apply_operators(operators):
    state = [0,0,0,0]
    sign = 1
    # [::-1] to get the right most operator first,
    # such that it works as we expect when applying to the ket.
    for operator in operators[::-1]:
        if operator.dagger:
            if state[operator.idx-1] == 1:
                return 0
            if np.sum(state[:operator.idx-1])%2 != 0:
                sign *= -1
            state[operator.idx-1] = 1
        else:
            if state[operator.idx-1] == 0:
                return 0
            if np.sum(state[:operator.idx-1])%2 != 0:
                sign *= -1
            state[operator.idx-1] = 0
    return sign
{% endhighlight %}

What is worth to note is that:

{% highlight python %}
        if operator.dagger:
            if state[operator.idx-1] == 1:
                return 0
{% endhighlight %}

Will keep return the oblivion state if a creation operator is applied to an occupied orbital.
There is a similar part in the function for annihilation on an unoccupied staate.

To keep track of the sign, it is simply checked if the sum up to orbital is being worked on is an even number (an occupied orbital is represented by 1, and unoocupied by 0):

{% highlight python %}
            if np.sum(state[:operator.idx-1])%2 != 0:
                sign *= -1
{% endhighlight %}

Now before the operator pools are constructed, let us consider the problem at hand.
The operator between the determinants is the molecular Hamiltonian (in orthonormal spin basis).
The molecular Hamiltonian in second quantization is given as:

$$ H = \sum_{pq}h_{pq}a^\dagger_p a_q + \frac{1}{2}\sum_{pqrs}g_{pqrs}a^\dagger_p a^\dagger_q a_s a_r $$

Note here that for the second term the indicies $$s$$ and $$r$$ are flipped on the annihilation operators.
Here the integral elements are defined as:

$$ h_{pq} = \int\phi^\dagger_p(1)\hat{h}(1)\phi_q(1)\mathrm{d}r_1 $$

with the number indicating which electron the orbital is associted with, and, the two-electron integral being,

$$ g_{pqrs} = \int\phi^\dagger_p(1)\phi^\dagger_q(2)\hat{g}(1,2)\phi_r(1)\phi_s(2)\mathrm{d}r_1\mathrm{d}r_2 $$

Now the operator pools for the molecular Hamiltonian can be constructed:

{% highlight python %}
determinants = [[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 1, 1]]
for bra in determinants:
    for ket in determinants:
        bra_occ = []
        for i, occ in enumerate(bra):
            if occ == 1:
                bra_occ.append(i+1)
        ket_occ = []
        for i, occ in enumerate(ket):
            if occ == 1:
                ket_occ.append(i+1)

        operator_pool = []
        for p in range(4):
            for q in range(4):
                operator_pool.append([a(bra_occ[1]),a(bra_occ[0]),c(p+1),a(q+1),c(ket_occ[0]),c(ket_occ[1])])
{% endhighlight %}

The determinants are just fed in as a list that corrosponds to the state vector, and then the appropriate annihilation and creation operators are constructed from this.
All combinations of p and q are taking to construct all possible one-electron operators.
The last line is where the operator string is created using the classes defined earlier.
A very similar part is created in the code for the two-electron operator, just looping of pqrs instead.

The surviving terms can now be evaluated by looping over the operator pool, and using the function 'apply_operators()' that uses the second quantization algebra.

{% highlight python %}
        for operators in operator_pool:
            sign = apply_operators(operators)
            if sign != 0:
                idx1, idx2 = operators[2].idx, operators[3].idx
                print(f" {pm[sign]} h_{idx1}{idx2}", end="")
{% endhighlight %}

A similar part of the code does the same for the two-electron operator.
The full code can be found here: [lazy_second_quntization_algebra.py]({{ site.baseurl }}/assets/python_scripts/lazy_second_quntization_algebra.py)

Running the code, all the surviving terms (for now) can be found to be:

{% highlight text %}
<1100|H|1100> =  + h_11 + h_22 + 1/2 g_1212 - 1/2 g_1221 - 1/2 g_2112 + 1/2 g_2121
<1100|H|1001> =  + h_24 + 1/2 g_1214 - 1/2 g_1241 - 1/2 g_2114 + 1/2 g_2141
<1100|H|0110> =  - h_13 + 1/2 g_1223 - 1/2 g_1232 - 1/2 g_2123 + 1/2 g_2132
<1100|H|0011> =  + 1/2 g_1234 - 1/2 g_1243 - 1/2 g_2134 + 1/2 g_2143
<1001|H|1100> =  + h_42 + 1/2 g_1412 - 1/2 g_1421 - 1/2 g_4112 + 1/2 g_4121
<1001|H|1001> =  + h_11 + h_44 + 1/2 g_1414 - 1/2 g_1441 - 1/2 g_4114 + 1/2 g_4141
<1001|H|0110> =  + 1/2 g_1423 - 1/2 g_1432 - 1/2 g_4123 + 1/2 g_4132
<1001|H|0011> =  + h_13 + 1/2 g_1434 - 1/2 g_1443 - 1/2 g_4134 + 1/2 g_4143
<0110|H|1100> =  - h_31 + 1/2 g_2312 - 1/2 g_2321 - 1/2 g_3212 + 1/2 g_3221
<0110|H|1001> =  + 1/2 g_2314 - 1/2 g_2341 - 1/2 g_3214 + 1/2 g_3241
<0110|H|0110> =  + h_22 + h_33 + 1/2 g_2323 - 1/2 g_2332 - 1/2 g_3223 + 1/2 g_3232
<0110|H|0011> =  - h_24 + 1/2 g_2334 - 1/2 g_2343 - 1/2 g_3234 + 1/2 g_3243
<0011|H|1100> =  + 1/2 g_3412 - 1/2 g_3421 - 1/2 g_4312 + 1/2 g_4321
<0011|H|1001> =  + h_31 + 1/2 g_3414 - 1/2 g_3441 - 1/2 g_4314 + 1/2 g_4341
<0011|H|0110> =  - h_42 + 1/2 g_3423 - 1/2 g_3432 - 1/2 g_4323 + 1/2 g_4332
{% endhighlight %}

One worry can immediatly be noted, terms like <1100|H|1001> seem to be non-zero which is a not what we expect from [Brillouin's theorem](https://en.wikipedia.org/wiki/Brillouin%27s_theorem).
The terms are not yet evaluated, so they might still be zero, and Brillouin's theorem might not be violated.
If we consider the value of the intgrals $$h_{pq}$$ and $$g_{pqrs}$$ (removing zero valued $$h_{pq}$$ and zero valued $$g_{pqrs}$$), then all surving non-zero terms are:

{% highlight text %}
<1100|H|1100> =  + h_11 + h_22 + 1/2 g_1212 + 1/2 g_2121
<1100|H|1001> =
<1100|H|0110> =
<1100|H|0011> =  + 1/2 g_1234 + 1/2 g_2143
<1001|H|1100> =
<1001|H|1001> =  + h_11 + h_44 + 1/2 g_1414 + 1/2 g_4141
<1001|H|0110> =  - 1/2 g_1432 - 1/2 g_4123
<1001|H|0011> =
<0110|H|1100> =
<0110|H|1001> =  - 1/2 g_2341 - 1/2 g_3214
<0110|H|0110> =  + h_22 + h_33 + 1/2 g_2323 + 1/2 g_3232
<0110|H|0011> =
<0011|H|1100> =  + 1/2 g_3412 + 1/2 g_4321
<0011|H|1001> =
<0011|H|0110> =
<0011|H|0011> =  + h_33 + h_44 + 1/2 g_3434 + 1/2 g_4343
{% endhighlight %}

The modified code that includes the integrals can be found here: [lazy_second_quntization_algebra_with_int.py]({{ site.baseurl }}/assets/python_scripts/lazy_second_quntization_algebra_with_int.py)

In the code top of the code the integrals are calculated using an external quantum chemistry program and then converted first converted to MO-basis and then afterwards converted to spin-basis.
The details about this is out-of-scope for this.

Allready now Brillouin's theorem is recovered.

Instead of printing the terms, the nummerical value can just be placed in a matrix (Hamiltonian matrix).
And the FCI energy can be found by diagonalizing it.

The modified version of the code that does this can be found here: [lazy_second_quntization_algebra_fci.py]({{ site.baseurl }}/assets/python_scripts/lazy_second_quntization_algebra_fci.py)

Running this code it found that the FCI electronic energy (this is E\_HF + E\_corr) is -1.8510463 Hartree.
The Hamiltonian is ordering
($$\left|1100\right>$$, $$\left|1001\right>$$, $$\left|0110\right>$$, $$\left|0011\right>$$):

$$ H^\mathrm{FCI} = \left(\begin{matrix}
-1.83 & 0. &    0.   &  0.181\\
 0.  &  -1.065 & -0.181 & 0.   \\
 0.  &  -0.181 & -1.065 & 0.   \\
 0.181 & 0. &    0. &   -0.254
\end{matrix}\right) $$

One very notable feature of the FCI Hamiltonian for hydrogen in a minimal basis, is that single excited determinants does not contribute to the energy of the ground-state.

The FCI energy for hydrogen in a minimal basis can thus be found by only considering the ground-state and the double excitated state
($$\left|1100\right>$$, $$\left|0011\right>$$), just giving a two by two Hamiltonian:

$$ H^\mathrm{FCI} = \left(\begin{matrix}
-1.83  & 0.181\\
 0.181 & -0.254
\end{matrix}\right) $$

This also means that for the FCI of hydrogen in a minimal basis the only contributing integrals are giving by:

{% highlight text %}
<1100|H|1100> =  + h_11 + h_22 + 1/2 g_1212 + 1/2 g_2121
<1100|H|0011> =  + 1/2 g_1234 + 1/2 g_2143
<0011|H|1100> =  + 1/2 g_3412 + 1/2 g_4321
<0011|H|0011> =  + h_33 + h_44 + 1/2 g_3434 + 1/2 g_4343
{% endhighlight %}

For why this particular Hamiltonian behaves like this see: [Modern Quantum Chemistry: Introduction to Advanced Electronic Structure Theory](https://www.amazon.com/Modern-Quantum-Chemistry-Introduction-Electronic/dp/0486691861)
