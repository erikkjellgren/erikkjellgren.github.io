import dkfinance_modeller.utility.formler as formler
import matplotlib.pyplot as plt
import numpy as np

huspris = np.genfromtxt("data/huspriser_danmark.txt")
huspris_indeks = huspris / huspris[0]

labels = np.genfromtxt("data/labels.txt", dtype=str, delimiter=",")

diskonto = np.genfromtxt("data/diskonto.txt", delimiter=",")
diskonto_min = np.zeros(len(diskonto))
mindste = 10
for i, rente in enumerate(diskonto):
    mindste = min(mindste, rente)
    diskonto_min[i] = mindste

lønstigning = np.genfromtxt("data/loenstigning.txt")
lønstigning = (1 + lønstigning / 100) ** (3 / 12) - 1
løn_indeks = [1]
for stigning in lønstigning[1:]:
    løn_indeks.append(løn_indeks[-1] * (1 + stigning))

husomkostninger = []
husomkostninger_min = []
for rente, rente_min, pris in zip(diskonto, diskonto_min, huspris):
    husomkostninger.append(
        formler.afbetalling(klån=pris * 0.8, n=30, r=rente / 100 + 10 ** -6) * 30
        + 0.2 * pris
    )
    husomkostninger_min.append(
        formler.afbetalling(klån=pris * 0.8, n=30, r=rente_min / 100 + 10 ** -6) * 30
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
ax1.plot(
    labels,
    husomkostninger_min_indeks,
    "r--",
    label="Huskøbsomkostninger indeks (minimum diskonto)",
)
ax1.plot(labels, husomkostninger_indeks, "k-", label="Huskøbsomkostninger indeks")
ax1.plot(labels, huspris_indeks, "m-", label="Huspris indeks")
ax1.plot(labels, løn_indeks, "g-", label="Løn indeks")
ax1.legend(frameon=False)

ax2.plot(labels, diskonto_min, "r--", label="Diskonto minimum")
ax2.plot(labels, diskonto, "k--", label="Diskonto")
ax2.set_ylim(-0.2, 5.5)
ax2.set_ylabel("Diskonto")
ax2.legend(frameon=False)

for i, tick in enumerate(ax1.get_xticklabels()):
    tick.set_rotation(90)
    if i % 4 != 0:
        tick.set_fontsize(0)
        tick.set_color("white")

ax1.set_xlim(-1, len(labels) + 1)
ax1.set_ylim(0.9, 4.0)
ax1.set_ylabel("Indeks værdi")
plt.tight_layout()
plt.savefig("huspris_indekser.svg")

huspris = np.genfromtxt("data/huspriser_danmark.txt")
københavn = np.genfromtxt("data/huspriser_koebenhavn.txt")
odense = np.genfromtxt("data/huspriser_odense.txt")
aarhus = np.genfromtxt("data/huspriser_aarhus.txt")
aalborg = np.genfromtxt("data/huspriser_aalborg.txt")
langeland = np.genfromtxt("data/huspriser_langeland.txt")
lolland = np.genfromtxt("data/huspriser_lolland.txt")
fig, ax1 = plt.subplots(1, 1, figsize=(6, 4), sharex=True)
ax1.plot(labels, huspris_indeks, "m-", label="Danmark indeks")
ax1.plot(labels, københavn / københavn[0], "k--", label="København indeks")
ax1.plot(labels, odense / odense[0], "b--", label="Odense indeks")
ax1.plot(labels, aarhus / aarhus[0], "g--", label="Aarhus indeks")
ax1.plot(labels, aalborg / aalborg[0], "r--", label="Aalborg indeks")
ax1.plot(labels, langeland / langeland[0], "c--", label="Langeland indeks")
ax1.plot(labels, lolland / lolland[0], "y--", label="Lolland indeks")
ax1.legend(frameon=False)

for i, tick in enumerate(ax1.get_xticklabels()):
    tick.set_rotation(90)
    if i % 4 != 0:
        tick.set_fontsize(0)
        tick.set_color("white")

ax1.set_xlim(-1, len(labels) + 1)
ax1.set_ylim(0.8, 8)
ax1.set_ylabel("Indeks værdi")
plt.tight_layout()
plt.savefig("geografiske_forskelle.svg")


relativ_huspris = []
for rente in np.linspace(0, 10, 1000):
    relativ_huspris.append(
        (formler.afbetalling(klån=1, n=30, r=rente / 100 + 10 ** -6) * 30 * 0.8 + 0.2)
        ** (-1)
    )

fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(np.linspace(0, 10, 1000), relativ_huspris, linewidth=4)
ax1.set_ylabel("Relativ Huspris")
ax1.set_xlabel("Rente %")
ax1.grid(which="minor")
ax1.grid(which="major")
plt.tight_layout()
plt.savefig("huspris_rente_funktion.svg")
