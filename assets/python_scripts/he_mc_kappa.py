import matplotlib.pyplot as plt
import numpy as np
import slowquant.SlowQuant as sq
from slowquant.unitary_coupled_cluster.ucc_wavefunction import WaveFunctionUCC

SQobj = sq.SlowQuant()
SQobj.set_molecule(
    """He 0.0 0.0 0.0;""",
    distance_unit="angstrom",
)
SQobj.set_basis_set("6-31G")

Lambda_S, L_S = np.linalg.eigh(SQobj.integral.overlap_matrix)
S_sqrt = np.dot(np.dot(L_S, np.diag(Lambda_S ** (-1 / 2))), np.transpose(L_S))

h_core = SQobj.integral.kinetic_energy_matrix + SQobj.integral.nuclear_attraction_matrix
g_eri = SQobj.integral.electron_repulsion_tensor
WF = WaveFunctionUCC(
    SQobj.molecule.number_bf * 2,
    SQobj.molecule.number_electrons,
    (2, 2),
    S_sqrt,
    h_core,
    g_eri,
    include_active_kappa=True,
)

kappas = np.linspace(0, np.pi, 300)
energies = []
s1100 = []
s1010 = []
s0101 = []
s0011 = []

for kappa in kappas:
    WF.kappa = [kappa]
    WF.run_ucc("SD", False)
    energies.append(WF.energy_elec + SQobj.molecule.nuclear_repulsion)
    s1100.append(WF.state_vector.active[12])
    s0101.append(WF.state_vector.active[9])
    s1010.append(WF.state_vector.active[6])
    s0011.append(WF.state_vector.active[3])
s1100 = np.array(s1100)
s1010 = np.array(s1010)
s0101 = np.array(s0101)
s0011 = np.array(s0011)

SQobj = sq.SlowQuant()
SQobj.set_molecule(
    """He 0.0 0.0 0.0;""",
    distance_unit="angstrom",
)
SQobj.set_basis_set("6-31G")
SQobj.init_hartree_fock()
SQobj.hartree_fock.run_restricted_hartree_fock()
h_core = SQobj.integral.kinetic_energy_matrix + SQobj.integral.nuclear_attraction_matrix
g_eri = SQobj.integral.electron_repulsion_tensor
WF = WaveFunctionUCC(
    SQobj.molecule.number_bf * 2,
    SQobj.molecule.number_electrons,
    (2, 2),
    SQobj.hartree_fock.mo_coeff,
    h_core,
    g_eri,
    include_active_kappa=True,
)
WF.run_ucc("SD", False)
hf_orbidx = np.argmin(np.abs(s1100 - WF.state_vector.active[12]))

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 5))

ax1.plot((0, np.pi), (0, 0), "--", color="grey", alpha=0.4)
ax1.plot(kappas, s1100, label=r"$\left|1100\right>$")
ax1.plot(
    kappas,
    2 ** (-1 / 2) * (s1010 - s0101),
    label=r"$\frac{1}{\sqrt{2}}\left(\left|1001\right> - \left|0110\right>\right)$",
)
ax1.plot(kappas, s0011, label=r"$\left|0011\right>$")
ax1.plot(
    (kappas[hf_orbidx], kappas[hf_orbidx]),
    (-1, 1),
    "k--",
    label="Hartree-Fock orbitals",
)

ax1.set_xlabel(r"$\kappa}$")
ax1.set_ylabel("CI coefficient")
ax1.set_xlim(0, np.pi)
ax1.set_ylim(-1, 1)
plt.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.25), ncols=2)
plt.tight_layout()
plt.savefig("he_mc_vs_kappa.svg")

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))

w1100 = s1100**2
w1010_0101 = (2 ** (-1 / 2) * (s1010 - s0101)) ** 2
w0011 = s0011**2
entropy = (
    -w1100 * np.log(w1100) - w1010_0101 * np.log(w1010_0101) - w0011 * np.log(w0011)
)

ax1.plot(kappas, entropy)
ax1.set_xlabel(r"$\kappa$")
ax1.set_ylabel("Entropy")
ax1.set_xlim(0, np.pi)
ax1.set_ylim(0, 1)
plt.tight_layout()
plt.savefig("he_entropy_vs_kappa.svg")
