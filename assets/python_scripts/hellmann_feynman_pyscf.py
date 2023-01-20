import numpy as np
from pyscf import gto, mcscf, scf


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


mol = gto.Mole()
mol.atom = "H 0 0 0; H 2 0 0"
mol.basis = "cc-pVTZ"
mol.build()
mf = mol.RHF().run()
mycas = mcscf.CASSCF(mf, 2, (1, 1))

mycas.kernel()
e_old = mycas.e_tot

max_iterations = 100
for iteration in range(max_iterations):

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

    # Move atoms and reconstruct molecule
    # Moving using gradient decent
    atom_str = ""
    for atm_idx in range(mol.natm):
        x = (mol.atom_coord(atm_idx)[0] - forces[atm_idx, 0]) / 1.8897259886
        y = (mol.atom_coord(atm_idx)[1] - forces[atm_idx, 1]) / 1.8897259886
        z = (mol.atom_coord(atm_idx)[2] - forces[atm_idx, 2]) / 1.8897259886
        atom_str += f"{mol.atom_symbol(atm_idx)} {x} {y} {z};"

    mol.atom = atom_str
    mol.basis = "cc-pVTZ"
    mol.build()
    mf = mol.RHF().run()
    mycas = mcscf.CASSCF(mf, 2, (1, 1))

    mycas.kernel()
    if abs(e_old - mycas.e_tot) < 10**-5:
        print(iteration + 1)
        break
    e_old = mycas.e_tot
print(mol.atom_coords())
