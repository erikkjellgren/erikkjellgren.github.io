import matplotlib.pyplot as plt
import numpy as np
from pyscf import gto, mcscf

energies = []
xs = np.linspace(1.4 - 0.2, 1.4 + 0.2, 100)
for x in xs:
    y = 0
    z = 0
    mol = gto.Mole()
    mol.atom = f"H 0 0 0; H {x/1.8897259886} {y/1.8897259886} {z/1.8897259886}"
    mol.basis = "cc-pVTZ"
    mol.build()
    mf = mol.RHF().run()
    mycas = mcscf.CASSCF(mf, 2, (1, 1))

    mycas.kernel()
    energies.append(mycas.e_tot)

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))

ax1.plot(xs, energies, "-", label=r"$\mathrm{H}_2$ potential energy surface")
ax1.plot(
    2.61056706e00 - 1.16889253e00, -1.15151519062468, "o", label="Optimizer minima"
)
ax1.set_xlim(1.4 - 0.2, 1.4 + 0.2)
ax1.set_ylabel("Total Energy [Hartree]")
ax1.set_xlabel(r"$\mathrm{H}_2$ bond distance [bohr]")
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("h2_pes_geoopt.svg")
