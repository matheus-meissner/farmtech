# utils.py
import csv

def salvar_csv(lista, arquivo="dados.csv"):
    if not lista:
        print("Nenhum dado para salvar.")
        return

    # União de todas as chaves (para não estourar no DictWriter)
    all_keys = set()
    for row in lista:
        all_keys.update(row.keys())

    # Opcional: ordenar e priorizar algumas colunas
    ordem_preferida = ["cultura", "area", "ruas", "sulco_total", "plantas", "N", "P", "K"]
    restantes = [k for k in sorted(all_keys) if k not in ordem_preferida]
    fieldnames = [k for k in ordem_preferida if k in all_keys] + restantes

    with open(arquivo, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in lista:
            writer.writerow({k: row.get(k, "") for k in fieldnames})
