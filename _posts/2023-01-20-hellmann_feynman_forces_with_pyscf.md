---
layout: post
title: Hellmann-Feynman forces with PySCF
lang: en
lang-ref: Hellmann-Feynman forces with PySCF
tag: quantum
---

The [Hellmann-Feynman theorem](https://en.wikipedia.org/wiki/Hellmann%E2%80%93Feynman_theorem) states that:

$$ \frac{\mathrm{d}E}{\mathrm{d\lambda}} = \left<\psi\left|\frac{\mathrm{d}\hat{H}}{\mathrm{d}\lambda}\right|\psi\right> $$

It should be noted that for a finite basis this theorem does not hold, and might want to account for [Pulay forces](https://en.wikipedia.org/wiki/Pulay_stress).

For the molecular Hamiltonian:

$$ \hat{H} = -\frac{1}{2}\sum_i\nabla_i^2 - \sum_{iK}\frac{Z_K}{r_{iK}} + \sum_{K>L}\frac{Z_KZ_L}{\left|R_{KL}\right|} $$

When taking the derivative with respect to the nuclear coordinate it should be clear that:

$$ \left<\psi\left|\nabla_K\hat{H}\right|\psi\right> = -\left<\psi\left|\nabla_K\left(\sum_{iK}\frac{Z_K}{r_{iK}}\right)\right|\psi\right> + \nabla_K\left(\sum_{K>L}\frac{Z_KZ_L}{\left|R_{LK}\right|}\right) $$

Writing out the two contributions:

$$ -\left<\psi\left|\nabla_K\left(\sum_{iK}\frac{Z_K}{r_{iK}}\right)\right|\psi\right> = \left<\psi\left|\left(\sum_{iK}\frac{Z_Kr_{iK}}{r_{iK}^3}\right)\right|\psi\right> $$

and,

$$ \nabla_K\left(\sum_{K>L}\frac{Z_KZ_L}{\left|R_{LK}\right|}\right) = \left(\sum_{L\neq K}\frac{Z_KZ_LR_{LK}}{\left|R_{LK}\right|^3}\right) $$

[PySCF](https://github.com/pyscf/pyscf) uses [Libcint](https://github.com/sunqm/libcint) for integrals, and it can be seen in the [list of available integrals](https://github.com/sunqm/libcint/blob/master/scripts/auto_intor.cl) that the derivative of the nuclear attraction operator is unavailable (it is not there).
In general the available integrals uses the gradient with respect to the electron and not with respect to a nuclei.
However, we can realize that:

$$ \left<\psi\left|\nabla_e\left(\sum_{iK}\frac{Z_K}{r_{iK}}\right)\right|\psi\right> = \left<\psi\left|\left(\sum_{iK}\frac{Z_Kr_{iK}}{r_{iK}^3}\right)\right|\psi\right> = -\left<\psi\left|\nabla_K\left(\sum_{iK}\frac{Z_{K}}{r_{iK}}\right)\right|\psi\right> $$

We can thus write that:

$$ -\left<\psi\left|\nabla_K\left(\sum_{iK}\frac{Z_K}{r_{iK}}\right)\right|\psi\right> = \left<\psi\left|\nabla_e\left(\sum_{iK}\frac{Z_K}{r_{iK}}\right)\right|\psi\right> $$

Now again we have the problem that this integral with respect to the derivative of the electron coordinate is unavailable, but we can do one more rewrite using partial-integration.
Following the derivation done in a [previous post]({{ site.baseurl }}/2019/09/15/d_rinv_integrals/), we arrive at the following relation:

$$ \left<\psi\left|\nabla_e\left(\sum_{iK}\frac{Z_K}{r_{iK}}\right)\right|\psi\right> = -\left<\nabla_e\psi\left|\sum_{iK}\frac{Z_K}{r_{iK}}\right|\psi\right> -\left<\psi\left|\sum_{iK}\frac{Z_K}{r_{iK}}\right|\nabla_e\psi\right> $$

And these two integrals are available as "int1e_iprinv_sph".
The integral can now be computed as:

{% highlight python %}
mol.set_rinv_orig((origin))
grad_nuc_integral = -mol.intor("int1e_iprinv_sph") - mol.intor("int1e_iprinv_sph").transpose(0,2,1)
{% endhighlight %}

Obviously, the "mol" object needs to be created as usual with PySCF, and the "origin" will be center of the atom for which the gradient is calculated.

The integrals are calculated in AO-basis, thus to get the contribution to the nuclear gradient the integrals just need to be contracted with density matrix:

$$ \nabla_KE = \sum_{\mu,\nu}D_{\mu,\nu} \left(\nabla_KV_\mathrm{Ne}\right)_{\nu,\mu} $$

This contraction can easily be achived with "np.einsum()":

{% highlight python %}
rdm1 = mycas.make_rdm1()
nuc_grad_int = np.einsum('vu,iuv->i', rdm1, grad_nuc_integral)
{% endhighlight %}

Now the simple geometry optimizer can be programed.
Using PySCF molecule object the classical nuclear-nuclear repulsion gradient can be calculated as:

{% highlight python %}
def nuc_grad(mol_obj, nuc_idx):
    coord_nuc = mol_obj.atom_coord(nuc_idx)
    Z_nuc = mol_obj.atom_charge(nuc_idx)
    grad = np.zeros(3)
    for i, (coord, Z) in enumerate(zip(mol_obj.atom_coords(), mol_obj.atom_charges())):
        if i == nuc_idx:
            continue
        grad += Z*Z_nuc*(coord-coord_nuc)/(np.linalg.norm(coord-coord_nuc))**3
    return grad
{% endhighlight %}

Calculating the forces using the previous shown code snippets can be achived as:

{% highlight python %}
    # Calculate forces
    forces = np.zeros((mol.natm, 3))
    for atm_idx in range(mol.natm):
        origin = mol.atom_coord(atm_idx)
        mol.set_rinv_orig((origin))
        grad_nuc_integral = -mol.intor("int1e_iprinv_sph") - mol.intor("int1e_iprinv_sph").transpose(0,2,1)
        rdm1 = mycas.make_rdm1()

        nuc_grad_int = np.einsum('vu,iuv->i', rdm1, grad_nuc_integral)
        nuc_grad_classical = nuc_grad(mol, atm_idx)

        forces[atm_idx, :] = nuc_grad_int + nuc_grad_classical
{% endhighlight %}

And finally the forces can be applied to move the atoms.
The algorithm used here is the [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent).
Using gradient descent the coordinates are just updated with the size of the forces ($$\gamma=1$$):

$$ x_{n+1} = x_n - \gamma F $$

In code this can be implemented as:

{% highlight python %}
    # Move atoms and reconstruct molecule
    # Moving using gradient decent
    atom_str = ""
    for atm_idx in range(mol.natm):
        x = (mol.atom_coord(atm_idx)[0] - forces[atm_idx, 0])/1.8897259886
        y = (mol.atom_coord(atm_idx)[1] - forces[atm_idx, 1])/1.8897259886
        z = (mol.atom_coord(atm_idx)[2] - forces[atm_idx, 2])/1.8897259886
        atom_str += f"{mol.atom_symbol(atm_idx)} {x} {y} {z};"
{% endhighlight %}

A lot of details in the script has not been descriped in the above (only the very most important parts).
The full script can be found here: [hellmann_feynman_pyscf.py]({{ site.baseurl }}/assets/python_scripts/hellmann_feynman_pyscf.py)

To test if the method works, we can check that the optimizer finds the minima on the potential energy surface.

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/h2_pes_geoopt.svg">
</p>

Script to generate the plot can be found here: [hellmann_feynman_pyscf_pes_plot.py]({{ site.baseurl }}/assets/python_scripts/hellmann_feynman_pyscf_pes_plot.py)

As can be seen from the graph, the algorithm using Hellmann-Feynman forces seems to be able to find the minima on the potential energy surface of the hydrogen molecule.

## Pulay forces magnitude

Since we do not have a complete basis, it is known that the Hellmann-Feynman theorem does not hold.
We can see how big of an error we are making in the forces by finding the true forces using finite difference:

$$ \frac{\mathrm{d}f(x)}{\mathrm{d}x} \approx \frac{f(x+\epsilon)-f(x-\epsilon)}{2\epsilon} $$

Calculating the forces like this, and calculating the Hellmann-Feynman forces, they compare as follows:

<p align="center">
<img src="{{ site.baseurl }}/assets/plots/hf_forces_vs_true_forces.svg">
</p>

Script to generate the plot can be found here: [pulay_forces.py]({{ site.baseurl }}/assets/python_scripts/pulay_forces.py)

It can immidiately be seen from the plot that the Pulay forces are not always small compared to the Hellmann-Feynman forces.
Even more worrying it can also be noted that the Hellmann-Feynman forces does not find the exact minima.
