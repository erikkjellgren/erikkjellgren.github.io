"To use multiprossing pool, this name main guard is needed."
"I do not understand the reason."
if __name__ == "__main__":
    import dkfinance_modeller.utility.webscrape as webscrape

    f = open("data/template_skat_positiv_liste.csv", "r")
    isiner = []
    for i, line in enumerate(f):
        if i == 0:
            continue
        isiner.append(line.strip("\n"))
    f.close()

    out = open("skat_positiv_liste_info.csv", "w")
    out.write("ISIN;Navn;Index;ÅOP;Replication;Domicil\n")
    infoer = webscrape.få_etf_info(isiner, 4)
    for info in infoer:
        if info["succes"]:
            out.write(
                f"{info['isin']};{info['navn']};{info['indeks']};"
                f"{info['åop']};{info['replication']};{info['domicile']}\n"
            )
        else:
            print(info)
    out.close()
    f = open("data/template_nordnet_liste.csv", "r")
    isiner = []
    skat = {}
    for i, line in enumerate(f):
        if i == 0:
            continue
        isiner.append(line.strip("\n").split(";")[1])
        skat[line.strip("\n").split(";")[1]] = line.strip("\n").split(";")[0]
    f.close()
    out = open("nordnet_liste_info.csv", "w")
    out.write("ISIN;Navn;Index;ÅOP;Replication;Domicil;Beskatning\n")
    infoer = webscrape.få_etf_info(isiner, 4)
    for info in infoer:
        if info["succes"]:
            out.write(
                f"{info['isin']};{info['navn']};{info['indeks']};"
                f"{info['åop']};{info['replication']};{info['domicile']};{skat[str(info['isin'])]}\n"
            )
        else:
            print(info)
    out.close()
