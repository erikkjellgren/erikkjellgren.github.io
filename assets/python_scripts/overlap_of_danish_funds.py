from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import scipy.cluster.hierarchy as scipyhierarchy
import scipy.spatial.distance as scipydistance

danish_fonds = [
    "data/danish_funds_assets/Sparindex_Dow_Jones_Sustainability_World_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Globale_Aktier_Min_Risiko_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Globale_Aktier_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Emerging_Markets_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Baeredygtige_Global_KL_downloaded_31may2021.txt",
    #    "data/danish_funds_assets/Sparindex_Globale_Aktier_Min_Risiko_Akk_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_OMX_C25_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Europa_Value_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Europa_Small_Cap_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Europa_Growth_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Baeredygtige_Europa_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_USA_Small_Cap_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_USA_Value_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_USA_Growth_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Baeredygtige_USA_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Japan_Small_Cap_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Japan_Value_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Japan_Growth_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Nye_Markeder_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_oesteuropa_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Fjernoesten_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Fjernoesten_Indeks_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Danmark_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Danmark_Indeks_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Danmark_Indeks_ex_OMXC20_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Danmark_Fokus_klasse_DKK_d_downloaded_31may2021.txt",
    #    "data/danish_funds_assets/Danske_Invest_Danmark-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Nye_Markeder_Small_Cap_klasse_DKK_d_downloaded_31may2021.txt",
    #    "Danske_Invest_Nye_Markeder-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Emerging_Markets_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europe_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_Small_Cap_klasse_DKK_d_downloaded_31may2021.txt",
    #    "data/danish_funds_assets/Danske_Invest_Europa_Small_Cap-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_Indeks_klasse_DKK_d_downloaded_31may2021.txt",
    #    "data/danish_funds_assets/Danske_Invest_Europa-Akkumulerende_klasse_DKK_h_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_Indeks_BNP_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_Hoejt_Udbytte_klasse_DKK_d_downloaded_31may2021.txt",
    #    "data/danish_funds_assets/Danske_Invest_Europa_Hoejt_Udbytte-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_2_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Teknologi_Indeks_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Pacific_incl_Canada_ex_Japan_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Sustainable_Future_klasse_DKK_d_downloaded_31may2021.txt",
    #    "data/danish_funds_assets/Danske_Invest_Global_Sustainable_Future-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Sustainable_Future_3_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Sustainable_Future_2_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Indeks_klasse_DKK_d_downloaded_31may2021.txt",
    #    "data/danish_funds_assets/Danske_Invest_Global_Indeks-Akkumulerende_klasse_DKK_h_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_AC_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Bioteknologi_Indeks_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Japan_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Japan_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Kina_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_USA_klasse_DKK_d_downloaded_31may2021.txt",
    #    "data/danish_funds_assets/Danske_Invest_USA-Akkumulerende_klasse_DKK_h_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_USA_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
]

name2yahooticker = {}
f = open("data/manual_added_name2yahooticker.txt", "r")
for line in f:
    name, ticker = line.strip("\n").split(":")
    name2yahooticker[name] = ticker
f.close()
f = open("data/name2yahooticker.txt", "r")
for line in f:
    name, ticker = line.strip("\n").split(":")
    name2yahooticker[name] = ticker
f.close()

all_fonds: Dict[str, Dict[str, float]] = {}
for fond in danish_fonds:
    all_fonds[fond] = {}
    f = np.genfromtxt(fond, delimiter=";", dtype=str)
    for line in f:
        if line[0] not in name2yahooticker.keys():
            continue
        if name2yahooticker[line[0]] not in all_fonds[fond]:
            all_fonds[fond][name2yahooticker[line[0]]] = max(float(line[1]), 0)
        else:
            all_fonds[fond][name2yahooticker[line[0]]] += max(float(line[1]), 0)

S = np.zeros((len(all_fonds.keys()), len(all_fonds.keys())))
for i, fond1 in enumerate(danish_fonds):
    for j, fond2 in enumerate(danish_fonds):
        overlap = 0.0
        for key in all_fonds[fond1].keys():
            if key in all_fonds[fond2].keys():
                overlap += (all_fonds[fond1][key] * all_fonds[fond2][key]) ** 0.5
        S[i, j] = overlap

flat_dist_mat = scipydistance.squareform(scipydistance.squareform(scipydistance.pdist(S)))
res_linkage = scipyhierarchy.linkage(flat_dist_mat, method="average")
res_order = scipyhierarchy.leaves_list(res_linkage)

ordered_list = []
for i in res_order:
    ordered_list.append(danish_fonds[i])

S = np.zeros((len(all_fonds.keys()), len(all_fonds.keys())))
for i, fond1 in enumerate(ordered_list):
    for j, fond2 in enumerate(ordered_list):
        overlap = 0.0
        for key in all_fonds[fond1].keys():
            if key in all_fonds[fond2].keys():
                overlap += (all_fonds[fond1][key] * all_fonds[fond2][key]) ** 0.5
        S[i, j] = overlap

SIZE = 15
plt.rc("font", size=SIZE)
plt.rc("axes", titlesize=SIZE)
plt.rc("axes", labelsize=SIZE)
plt.rc("xtick", labelsize=SIZE)
plt.rc("ytick", labelsize=SIZE)
plt.rc("legend", fontsize=SIZE)
plt.rc("figure", titlesize=SIZE)

fig, ax1 = plt.subplots(1, 1, figsize=(24, 20))
cax = ax1.pcolormesh(S, edgecolors="k", linewidths=1, vmin=0, vmax=1.0, cmap="turbo")
fig.colorbar(cax)
labels = list(ordered_list)
for i, item in enumerate(labels):
    item = item.replace("_downloaded_31may2021.txt", "")
    item = item.replace("data/danish_funds_assets/", "")
    item = item.replace("_", " ")
    item = item.replace("Restricted-Akkumulerende", "Restric.-Akk.")
    item = item.replace("Danske Invest", "Danske Inv.")
    item = item.replace(" KL", "")
    item = item.replace(" DKK d", "")
    item = item.replace(" DKK", "")
    item = item.replace(" klasse", "")
    item = item.replace(" h", "")
    labels[i] = item
axis_ticks = labels
axis_ticks.append(" ")
ax1.set_xticks(ticks=np.linspace(0.5, len(all_fonds.keys()) + 0.5, len(all_fonds.keys()) + 1))
ax1.set_xticklabels(axis_ticks, rotation=90)
ax1.set_yticks(ticks=np.linspace(0.5, len(all_fonds.keys()) + 0.5, len(all_fonds.keys()) + 1))
ax1.set_yticklabels(axis_ticks)
ax1.set_xlim(0, len(all_fonds.keys()))
ax1.set_ylim(0, len(all_fonds.keys()))
plt.tight_layout()
plt.savefig("overlap_of_danish_funds.svg")
