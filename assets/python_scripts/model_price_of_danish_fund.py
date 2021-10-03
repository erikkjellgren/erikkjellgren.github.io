from typing import List

import matplotlib.pyplot as plt
import numpy as np


def fund_price(
    T: float, r: np.array, ks: List[float], b_case: int, k0: float = 100
) -> np.ndarray:
    """Calculates the fund price of a Danish investment fund.

    Args:
      T: Turnover rate.
      r: List of yearly returns, in decimal notation, i.e. 0.07 for 7%.
      ks: Previous fund prices.
      b_case: base-line price model.
              1, is a fixed base price.
              2, is an average base price.
              3, is a price-weighted average price.
      k0: base-line price (only relevant for b_case = 1).

    Returns:
      Estimate of fund price.
    """
    r = np.array(r)
    R = 1 + r
    N = len(r)
    k_out = [ks[-1]]
    for i in range(N):
        if b_case == 1:
            b = k0
        elif b_case == 2:
            b = np.mean(ks)
        elif b_case == 3:
            b = len(ks) / np.sum(1 / np.array(ks))
        k_new = k_out[i] * (R[i] - T * R[i]) + b * T * R[i]
        k_out.append(k_new)
        ks.append(k_new)
    return np.array(k_out)


sparindex = np.array(
    [100.5, 90.45, 115.2, 94.95, 116.10, 122.3, 126.45, 114.75, 151.55]
)
danskeinv = np.array([342, 288.5, 338.1, 263.2, 254.5, 226.4, 213.4, 162.1, 242.2])
# Last element in "old" is the first element in the above lists.
sparindex_old = np.array([100, 96.85, 100.5])
danskeinv_old = np.array(
    [100, 135, 95.7, 135.5, 160.0, 251.8, 254, 225.6, 146.6, 277.8, 316.8, 332, 342]
)
EM = np.array(
    [1056.59, 970.26, 993.1, 826.63, 978.22, 1212.95, 1096.36, 1052.68, 1320.98]
)
USDEURO = np.array([0.77, 0.72, 0.95, 0.91, 0.94, 0.80, 0.88, 0.89, 0.83])
EM = EM * USDEURO
EMp = (EM[1:] - EM[:-1]) / EM[:-1]

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

spar_m1 = fund_price(0.09, EMp - 0.5 / 100, [sparindex[0]], 1)
spar_m2 = fund_price(0.09, EMp - 0.5 / 100, sparindex_old.tolist(), 2)
spar_m3 = fund_price(0.09, EMp - 0.5 / 100, sparindex_old.tolist(), 3)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(spar_m1, "-o", linewidth=2, label="b_case=1")
ax1.plot(spar_m2, "-o", linewidth=2, label="b_case=2")
ax1.plot(spar_m3, "-o", linewidth=2, label="b_case=3")
ax1.plot(sparindex, "-o", linewidth=2, label="Acutal")
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("Fund price [DKK]")
ax1.set_xlabel("Year")
ax1.set_xticks(range(9))
ax1.set_xticklabels([2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
ax1.set_title("Sparinvest, INDEX Emerging Markets KL")
for tick in ax1.get_xticklabels():
    tick.set_rotation(45)
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("sparinvest_em.svg")

danske_m1 = fund_price(0.09, EMp - 1.63 / 100, [danskeinv[0]], 1)
danske_m2 = fund_price(0.09, EMp - 1.63 / 100, danskeinv_old.tolist(), 2)
danske_m3 = fund_price(0.09, EMp - 1.63 / 100, danskeinv_old.tolist(), 3)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(danske_m1, "-o", linewidth=2, label="b_case=1")
ax1.plot(danske_m2, "-o", linewidth=2, label="b_case=2")
ax1.plot(danske_m3, "-o", linewidth=2, label="b_case=3")
ax1.plot(danskeinv, "-o", linewidth=2, label="Acutal")
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("Fund price [DKK]")
ax1.set_xlabel("Year")
ax1.set_xticks(range(9))
ax1.set_xticklabels([2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
ax1.set_title("Danske Invest, Nye Markeder, klasse DKK d")
for tick in ax1.get_xticklabels():
    tick.set_rotation(45)
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("danskeinvest_em.svg")

spar_growth = np.array(
    [
        67.8,
        59.3,
        42.3,
        60.5,
        66,
        77.15,
        87.75,
        100.6,
        153.4,
        134.6,
        106.4,
        97.65,
        122.8,
        134.3,
        166.65,
    ]
)
USDEURO_long = np.array(
    [
        0.76,
        0.64,
        0.77,
        0.73,
        0.71,
        0.76,
        0.77,
        0.72,
        0.95,
        0.91,
        0.94,
        0.80,
        0.88,
        0.89,
        0.83,
    ]
)
nasdaq = np.array(
    [
        1726.03,
        1707.5,
        1064.7,
        1888.56,
        2359.96,
        2646.85,
        2804.11,
        3662.6,
        4399.23,
        4351.83,
        5373.48,
        6811.04,
        7015.69,
        8530.34,
        12668.51,
    ]
)
nasdaq = nasdaq * USDEURO_long
nasdaqp = (nasdaq[1:] - nasdaq[:-1]) / nasdaq[:-1]

spar_m1 = fund_price(0.25, nasdaqp - 0.5 / 100, [spar_growth[0]], 1, k0=65)
spar_m2 = fund_price(0.25, nasdaqp - 0.5 / 100, [spar_growth[0]], 2)
spar_m3 = fund_price(0.25, nasdaqp - 0.5 / 100, [spar_growth[0]], 3)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(spar_m1, "-o", linewidth=2, label="b_case=1")
ax1.plot(spar_m2, "-o", linewidth=2, label="b_case=2")
ax1.plot(spar_m3, "-o", linewidth=2, label="b_case=3")
ax1.plot(spar_growth, "-o", linewidth=2, label="Acutal")
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("Fund price [DKK]")
ax1.set_xlabel("Year")
ax1.set_xticks(range(15))
ax1.set_xticklabels(
    [
        2007,
        2008,
        2009,
        2010,
        2011,
        2012,
        2013,
        2014,
        2015,
        2016,
        2017,
        2018,
        2019,
        2020,
        2021,
    ]
)
ax1.set_title("Sparinvest, INDEX USA Growth KL")
for tick in ax1.get_xticklabels():
    tick.set_rotation(45)
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("sparinvest_growth.svg")

fig, ax1 = plt.subplots(1, 1, figsize=(6, 5))
Ts = np.linspace(0, 0.2, 9)
for t in Ts:
    ax1.plot(fund_price(t, [0.07] * 10, [100], 1), linewidth=3, label=f"T={t:2.2f}")
ax1.plot(
    fund_price(1 - 1 / 1.07, [0.07] * 10, [100], 1),
    linewidth=3,
    label=f"T={1-1/1.07:2.2f}",
)
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("Fund price [DKK]")
ax1.set_xlabel("Year")
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("model1_behaviour.svg")
