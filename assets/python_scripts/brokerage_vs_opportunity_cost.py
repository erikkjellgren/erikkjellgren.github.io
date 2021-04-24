import matplotlib.pyplot as plt
import numpy as np


def N_opt(k: float, r_m: float, p: float) -> float:
    """Calculates the number of months between each investment.

    Args:
      k: capital.
      r_m: monthly return.
      p: brokerage as fixed value.

    Returns:
      Montly frequency.
    """
    return np.ceil((p + p / r_m) / k)


def k_min(r_m: float, p: float) -> float:
    """Calculates minimum required capital 
    for return to outweigh brokerage.

    Args:
      k: capital.
      p: brokerage as fixed value.

    Returns:
      Minimum capital.
    """

    return p + p / r_m


plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))

ks = np.linspace(65, 540, 10000)
N5 = np.zeros(len(ks))
N7 = np.zeros(len(ks))
N9 = np.zeros(len(ks))
for j, k_ in enumerate(ks):
    N5[j] = N_opt(k_, (1 + 0.05) ** (1 / 12) - 1, 2)
    N7[j] = N_opt(k_, (1 + 0.07) ** (1 / 12) - 1, 2)
    N9[j] = N_opt(k_, (1 + 0.09) ** (1 / 12) - 1, 2)
ax1.plot(ks, N9, label="CAGR = 9%", linewidth=3)
ax1.plot(ks, N7, label="CAGR = 7%", linewidth=3)
ax1.plot(ks, N5, label="CAGR = 5%", linewidth=3)

ax1.set_xlabel("Monthly capital, Euro")
ax1.set_ylabel(r"$N_\mathrm{opt}$, months")
ax1.legend()
ax1.grid(which="minor")
ax1.grid(which="major")

plt.tight_layout()
plt.savefig("brokerage_vs_oppertunity_cost.svg")


fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))

r_y = np.linspace(0.02, 0.2, 10000)
r = (1 + r_y) ** (1 / 12) - 1
ax1.plot(r_y * 100, k_min(r, 2), linewidth=3)

ax1.set_ylabel("Minimum capitial, Euro")
ax1.set_xlabel(r"CAGR, %")
ax1.grid(which="minor")
ax1.grid(which="major")

plt.tight_layout()
plt.savefig("capital_vs_return.svg")
