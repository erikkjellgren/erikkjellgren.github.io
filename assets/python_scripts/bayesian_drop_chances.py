from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.special import factorial


def likelihood(runs: int, hits: int, p: float) -> float:
    """Calculate the likelihood.

    Args:
      runs: Number of sample runs.
      hits: Number of positive sample runs.
      p: Model parameter.

    Returns:
      The likelihood.
    """
    return (
        factorial(runs)
        / (factorial(hits) * factorial(runs - hits))
        * p**hits
        * (1 - p) ** (runs - hits)
    )


def calcaulte_marginal_likelihood(
    runs: int, hits: int, prior: np.ndarray, p: np.ndarray
) -> np.ndarray:
    """Calculate the marginal likelihood.

    Args:
      runs: Number of sample runs.
      hits: Number of positive sample runs.
      prior: Probability density function of prior.
      p: Model parameter.

    Returns:
      The marginal likelihood.
    """
    integration_size = 1 / len(prior)
    integral = 0
    for (p_value, prior_value) in zip(p, prior):
        integral += likelihood(runs, hits, p_value) * prior_value
    return integral * integration_size


def calculate_posterior(
    runs: int, hits: int, prior: np.ndarray, p: np.ndarray
) -> np.ndarray:
    """Calculate the posterior.

    Args:
      runs: Number of sample runs.
      hits: Number of positive sample runs.
      prior: Probability density function of prior.
      p: Model parameter.

    Returns:
      The posterior probability density function.
    """
    posterior = np.zeros(len(prior))
    marginal_likelihood = calcaulte_marginal_likelihood(runs, hits, prior, p)
    for i, (p_value, prior_value) in enumerate(zip(p, prior)):
        posterior[i] = (
            likelihood(runs, hits, p_value) * prior_value / marginal_likelihood
        )
    return posterior


def calculate_confidence_interval(
    posterior: np.ndarray, confidence_level: float
) -> Tuple[float, float, int, int]:
    """Calculate confidence interval.

    Args:
      confidence_level: Confidence level as a decimal number.
      posterior: Probability density function of posterior.

    Returns:
      Confidence interval.
    """
    low = 1
    idx_low = 0
    high = 0
    idx_high = 0
    integral = 0
    integration_size = 1 / len(posterior)
    for idx in np.argsort(posterior)[::-1]:
        integral += posterior[idx] * integration_size
        if low > idx * integration_size:
            low = idx * integration_size
            idx_low = idx
        if high < idx * integration_size:
            high = idx * integration_size
            idx_high = idx
        if integral > confidence_level:
            break
    return low, high, idx_low, idx_high


plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

sampled_data = np.array(
    [
        1,
        1,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
    ]
)
prior = np.zeros(1000) + 1
p = np.linspace(0, 1, 1000)
posterior = calculate_posterior(len(sampled_data), np.sum(sampled_data), prior, p)
conf_low, conf_high, conf_idx1, conf_idx2 = calculate_confidence_interval(
    posterior, 0.95
)

fig, ax = plt.subplots(1, figsize=(6, 4))
ax.plot(p, posterior, color="blue", linewidth=3)
ax.fill_between(
    p[conf_idx1:conf_idx2], posterior[conf_idx1:conf_idx2], alpha=0.3, color="green"
)
ax.set_ylim(0, 5)
ax.set_xlim(0, 1)
ax.set_xlabel("p")
ax.set_ylabel("Probability Density")
plt.tight_layout()
plt.grid()
plt.savefig("bayesian_mysterious_stranger.svg")


fig, ax = plt.subplots(1, figsize=(6, 4))
fig.set_tight_layout(True)
ax.set_ylim(0, 5)
ax.set_xlim(0, 1)
ax.set_xlabel("p")
ax.set_ylabel("Probability Density")
plt.grid()

# Make first frame
sampled_data = np.array(
    [
        1,
        1,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
    ]
)
p = np.linspace(0, 1, 1000)
prior = np.linspace(0, 1, 1000)
posterior = calculate_posterior(
    len(sampled_data[:1]), np.sum(sampled_data[:1]), prior, p
)
conf_low, conf_high, conf_idx1, conf_idx2 = calculate_confidence_interval(
    posterior, 0.95
)
(probability_density_function,) = ax.plot(p, posterior, color="blue", linewidth=3)
ax.fill_between(
    p[conf_idx1:conf_idx2], posterior[conf_idx1:conf_idx2], alpha=0.3, color="green"
)


def update(i: int) -> None:
    """Update animiate.

    Args:
      i: frame number.
    """
    p = np.linspace(0, 1, 1000)
    prior = np.zeros(1000) + 1
    posterior = calculate_posterior(
        len(sampled_data[:i]), np.sum(sampled_data[:i]), prior, p
    )
    conf_low, conf_high, conf_idx1, conf_idx2 = calculate_confidence_interval(
        posterior, 0.95
    )
    probability_density_function.set_ydata(posterior)
    ax.collections.clear()
    ax.fill_between(
        p[conf_idx1:conf_idx2], posterior[conf_idx1:conf_idx2], alpha=0.3, color="green"
    )
    ax.set_title(
        f"Runs: {len(sampled_data[:i])}; Mysterious Strangers: {np.sum(sampled_data[:i])}"
    )


# Make animation
anim = FuncAnimation(
    fig, update, frames=np.arange(1, len(sampled_data) + 1), interval=300
)
anim.save("ms_bayesian.gif", dpi=400)
