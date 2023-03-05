import matplotlib.pyplot as plt
import numpy as np
from matplotlib import transforms
from mpl_toolkits.axes_grid1 import make_axes_locatable
from numba import jit


@jit(nopython=True, cache=True)
def calculate_likelihood(observed: np.ndarray, mu: float, sigma: float) -> float:
    likelihood_of_data = 1
    for observation in observed:
        likelihood_of_data *= (
            1
            / (sigma**2 * 2 * np.pi) ** 0.5
            * np.exp(-0.5 * (observation - mu) ** 2 / sigma**2)
        )
    return likelihood_of_data


@jit(nopython=True, cache=True)
def calculate_marginal_likelihood(
    observed: np.ndarray,
    mu_values: np.ndarray,
    sigma_values: np.ndarray,
    prior: np.ndarray,
) -> float:
    integration_size_x = 1 / len(prior)
    integration_size_y = 1 / len(prior[0])
    integral = 0
    for (mu, prior_values) in zip(mu_values, prior):
        for (sigma, prior_value) in zip(sigma_values, prior_values):
            integral += calculate_likelihood(observed, mu, sigma)
    return integral * integration_size_x * integration_size_y


@jit(nopython=True, cache=True)
def calculate_posterior(
    observed: np.ndarray,
    mu_values: np.ndarray,
    sigma_values: np.ndarray,
    prior: np.ndarray,
) -> np.ndarray:
    posterior = np.zeros_like(prior)
    marginal_likelihood = calculate_marginal_likelihood(
        observed, mu_values, sigma_values, prior
    )
    for i, (mu, prior_values) in enumerate(zip(mu_values, prior)):
        for j, (sigma, prior_value) in enumerate(zip(sigma_values, prior_values)):
            posterior[i, j] = (
                calculate_likelihood(observed, mu, sigma)
                * prior_value
                / marginal_likelihood
            )
    return posterior


@jit(nopython=True, cache=True)
def calculate_crediable_region(
    posterior_: np.ndarray, crediable_threshold: float = 0.95
) -> tuple[np.ndarray, float, float, float, float]:
    posterior = np.copy(posterior_)
    integration_size_x = 1 / len(posterior)
    integration_size_y = 1 / len(posterior[0])
    crediable_region = np.zeros_like(posterior) + 1.01
    cummulated_integral = 0.0
    x_min = 10**10
    x_max = -(10**10)
    y_min = 10**10
    y_max = -(10**10)
    while cummulated_integral < crediable_threshold:
        max_arg = np.argmax(posterior)
        x = max_arg // len(posterior)
        y = max_arg - x * len(posterior)
        cummulated_integral += posterior[x, y] * integration_size_x * integration_size_y
        posterior[x, y] = 0.0
        crediable_region[x, y] = cummulated_integral
        x_min = min(x, x_min)
        x_max = max(x, x_max)
        y_min = min(y, y_min)
        y_max = max(y, y_max)
    return crediable_region, x_min, x_max, y_min, y_max


def calculate_unbiased_sigma(posterior: np.ndarray) -> np.ndarray:
    sigma_posterior = np.zeros(len(posterior[0]))
    integration_size_x = 1 / len(posterior)
    for i, mu_slice in enumerate(posterior.transpose()):
        sigma_posterior[i] += np.sum(mu_slice)
    return sigma_posterior * integration_size_x


def calculate_unbiased_mu(posterior: np.ndarray) -> np.ndarray:
    mu_posterior = np.zeros(len(posterior))
    integration_size_y = 1 / len(posterior[0])
    for i, sigma_slice in enumerate(posterior):
        mu_posterior[i] += np.sum(sigma_slice)
    return mu_posterior * integration_size_y


np.random.seed(10)

observed_values = np.random.normal(size=125)
grid_size = 400
mu_space = 3
sigma_space = 5
prior = np.ones((grid_size, grid_size))
mu_values = np.linspace(-mu_space, mu_space, grid_size)
sigma_values = np.linspace(0.001, sigma_space, grid_size)
posterior = calculate_posterior(observed_values[:5], mu_values, sigma_values, prior)
cr, x_min, x_max, y_min, y_max = calculate_crediable_region(posterior, 0.95)

# To make plot used:
#   https://matplotlib.org/stable/gallery/axes_grid1/scatter_hist_locatable_axes.html#sphx-glr-gallery-axes-grid1-scatter-hist-locatable-axes-py
#   https://stackoverflow.com/questions/22540449/how-can-i-rotate-a-matplotlib-plot-through-90-degrees

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, figsize=(6, 4))
cax = ax1.pcolormesh(sigma_values, mu_values, cr, cmap="gray")
ax1.plot(1, 0, "rx")
ax1.yaxis.set_tick_params(labelleft=False)
ax1.set_ylim(np.min(mu_values), np.max(mu_values))
ax1.set_xlim(0, np.max(sigma_values))
ax1.set_xlabel(r"$\sigma$")

divider = make_axes_locatable(ax1)
ax_top = divider.append_axes("top", 1.2, pad=0.1, sharex=ax1)
ax_left = divider.append_axes("left", 1.2, pad=0.1, sharey=ax1)
ax_top.xaxis.set_tick_params(labelbottom=False)

unbiased_sigma = calculate_unbiased_sigma(posterior)
ax_top.plot(sigma_values, unbiased_sigma)
ax_top.fill_between(
    sigma_values[y_min:y_max], unbiased_sigma[y_min:y_max], alpha=0.3, color="green"
)
ax_top.set_ylim(0, np.max(unbiased_sigma) * 1.05)

base = plt.gca().transData
rot = transforms.Affine2D().rotate_deg(270)
unbiased_mu = calculate_unbiased_mu(posterior)
ax_left.plot(-mu_values, unbiased_mu, transform=rot + base)
ax_left.fill_between(
    -mu_values[x_min:x_max],
    unbiased_mu[x_min:x_max],
    alpha=0.3,
    color="green",
    transform=rot + base,
)
ax_left.set_xlim(0, np.max(unbiased_mu) * 1.05)
ax_left.set_xlim(ax_left.get_xlim()[::-1])
ax_left.set_ylabel(r"$\mu$")

fig.colorbar(cax)
plt.savefig("gaussian_bayesian_5samples.png", dpi=400)

prior = np.ones((grid_size, grid_size))
mu_values = np.linspace(-mu_space, mu_space, grid_size)
sigma_values = np.linspace(0.001, sigma_space, grid_size)
posterior = calculate_posterior(observed_values[:25], mu_values, sigma_values, prior)
cr, x_min, x_max, y_min, y_max = calculate_crediable_region(posterior, 0.95)

# To make plot used:
#   https://matplotlib.org/stable/gallery/axes_grid1/scatter_hist_locatable_axes.html#sphx-glr-gallery-axes-grid1-scatter-hist-locatable-axes-py
#   https://stackoverflow.com/questions/22540449/how-can-i-rotate-a-matplotlib-plot-through-90-degrees

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, figsize=(6, 4))
cax = ax1.pcolormesh(sigma_values, mu_values, cr, cmap="gray")
ax1.plot(1, 0, "rx")
ax1.yaxis.set_tick_params(labelleft=False)
ax1.set_ylim(np.min(mu_values), np.max(mu_values))
ax1.set_xlim(0, np.max(sigma_values))
ax1.set_xlabel(r"$\sigma$")

divider = make_axes_locatable(ax1)
ax_top = divider.append_axes("top", 1.2, pad=0.1, sharex=ax1)
ax_left = divider.append_axes("left", 1.2, pad=0.1, sharey=ax1)
ax_top.xaxis.set_tick_params(labelbottom=False)

unbiased_sigma = calculate_unbiased_sigma(posterior)
ax_top.plot(sigma_values, unbiased_sigma)
ax_top.fill_between(
    sigma_values[y_min:y_max], unbiased_sigma[y_min:y_max], alpha=0.3, color="green"
)
ax_top.set_ylim(0, np.max(unbiased_sigma) * 1.05)

base = plt.gca().transData
rot = transforms.Affine2D().rotate_deg(270)
unbiased_mu = calculate_unbiased_mu(posterior)
ax_left.plot(-mu_values, unbiased_mu, transform=rot + base)
ax_left.fill_between(
    -mu_values[x_min:x_max],
    unbiased_mu[x_min:x_max],
    alpha=0.3,
    color="green",
    transform=rot + base,
)
ax_left.set_xlim(0, np.max(unbiased_mu) * 1.05)
ax_left.set_xlim(ax_left.get_xlim()[::-1])
ax_left.set_ylabel(r"$\mu$")

fig.colorbar(cax)
plt.savefig("gaussian_bayesian_25samples.png", dpi=400)

prior = np.ones((grid_size, grid_size))
mu_values = np.linspace(-mu_space, mu_space, grid_size)
sigma_values = np.linspace(0.001, sigma_space, grid_size)
posterior = calculate_posterior(observed_values, mu_values, sigma_values, prior)
cr, x_min, x_max, y_min, y_max = calculate_crediable_region(posterior, 0.95)

# To make plot used:
#   https://matplotlib.org/stable/gallery/axes_grid1/scatter_hist_locatable_axes.html#sphx-glr-gallery-axes-grid1-scatter-hist-locatable-axes-py
#   https://stackoverflow.com/questions/22540449/how-can-i-rotate-a-matplotlib-plot-through-90-degrees

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, figsize=(6, 4))
cax = ax1.pcolormesh(sigma_values, mu_values, cr, cmap="gray")
ax1.plot(1, 0, "rx")
ax1.yaxis.set_tick_params(labelleft=False)
ax1.set_ylim(np.min(mu_values), np.max(mu_values))
ax1.set_xlim(0, np.max(sigma_values))
ax1.set_xlabel(r"$\sigma$")

divider = make_axes_locatable(ax1)
ax_top = divider.append_axes("top", 1.2, pad=0.1, sharex=ax1)
ax_left = divider.append_axes("left", 1.2, pad=0.1, sharey=ax1)
ax_top.xaxis.set_tick_params(labelbottom=False)

unbiased_sigma = calculate_unbiased_sigma(posterior)
ax_top.plot(sigma_values, unbiased_sigma)
ax_top.fill_between(
    sigma_values[y_min:y_max], unbiased_sigma[y_min:y_max], alpha=0.3, color="green"
)
ax_top.set_ylim(0, np.max(unbiased_sigma) * 1.05)

base = plt.gca().transData
rot = transforms.Affine2D().rotate_deg(270)
unbiased_mu = calculate_unbiased_mu(posterior)
ax_left.plot(-mu_values, unbiased_mu, transform=rot + base)
ax_left.fill_between(
    -mu_values[x_min:x_max],
    unbiased_mu[x_min:x_max],
    alpha=0.3,
    color="green",
    transform=rot + base,
)
ax_left.set_xlim(0, np.max(unbiased_mu) * 1.05)
ax_left.set_xlim(ax_left.get_xlim()[::-1])
ax_left.set_ylabel(r"$\mu$")

fig.colorbar(cax)
plt.savefig("gaussian_bayesian_125samples.png", dpi=400)
