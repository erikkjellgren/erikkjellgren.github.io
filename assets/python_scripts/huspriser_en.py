import dkfinance_modeller.utility.formler as formler
import matplotlib.pyplot as plt
import numpy as np

huspris = np.genfromtxt("data/huspriser_danmark.txt")
huspris_indeks = huspris / huspris[0]

labels = np.genfromtxt("data/labels.txt", dtype=str, delimiter=",")
for i in range(len(labels)):
    labels[i] = labels[i].replace("1. kv.", "Q1")

langrente = np.genfromtxt("data/langrente.txt", delimiter=",")
langrente_min = np.zeros(len(langrente))
mindste = 10
for i, rente in enumerate(langrente):
    mindste = min(mindste, rente)
    langrente_min[i] = mindste

lønstigning = np.genfromtxt("data/loenstigning.txt")
lønstigning = (1 + lønstigning / 100) ** (3 / 12) - 1
løn_indeks = [1]
for stigning in lønstigning[1:]:
    løn_indeks.append(løn_indeks[-1] * (1 + stigning))

husomkostninger = []
husomkostninger_min = []
for rente, rente_min, pris in zip(langrente, langrente_min, huspris):
    husomkostninger.append(
        formler.afbetalling(klån=pris * 0.8, n=30, r=rente / 100 + 10**-6) * 30
        + 0.2 * pris
    )
    husomkostninger_min.append(
        formler.afbetalling(klån=pris * 0.8, n=30, r=rente_min / 100 + 10**-6) * 30
        + 0.2 * pris
    )
husomkostninger_indeks = husomkostninger / husomkostninger[0]
husomkostninger_min_indeks = husomkostninger_min / husomkostninger_min[0]

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, (ax2, ax1) = plt.subplots(2, 1, figsize=(6, 7), sharex=True)
ax1.plot(labels, huspris_indeks, "m-", label="House price index")
ax1.plot(
    labels,
    husomkostninger_min_indeks,
    "r--",
    label="House purchase costs index (min. interest)",
)
ax1.plot(labels, husomkostninger_indeks, "k-", label="House purchase costs index")
ax1.plot(labels, løn_indeks, "g-", label="Wage index")
ax1.legend(frameon=False)

ax2.plot(labels, langrente_min, "r--", label="Long interest rate minimum")
ax2.plot(labels, langrente, "k--", label="Long interest rate")
ax2.set_ylim(-1.0, 9.5)
ax2.set_ylabel("Long interest rate")
ax2.legend(frameon=False)

for i, tick in enumerate(ax1.get_xticklabels()):
    tick.set_rotation(90)
    if i % 4 != 0:
        tick.set_fontsize(0)
        tick.set_color("white")

ax1.set_xlim(-1, len(labels) + 1)
ax1.set_ylim(0.9, 4.0)
ax1.set_ylabel("Index value")
plt.tight_layout()
plt.savefig("huspris_indekser_en.svg")

huspris = np.genfromtxt("data/huspriser_danmark.txt")
københavn = np.genfromtxt("data/huspriser_koebenhavn.txt")
odense = np.genfromtxt("data/huspriser_odense.txt")
aarhus = np.genfromtxt("data/huspriser_aarhus.txt")
aalborg = np.genfromtxt("data/huspriser_aalborg.txt")
langeland = np.genfromtxt("data/huspriser_langeland.txt")
lolland = np.genfromtxt("data/huspriser_lolland.txt")
fig, ax1 = plt.subplots(1, 1, figsize=(6, 4), sharex=True)
ax1.plot(labels, huspris_indeks, "m-", label="Denmark index")
ax1.plot(labels, københavn / københavn[0], "k--", label="Copenhagen index")
ax1.plot(labels, odense / odense[0], "b--", label="Odense index")
ax1.plot(labels, aarhus / aarhus[0], "g--", label="Aarhus index")
ax1.plot(labels, aalborg / aalborg[0], "r--", label="Aalborg index")
ax1.plot(labels, langeland / langeland[0], "c--", label="Langeland index")
ax1.plot(labels, lolland / lolland[0], "y--", label="Lolland index")
ax1.legend(frameon=False)

for i, tick in enumerate(ax1.get_xticklabels()):
    tick.set_rotation(90)
    if i % 4 != 0:
        tick.set_fontsize(0)
        tick.set_color("white")

ax1.set_xlim(-1, len(labels) + 1)
ax1.set_ylim(0.8, 9)
ax1.set_ylabel("Index value")
plt.tight_layout()
plt.savefig("geografiske_forskelle_en.svg")


relativ_huspris = []
for rente in np.linspace(0, 10, 1000):
    relativ_huspris.append(
        (formler.afbetalling(klån=1, n=30, r=rente / 100 + 10**-6) * 30 * 0.8 + 0.2)
        ** (-1)
    )

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(np.linspace(0, 10, 1000), relativ_huspris, linewidth=4)
ax1.set_ylabel("Relative house price")
ax1.set_xlabel("Interest rate %")
ax1.grid(which="minor")
ax1.grid(which="major")
plt.tight_layout()
plt.savefig("huspris_rente_funktion_en.svg")
