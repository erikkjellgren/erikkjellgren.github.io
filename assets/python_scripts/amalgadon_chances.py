from typing import Callable, Union

import matplotlib.pyplot as plt
import numpy as np
from sympy import Rational


def P(adapts: int, num_uniques: int) -> Union[Callable[int, int], float]:  # type: ignore
    """Calculates the probability of getting a number of unique adapts, given a number of total adapts.

    Args:
      adapts: Number of adapts.
      num_uniques: Number of wanted unique adapts.

    Returns:
      The probability of getting a specific number of unique adapts, given the number of total adapts.
    """
    if adapts < 0:
        return 0
    elif adapts == 0 and num_uniques == 0:
        return 1
    elif num_uniques == 0:
        return Rational(4, 8) * P(adapts - 1, 0)
    elif num_uniques == 1:
        return Rational(4, 8) * P(adapts - 1, 0) + Rational(4, 7) * P(adapts - 1, 1)
    elif num_uniques == 2:
        return Rational(3, 7) * P(adapts - 1, 1) + Rational(4, 6) * P(adapts - 1, 2)
    elif num_uniques == 3:
        return Rational(2, 6) * P(adapts - 1, 2) + Rational(4, 5) * P(adapts - 1, 3)
    elif num_uniques == 4:
        return Rational(1, 5) * P(adapts - 1, 3) + Rational(4, 4) * P(adapts - 1, 4)


def specific(adapts: int) -> float:
    """Calculates the probability of getting a specific unique adapt.

    Args:
      adpats: Number of adapts.
    Returns:
      Probability of getting a specific unique adapt.
    """
    return (
        Rational(6, 24) * P(adapts, 1)
        + Rational(12, 24) * P(adapts, 2)
        + Rational(18, 24) * P(adapts, 3)
        + Rational(24, 24) * P(adapts, 4)
    )


def either(adapts: int) -> float:
    """Calculates the probability of getting a one or both of two unique adapts.

    Args:
      adpats: Number of adapts.
    Returns:
      Probability of getting a one or both of two unique adapts.
    """
    return (
        Rational(12, 24) * P(adapts, 1)
        + Rational(20, 24) * P(adapts, 2)
        + Rational(24, 24) * P(adapts, 3)
        + Rational(24, 24) * P(adapts, 4)
    )


def both(adapts: int) -> float:
    """Calculates the probability of getting two specific adapts.

    Args:
      adpats: Number of adapts.
    Returns:
      Probability of getting two specific adapts.
    """
    return (
        Rational(0, 24) * P(adapts, 1)
        + Rational(4, 24) * P(adapts, 2)
        + Rational(12, 24) * P(adapts, 3)
        + Rational(24, 24) * P(adapts, 4)
    )


DSorP = np.zeros(16)
Poison = np.zeros(16)
DSandP = np.zeros(16)
for i in range(0, 16):
    DSorP[i] = either(i)
    Poison[i] = specific(i)
    DSandP[i] = both(i)

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))

ax1.plot(np.linspace(0, 15, 16), DSorP, "go-", label="DS or P", markersize=7)
ax1.plot(np.linspace(0, 15, 16), Poison, "bo-", label="P", markersize=7)
ax1.plot(np.linspace(0, 15, 16), DSandP, "ro-", label="DS and P", markersize=7)

ax1.set_xlim(0, 15.5)
ax1.set_ylim(0, 1.05)
ax1.set_xticks(np.linspace(0, 15, 16, dtype=int))
ax1.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("Probability")
ax1.set_xlabel("Number of adaptations")
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("amalgadon_chances.svg")
