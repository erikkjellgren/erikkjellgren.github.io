import matplotlib.pyplot as plt
import numpy as np
import slowquant.SlowQuant as sq
from slowquant.unitary_coupled_cluster.linear_response import LinearResponseUCC
from slowquant.unitary_coupled_cluster.ucc_wavefunction import WaveFunctionUCC

mess_min = []
dist = []
xs = np.concatenate((np.linspace(0.2, 3.0, 60), np.linspace(1.5, 1.7, 20)))
for x in xs:
    SQobj = sq.SlowQuant()
    SQobj.set_molecule(
        f"""H 0.0 0.0 0.0;
            H {x} 0.0 0.0;""",
        distance_unit="angstrom",
    )
    SQobj.set_basis_set("STO-3G")

    Lambda_S, L_S = np.linalg.eigh(SQobj.integral.overlap_matrix)
    S_sqrt = np.dot(np.dot(L_S, np.diag(Lambda_S ** (-1 / 2))), np.transpose(L_S))

    h_core = (
        SQobj.integral.kinetic_energy_matrix + SQobj.integral.nuclear_attraction_matrix
    )
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

    kappas = np.linspace(0, np.pi, 200)
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
    w1100 = s1100**2
    w1010_0101 = (2 ** (-1 / 2) * (s1010 - s0101)) ** 2
    w0011 = s0011**2
    meassure = (
        -w1100 * np.log(w1100) - w1010_0101 * np.log(w1010_0101) - w0011 * np.log(w0011)
    )
    mess_min.append(np.min(meassure))
    dist.append(x)

energies_tot = []
for x in xs:
    SQobj = sq.SlowQuant()
    SQobj.set_molecule(
        f"""H 0.0 0.0 0.0;
            H {x} 0.0 0.0;""",
        distance_unit="angstrom",
    )
    SQobj.set_basis_set("STO-3G")

    Lambda_S, L_S = np.linalg.eigh(SQobj.integral.overlap_matrix)
    S_sqrt = np.dot(np.dot(L_S, np.diag(Lambda_S ** (-1 / 2))), np.transpose(L_S))

    h_core = (
        SQobj.integral.kinetic_energy_matrix + SQobj.integral.nuclear_attraction_matrix
    )
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
    WF.run_ucc("SD", False)
    energies_tot.append(WF.energy_elec + SQobj.molecule.nuclear_repulsion)

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))

w1100 = s1100**2
w1010_0101 = (2 ** (-1 / 2) * (s1010 - s0101)) ** 2
w0011 = s0011**2

sorting = np.argsort(xs)
dist = np.array(dist)
mess_min = np.array(mess_min)
energies_tot = np.array(energies_tot)
ax1.plot(dist[sorting], mess_min[sorting], color="tab:blue")
ax1.set_xlim(0.3, 3)
ax1.set_ylim(0, 0.5)
ax1.set_ylabel("Minimum entropy", color="tab:blue")
ax1.set_xlabel(r"$r_\mathrm{H_2}$ [Å]")

ax2 = ax1.twinx()
ax2.plot(dist[sorting], energies_tot[sorting], color="tab:red")
ax2.set_ylabel("Energy [Hartree]", color="tab:red")
ax2.set_ylim(-1.2, -0.6)

plt.tight_layout()
plt.savefig("h2_mc_scan.svg")
