import time

import matplotlib.pyplot as plt
import numpy as np
from numba import jit

odds = np.array(
    [
        3343185,
        31907,
        31907,
        5889,
        1963,
        116,
        58,
        24,
        11,
        6,
        2,
    ]
)

prizes = np.array(
    [
        25,
        50,
        100,
        500,
        1000,
        5000,
        10000,
        25000,
        50000,
        100000,
        1000000,
    ]
)

cum_odds = np.cumsum(odds)
total_bonds = np.sum(odds) * 24500

amounts = np.ceil(10 ** np.linspace(np.log10(25), np.log10(50000), 10))


@jit(nopython=True)
def run_simulation():
    odds = np.array(
        [
            3343185,
            31907,
            31907,
            5889,
            1963,
            116,
            58,
            24,
            11,
            6,
            2,
        ]
    )

    prizes = np.array(
        [
            25,
            50,
            100,
            500,
            1000,
            5000,
            10000,
            25000,
            50000,
            100000,
            1000000,
        ]
    )

    total_bonds = np.sum(odds) * 24500
    cum_odds = np.cumsum(odds)

    amounts = np.ceil(10 ** np.linspace(np.log10(25), np.log10(50000), 10))
    results = {}

    for amount in amounts:
        runs = np.zeros((100000, 12 * 10))
        for k in range(len(runs)):
            months = np.zeros(12 * 10)
            for i in range(len(months)):
                tickets = np.random.randint(1, total_bonds + 1, int(amount))
                for ticket in tickets:
                    if ticket > cum_odds[-1]:
                        continue
                    for j, odd in enumerate(cum_odds):
                        if ticket <= odd:
                            months[i] += prizes[j]
                            break
            runs[k] = months
        results[amount] = runs
    return results


results = run_simulation()


x = []
y = []
q2p5 = []
q97p5 = []

for key in results:
    x.append(key)
    y.append(np.median(np.sum(results[key], axis=1)))
    q2p5.append(np.quantile(np.sum(results[key], axis=1), 2.5 / 100))
    q97p5.append(np.quantile(np.sum(results[key], axis=1), 97.5 / 100))

y_cagr = []
q2p5_cagr = []
q97p5_cagr = []
for key, end_capital in zip(results, y):
    y_cagr.append((((end_capital + key) / key) - 1) / 10)
for key, end_capital in zip(results, q2p5):
    q2p5_cagr.append((((end_capital + key) / key) - 1) / 10)
for key, end_capital in zip(results, q97p5):
    q97p5_cagr.append((((end_capital + key) / key) - 1) / 10)
y_cagr = np.array(y_cagr)
q2p5_cagr = np.array(q2p5_cagr)
q97p5_cagr = np.array(q97p5_cagr)

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(
    [15, 100000],
    [
        np.sum(odds * prizes / total_bonds * 100 * 12),
        np.sum(odds * prizes / total_bonds * 100 * 12),
    ],
    "--",
    color="darkslategrey",
    label="Expected Return",
)
ax1.errorbar(
    x,
    y_cagr * 100,
    yerr=(y_cagr * 100 - q2p5_cagr * 100, q97p5_cagr * 100 - y_cagr * 100),
    fmt="o",
    color="purple",
    elinewidth=2,
    capsize=10,
    label="Simulated return",
)
ax1.set_xlim(18, 50000 * 25 / 18)
ax1.set_xscale("log")
ax1.set_ylabel("Annualized Return, %")
ax1.set_xlabel("Capital in Premium Bonds, £")
ax1.set_xticks(ticks=x[::3], labels=[int(i) for i in x[::3]])
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("simulated_premium_bonds_return.svg")


return_part = odds * prizes / total_bonds * 100 * 12

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))

colors = plt.cm.rainbow(np.linspace(0, 1, len(prizes)))
h = ax1.bar(0, return_part[0], label=f"{prizes[0]}£", color=colors[0])
handles = [h]
for i in range(1, len(return_part)):
    h = ax1.bar(
        0,
        return_part[i],
        bottom=np.sum(return_part[:i]),
        label=f"{prizes[i]}£",
        color=colors[i],
    )
    handles.append(h)

plt.legend(
    loc="center left", bbox_to_anchor=(1, 0.5), frameon=False, handles=handles[::-1]
)
ax1.set_ylabel("Annualized Return Contribution, %")
ax1.set_xticks([])
plt.tight_layout()
plt.savefig("premium_bonds_return_breakdown.svg")


fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.bar(
    np.linspace(1, len(odds), len(odds)),
    (1 - odds / total_bonds) ** (12 * 10 * 50000) * 100,
)
ax1.set_xticks(
    np.linspace(1, len(odds), len(odds)),
    [f"{prize}£" for prize in prizes],
    rotation=-45,
)
ax1.set_ylabel("Probability of not getting prize, %")
plt.tight_layout()
plt.savefig("premium_bonds_prize_likelihood.svg")
