import matplotlib.pyplot as plt
import numpy as np
from pyscf import gto, mcscf


def nuc_grad(mol_obj, nuc_idx):
    coord_nuc = mol_obj.atom_coord(nuc_idx)
    Z_nuc = mol_obj.atom_charge(nuc_idx)
    grad = np.zeros(3)
    for i, (coord, Z) in enumerate(zip(mol_obj.atom_coords(), mol_obj.atom_charges())):
        if i == nuc_idx:
            continue
        grad += (
            Z * Z_nuc * (coord - coord_nuc) / (np.linalg.norm(coord - coord_nuc)) ** 3
        )
    return grad


forces = []
hf_forces = []
xs = np.linspace(1.4 - 0.2, 1.4 + 0.2, 20)
for x in xs:
    y = 0
    z = 0
    step = 10**-7

    mol = gto.Mole()
    mol.atom = f"H 0 0 0; H {x/1.8897259886+step} {y/1.8897259886} {z/1.8897259886}"
    mol.basis = "cc-pVTZ"
    mol.build()
    mf = mol.RHF().run()
    mycas = mcscf.CASSCF(mf, 2, (1, 1))
    mycas.kernel()
    e_positive = mycas.e_tot

    mol = gto.Mole()
    mol.atom = f"H 0 0 0; H {x/1.8897259886-step} {y/1.8897259886} {z/1.8897259886}"
    mol.basis = "cc-pVTZ"
    mol.build()
    mf = mol.RHF().run()
    mycas = mcscf.CASSCF(mf, 2, (1, 1))
    mycas.kernel()
    e_negative = mycas.e_tot

    forces.append((e_positive - e_negative) / (2 * step))

    mol = gto.Mole()
    mol.atom = f"H 0 0 0; H {x/1.8897259886} {y/1.8897259886} {z/1.8897259886}"
    mol.basis = "cc-pVTZ"
    mol.build()
    mf = mol.RHF().run()
    mycas = mcscf.CASSCF(mf, 2, (1, 1))
    mycas.kernel()
    origin = mol.atom_coord(1)
    mol.set_rinv_orig((origin))
    grad_nuc_integral = -mol.intor("int1e_iprinv_sph") - mol.intor(
        "int1e_iprinv_sph"
    ).transpose(0, 2, 1)
    rdm1 = mycas.make_rdm1()
    nuc_grad_int = np.einsum("vu,iuv->i", rdm1, grad_nuc_integral)
    nuc_grad_classical = nuc_grad(mol, 1)
    hf_forces.append(nuc_grad_int[0] + nuc_grad_classical[0])

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))

ax1.plot(xs, forces, "-", label="True forces")
ax1.plot(xs, hf_forces, "-", label="Hellmann-Feynman forces")
ax1.set_xlim(1.4 - 0.2, 1.4 + 0.2)
ax1.set_ylabel("Nuclear force [au]")
ax1.set_xlabel(r"$\mathrm{H}_2$ bond distance [bohr]")
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("hf_forces_vs_true_forces.svg")
