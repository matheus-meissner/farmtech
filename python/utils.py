import csv

def salvar_csv(lista, arquivo="dados.csv"):
    if not lista:
        print("Nenhum dado para salvar.")
        return

    chaves = lista[0].keys()

    with open(arquivo, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=chaves)
        writer.writeheader()
        writer.writerows(lista)
