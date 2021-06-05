import time
from json import JSONDecodeError
from typing import List

import numpy as np
import requests

names = []
danish_fonds = [
    "data/danish_funds_assets/Sparindex_Dow_Jones_Sustainability_World_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Globale_Aktier_Min_Risiko_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Globale_Aktier_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Emerging_Markets_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Baeredygtige_Global_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Sparindex_Globale_Aktier_Min_Risiko_Akk_KL_downloaded_31may2021.txt",
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
    "data/danish_funds_assets/Danske_Invest_Oesteuropa_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Fjernoesten_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Fjernoesten_Indeks_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Danmark_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Danmark_Indeks_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Danmark_Indeks_ex_OMXC20_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Danmark_Fokus_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Danmark-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Nye_Markeder_Small_Cap_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Nye_Markeder-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Emerging_Markets_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europe_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_Small_Cap_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_Small_Cap-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_Indeks_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa-Akkumulerende_klasse_DKK_h_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_Indeks_BNP_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_Hoejt_Udbytte_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_Hoejt_Udbytte-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Europa_2_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Teknologi_Indeks_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Pacific_incl_Canada_ex_Japan_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Sustainable_Future_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Sustainable_Future-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Sustainable_Future_3_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Sustainable_Future_2_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Indeks_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_Indeks-Akkumulerende_klasse_DKK_h_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Global_AC_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Bioteknologi_Indeks_KL_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Japan_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Japan_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_Kina_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_USA_klasse_DKK_d_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_USA-Akkumulerende_klasse_DKK_h_downloaded_31may2021.txt",
    "data/danish_funds_assets/Danske_Invest_USA_Restricted-Akkumulerende_klasse_DKK_downloaded_31may2021.txt",
]

for fond in danish_fonds:
    f = np.genfromtxt(fond, delimiter=";", dtype=str)
    for line in f:
        names.append(line[0])

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

skip_list = [
    "(A)",
    "(GDR)",
    "(USD)",
    "(SGD)",
    "(Foreign)",
    "(ord.)",
    "(Ord.)",
    "(Ord)",
    "(KR)",
    "(ADR)",
    "(HK)",
    "(GB)",
    "(US)",
    "(HKD)",
    "(DK)",
    "(DKK)",
    "(TW)",
    "(GR)",
    "(Persero)",
    "(SG)",
    "(Cayman)",
    "(Group)",
    "(Pref.)",
    "(B9GFHQ6)",
    "(Local)",
    "(foreign)",
    "Ltd(Foreign)",
    "(A-REIT)",
    "(TH)",
    "(Pfd)",
    "(SDPL)",
    "(NLMK)",
    "(Femsa)",
    "(Q.S.C.)",
    "(pref.)",
    "(Pref)",
    "(WOQOD)",
    "(ZAR)",
    "(Isbank)",
    "(Hangzhou)",
    "(Sisecam)",
    "(Regd)",
    "(regd)",
    "(genusscheine)",
    "(CHF)",
    "(GBP)",
    "(FR)",
    "(CH)",
    "(Reg)",
    "(NL)",
    "(IE)",
    "(CA)",
    "(INDITEX)",
    "(IT)",
    "(SE)",
    "(Regd)(Vink)",
    "(EUR)",
    "(B)",
    "(Regd.)",
    "(ES)",
    "(Bearer)",
    "(REIT)",
    "(FI)",
    "(BE)",
    "(DE)",
    "(EDF)",
    "(CAD)",
    "(JP)",
    "(AT)",
    "(ADP)",
    "(NO)",
    "(J)",
    "(bearer)",
    "(Reg.)",
    "(AUD)",
    "(DAL)",
    "(george)",
    "(Japan)",
    "(AU)",
    "(ZA)",
    "A/S",
    "AS",
    "A.S.",
    "S.A",
    "AG",
    "AB",
    "Class",
    "Ltd",
    "LTD",
    "Ltd.",
    "Tbk",
    "NV",
    "PLC",
    "S/A",
    "SA",
    "S.A.",
    "SE",
    "Regd",
    "Ord",
    "Plc",
    "Inc",
    "INC",
    "Inc.",
    "SpA",
    "Oyj",
    "OYJ",
    "ASA",
    "PCL",
    "PJSC",
    "PT",
    "SAE",
    "Bhd",
    "SCA",
    "QSC",
    "Q.S.C.",
    "Q.S.C",
    "ADR",
    "LLC",
    "KgaA",
    "KK",
    "H",
    "A",
    "B",
    "Berhad",
    "C",
    "L",
    "DKK",
    "Pref.",
    "S.A.-B",
    "SA-Pref.",
    "Pref",
    "Ltd-H",
    "Lt",
    "BV",
    "SGPS",
    "Reg.",
    "ltd",
    "HK",
    "New",
    "new",
    "Serie",
    "R.E.I.T",
    "Tbk.",
    "REIT",
    "20201228",
    "20210323",
    "B1",
    "BHD",
    "Shs",
    "shares",
    "CV",
    "Pfd",
    "REGR",
    "-",
    "sh",
    "CLS",
    "S.A.Q.",
    "Ubd",
    "S.P.A",
    "PC",
    "Se",
    "S",
    "20201228",
    "Akt.",
    "NEW",
    "shares",
]

name2yahooticker_file = open("data/name2yahooticker.txt", "a")
notfound_file = open("data/notfound_name2yahooticker.txt", "w+")

notfound_list: List[str] = []
for i, name in enumerate(names):
    if name in name2yahooticker.keys():
        continue
    if name in notfound_list:
        continue
    original_name = name
    name_copy = name
    name_copy = name_copy.replace("/The", "")
    name_copy = name_copy.replace("/Delaware", "")
    name_copy = name_copy.replace("/Japan", "")
    name_copy = name_copy.replace("/MD", "")
    name_copy = name_copy.replace("/Tokyo", "")
    name_copy = name_copy.replace("/Canada", "")
    name_copy = name_copy.replace("/Jersey", "")
    name_copy = name_copy.replace("/OH", "")
    name_copy = name_copy.replace("/GA", "")
    name_copy = name_copy.replace("/DE", "")
    name_copy = name_copy.replace("/CA", "")
    name_copy = name_copy.replace("/NV", "")
    name_copy = name_copy.replace("/Bermuda", "")
    name_copy = name_copy.replace("/Brazil", "")
    name_copy = name_copy.replace("/NY", "")
    name_copy = name_copy.replace("/New York NY", "")
    name_copy = name_copy.replace("/IN", "")
    name_copy = name_copy.replace("/Milano", "")
    name_copy = name_copy.replace("/France", "")
    name_copy = name_copy.replace("/MO", "")
    name_copy = name_copy.replace("/US", "")
    name_copy = name_copy.replace("/Los Angeles CA", "")
    name_copy = name_copy.replace("/United States", "")
    name_copy = name_copy.replace("/Ehime", "")
    name_copy = name_copy.replace("/Aichi Japan", "")
    name_copy = name_copy.replace("(stk 10 USD)", "")
    name_copy = name_copy.replace("(Cayman Islands)", "")
    name_copy = name_copy.replace("(stk A 10 USD)", "")
    name_copy = name_copy.replace("(UK Reg)", "")
    name_copy = name_copy.replace("(Ord 2.5p)", "")
    name_copy = name_copy.replace("(class A)", "")
    name_copy = name_copy.replace("(Svenska Cellulosa)", "")
    name_copy = name_copy.replace("(di Risp)", "")
    name_copy = name_copy.replace("(Class 1 Non-Voting)", "")
    name_copy = name_copy.replace("SAB de CV", "")
    name_copy = name_copy.replace("S.A. de C.V.", "")
    name_copy = name_copy.replace("SAB de C.V.", "")
    name_copy = name_copy.replace("-ADR", "")
    name_copy = name_copy.replace("-H", "")
    name_copy = name_copy.replace(".,", "")
    name_copy = name_copy.replace("-A", "")
    name_copy = name_copy.replace("-Pref.", "")
    name_copy = name_copy.replace("H- Unitary 144A/Reg S", "")
    name_copy = name_copy.replace("Del-B SH", "")
    name_copy = name_copy.replace("Units Cons of 1 Sh + 2 Pfd", "")
    name_copy = name_copy.replace("Unitary Reg S/144A", "")
    name_copy = name_copy.replace("Units Cons of 1 Sh + 4 Pfd Shs", "")
    name_copy = name_copy.split()
    new_name = ""
    for part in name_copy:
        if part in skip_list:
            continue
        new_name += f"{part} "
    r = requests.get(
        "https://query2.finance.yahoo.com/v1/finance/search",
        params={"q": new_name, "quotesCount": 1, "newsCount": 0},
    )
    time.sleep(1.0)
    counter = 0
    while True:
        try:
            data = r.json()
            ticker = data["quotes"][0]["symbol"]
            if "=" in ticker:
                raise IndexError
            name2yahooticker_file.write(f"{original_name}:{ticker}\n")
            name2yahooticker[original_name] = ticker
            name2yahooticker_file.flush()
            break
        except IndexError:
            notfound_file.write(f"{original_name}\n")
            notfound_list.append(original_name)
            notfound_file.flush()
            break
        except KeyError:
            print(f"KeyError: {original_name}")
            continue
        except JSONDecodeError:
            print("Waiting 300 sec")
            time.sleep(300)
            continue
notfound_file.close()
name2yahooticker_file.close()
