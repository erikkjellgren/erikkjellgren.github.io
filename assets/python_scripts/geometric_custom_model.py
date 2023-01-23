import tempfile
from functools import partial

import geometric
import geometric.molecule
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


class CustomEngine(geometric.engine.Engine):
    def __init__(self, molecule, model_):
        super(CustomEngine, self).__init__(molecule)
        self.model = model_

    def calc_new(self, coords, dirname):
        energy, gradient = self.model(coords.reshape(-1, 3))
        return {"energy": energy, "gradient": gradient.ravel()}


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

    return m.xyzs[-1] * 1.8897259886, m.qm_energies[-1], m.qm_grads[-1]


run_customengine()
