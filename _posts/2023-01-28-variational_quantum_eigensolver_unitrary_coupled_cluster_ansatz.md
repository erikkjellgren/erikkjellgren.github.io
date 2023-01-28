---
layout: post
title: Variational quantum eigensolver unitrary coupled cluster ansatz
lang: en
lang-ref: Variational quantum eigensolver unitrary coupled cluster ansatz
tag: computation
---

In a [previous post]({{ site.baseurl }}/2023/01/27/jordan_wigner_hamiltonian_for_hydrogen) the Jordan-Wigner representation of the molecular Hamiltonian for the hydrogen molecule was constructed.
This Hamiltonian was solved explicit diagonalization.
The method of explicit diagonalization quickly becomes computationally impossible when the dimension of the Hamiltonian grow, and cannot be implemented on quantum computers.

A scheme that can be utilized by quantum computers is the [variational quantum eigensolver](https://en.wikipedia.org/wiki/Variational_quantum_eigensolver) (VQE).
The first requirement of VQE is that we have to represent the fermionic operators as Pauli operators, this is what was achived using the Jordan-Wigner representation.
The second requirement is that an ansatz has to be defined.
A choice of ansatz is the unitrary coupled cluster with singles and doubles (UCCSD).
The UCCSD ansatz is defined as:

$$ \left|\Psi(\theta)\right> = U(\theta)\left|\psi\right> = \exp\left(T(\theta) - T^\dagger(\theta)\right)\left|\phi\right> $$

With the cluster operator $$T(\theta)$$ being:

$$ T(\theta) = \sum_k\ ^{(k)}T(\theta) $$

For the UCCSD ansatz $$k = \{1,2\}$$, with:

$$ \begin{align}
^{(1)}T(\theta) &= \sum_{\substack{i_1\in occ\\ a_1\in virt}}\theta_{i_1}^{a_1} a^\dagger_{a_1} a_{i_1}\\
^{(2)}T(\theta) &= \frac{1}{4}\sum_{\substack{i_1,i_2\in occ\\ a_1,a_2\in virt}}\theta_{i_1,i_2}^{a_1,a_2} a^\dagger_{a_2} a_{i_2} a^\dagger_{a_1} a_{i_1}
\end{align} $$

Again all of the fermionic need to be translated to Pauli matrices.
Doing it by hand is to cumbersome, so once again Python will assist with the Jordan-Wigner representation of the UCCSD ansatz.
The script used to generate to UCCSD ansatz can be found here: [construct_uccsd_jordan_wigner.py]({{ site.baseurl }}/assets/python_scripts/construct_uccsd_jordan_wigner.py)

The UCCSD ansatz for this particular system is now:

{% highlight python %}
def uccsd_anzats(theta):
    theta_31 = theta[0]
    theta_32 = theta[1]
    theta_41 = theta[2]
    theta_42 = theta[3]
    theta_4321 = theta[4]
    theta_4312 = theta[5]
    theta_3421 = theta[6]
    theta_3412 = theta[7]

    T = np.zeros((16,16))*0.j
    T += theta_31*(+0.5j*krons([Y, I, X, I])-0.5j*krons([X, I, Y, I]))
    T += theta_32*(+0.5j*krons([I, Y, X, I])-0.5j*krons([I, X, Y, I]))
    T += theta_41*(+0.5j*krons([Y, I, I, X])-0.5j*krons([X, I, I, Y]))
    T += theta_42*(+0.5j*krons([I, Y, I, X])-0.5j*krons([I, X, I, Y]))
    T += theta_4321*(+0.03125j*krons([X, Y, X, X])-0.03125j*krons([X, X, X, Y])+0.03125j*krons([Y, X, X, X])+0.03125j*krons([Y, Y, X, Y])-0.03125j*krons([X, X, Y, X])-0.03125j*krons([X, Y, Y, Y])+0.03125j*krons([Y, Y, Y, X])-0.03125j*krons([Y, X, Y, Y]))
    T += theta_4312*(+0.03125j*krons([Y, X, X, X])-0.03125j*krons([X, X, X, Y])+0.03125j*krons([X, Y, X, X])+0.03125j*krons([Y, Y, X, Y])-0.03125j*krons([X, X, Y, X])-0.03125j*krons([Y, X, Y, Y])+0.03125j*krons([Y, Y, Y, X])-0.03125j*krons([X, Y, Y, Y]))
    T += theta_3421*(+0.03125j*krons([X, Y, X, X])-0.03125j*krons([X, X, Y, X])+0.03125j*krons([Y, X, X, X])+0.03125j*krons([Y, Y, Y, X])-0.03125j*krons([X, X, X, Y])-0.03125j*krons([X, Y, Y, Y])+0.03125j*krons([Y, Y, X, Y])-0.03125j*krons([Y, X, Y, Y]))
    T += theta_3412*(+0.03125j*krons([Y, X, X, X])-0.03125j*krons([X, X, Y, X])+0.03125j*krons([X, Y, X, X])+0.03125j*krons([Y, Y, Y, X])-0.03125j*krons([X, X, X, Y])-0.03125j*krons([Y, X, Y, Y])+0.03125j*krons([Y, Y, X, Y])-0.03125j*krons([X, Y, Y, Y]))
    return scipy.linalg.expm(T)
{% endhighlight %}

Here the 'krons()' is just a custom made function that contracts $$A_1\otimes A_2\otimes ... \otimes A_n$$ into a single matrix.
It should be noted that even for this small system, hydrogen in a minimal basis, we are left with eight $$\theta$$-parameters for the optimization, tho we might expect that the parameters from $$^{(1)}T$$ will not change during the optimization, because single excitations does not contribute to the ground-state energy for this particular system.

All there is left to do is minimize the energy.
The energy is given as:

$$ E = \frac{\left<\psi\left|U(\theta)H^\mathrm{JW}U(\theta)\right|\psi\right>}{\left<\psi U^\dagger(\theta)\left|U(\theta)right. psi\right>} $$

Since our ansatz for is unitray we know that $$\left<\psi U^\dagger(\theta)\left|U(\theta)right. psi\right>$$ for all possible $$\theta$$, thus expression for the energy simplifies to:

$$ E = \left<\psi\left|U(\theta)H^\mathrm{JW}U(\theta)\right|\psi\right> $$

To evaluate this expression let us remember that the Hamiltonian has the form:

$$ H^\mathrm{JW} = f_1(I\otimes I\otimes I\otimes I) + f_2(Z\otimes I\otimes I\otimes I) + ... $$

Or in a more compact notation, a sum of Pauli strings:

$$ H^\mathrm{JW} = \sum_i f_iP_i $$

Thus inserting into the energy expression it is found:

$$ \begin{align}
E &= f_1\left<\psi\left|(I\otimes I\otimes I\otimes I)\right|\psi\right>  + f_2\left<\psi\left|(Z\otimes I\otimes I\otimes I)\right|\psi\right>  + ...\\
&= \sum_i f_i \left<\psi\left|P_i\right|\psi\right>
\end{align} $$

The energy is now the sum of expectation values of the individual Pauli strings weighted with some factor.

{% highlight python %}
def total_energy(theta):
    E_tot = np.zeros((16,16))*0.j
    for paulis, factor in pauli_strings.items():
        pauli_string = []
        for pauli in paulis:
            if pauli == 'I':
                pauli_string.append(I)
            elif pauli == 'X':
                pauli_string.append(X)
            elif pauli == 'Y':
                pauli_string.append(Y)
            elif pauli == 'Z':
                pauli_string.append(Z)
        UCCSD = uccsd_anzats(theta)
        UCCSD_dagger = np.conj(uccsd_anzats(theta)).T
        E = factor*np.matmul(UCCSD_dagger, np.matmul(krons(pauli_string), UCCSD))
        E_tot += E
    return np.min(np.real(E_tot))
{% endhighlight %}

Putting it all together in a Python script and using 'scipy.minimize' to find the optimal parameters, it is found that the ground-state energy is indeed again -1.85105 Hartree (just as for FCI).
The Python script can be found here: []()

Starting from $$\theta=0$$, the optimal $$\theta$$'s are found to be [ 0.       0.       0.       0.      -0.11306 -0.11306 -0.11306 -0.11306].
Indeed as expected the first four parameters stayed zero.
The last four parameters was found to be the same value, this lead one to wonder if the hydrogen molecule in a minimal basis could be described by a single parameter.

## Trotterization

In general it is a hard task to convert exponental to a quantum circuit with the exponential is a sum of terms.
This is the motivation for doing trotterization.
To first order the trotterization is given as:

$$ \exp(\sum_if_iP_i) \approx \prod_i\exp(f_iP_i) $$
