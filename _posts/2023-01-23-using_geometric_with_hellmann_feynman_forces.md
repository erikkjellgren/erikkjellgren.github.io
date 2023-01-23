---
layout: post
title: Using geomeTRIC with Hellmann-Feynman forces
lang: en
lang-ref: Using geomeTRIC with Hellmann-Feynman forces
tag: computation
---

In a [previous post]({{ site.baseurl }}/2023/01/20/hellmann_feynman_forces_with_pyscf/) the Hellmann-Feynman forces where calculated using [PySCF](https://github.com/pyscf/pyscf), and used [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent) to optimize the geometry of the molecule.

Geometry optimization is however a surprising hard problem to do, and writing algorithms from scratch might result in poorly behaved optimizations.
So instead let us an open-source library.
One of the freely available libraries for doing geometry optimization is [geomeTRIC](https://github.com/leeping/geomeTRIC).
Luckily, geomeTRIC has an example of how to use it using a [custom-made energy and gradient function](https://github.com/leeping/geomeTRIC/blob/548eb712210b2389aad7840192650d7c8ed8d13b/geometric/tests/test_customengine.py).
Let us now modify this one to work with the Hellmann-Feynman forces from PySCF.

The first step is define the custom model:

{% highlight python %}
def model_expanded_input(coords, atom_symbols):
    # Build molecule
    atom_str = ""
    for coord, atom_symbol in zip(coords, atom_symbols):
        x = coord[0] / 1.8897259886
        y = coord[1] / 1.8897259886
        z = coord[2] / 1.8897259886
        atom_str += f"{atom_symbol} {x} {y} {z};"

    mol = gto.Mole()
    mol.verbose = 0
    mol.atom = atom_str
    mol.basis = "cc-pVTZ"
    mol.build()
    mf = mol.RHF().run()
    mycas = mcscf.CASSCF(mf, 2, (1, 1))

    mycas.kernel()

    # Calculate forces
    forces = np.zeros((mol.natm, 3))
    for atm_idx in range(mol.natm):
        origin = mol.atom_coord(atm_idx)
        mol.set_rinv_orig((origin))
        grad_nuc_integral = -mol.intor("int1e_iprinv_sph") - mol.intor(
            "int1e_iprinv_sph"
        ).transpose(0, 2, 1)
        rdm1 = mycas.make_rdm1()
        nuc_grad_int = np.einsum("vu,iuv->i", rdm1, grad_nuc_integral)
        nuc_grad_classical = nuc_grad(mol, atm_idx)
        forces[atm_idx, :] = nuc_grad_int + nuc_grad_classical

    return mycas.e_tot, forces
{% endhighlight %}

The model for this case takes the input of the coordinates and the atom symbols, such that PySCF can construct the it's molecule object.
The energy and the forces are then calculated (forces are calculated as [describe previously]({{ site.baseurl }}/2023/01/20/hellmann_feynman_forces_with_pyscf/).
In the end the function only returns the total energy and the total forces on each nuclei.
From geomeTRIC it is expected that model() function will only take the coordinates as input, this will be fixed later in the script using [functools.partial](https://docs.python.org/3/library/functools.html#functools.partial).

Next the CustomEngine() class is constructed:

{% highlight python %}
class CustomEngine(geometric.engine.Engine):
    def __init__(self, molecule, model_):
        super(CustomEngine, self).__init__(molecule)
        self.model = model_

    def calc_new(self, coords, dirname):
        energy, gradient = self.model(coords.reshape(-1, 3))
        return {"energy": energy, "gradient": gradient.ravel()}
{% endhighlight %}

This one is identical to the one in the geomeTRIC example, execpt that the \_\_init\_\_ now takes in the variable model\_.
At last the driver call is defined:

{% highlight python %}
def run_customengine():
    molecule = geometric.molecule.Molecule()
    molecule.elem = ["H", "H"]
    molecule.xyzs = [
        np.array(
            (
                (0.0, 0.0, 0),
                (2.0, 0.0, 0),
            )
        )  # In Angstrom
    ]
    model = partial(model_expanded_input, atom_symbols=molecule.elem)

    customengine = CustomEngine(molecule, model)

    tmpf = tempfile.mktemp()
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmpf:
        m = geometric.optimize.run_optimizer(
            customengine=customengine, check=1, input=tmpf.name
        )

    return m.xyzs[-1] / 1.8897259886, m.qm_energies[-1], m.qm_grads[-1]


run_customengine()
{% endhighlight %}

What should be noted here is that 'model' is defined as 'partial(model_expanded_input, atom_symbols=molecule.elem)', and then passed to CustomEngine().
This way model() only takes in the coordinates as argument because the atom_symbols have now been fixed as a constant.

The full Python script can be found here: [geometric_custom_model.py]({{ site.baseurl }}/assets/python_scripts/geometric_custom_model.py)

Running this will give a total energy of -1.1515 Hartree, and an interatomic distance of 1.4408 bohr.
This is the same as was found using gradient descent (within convergence thresholds), -1.1515 Hartree and 1.4417 bohr.
