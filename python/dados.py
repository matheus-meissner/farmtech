from calculos import calcular_cana, calcular_cafe

# Lista principal de registros (vetor)
culturas = []

def inserir_dados():
    print("\n1 - Cana-de-açúcar")
    print("2 - Café")
    escolha = input("Escolha a cultura: ")

    if escolha == "1":
        comprimento = float(input("Digite o comprimento (m): "))
        largura = float(input("Digite a largura (m): "))
        dados = calcular_cana(comprimento, largura)
        dados["cultura"] = "Cana-de-açúcar"
        culturas.append(dados)

    elif escolha == "2":
        raio = float(input("Digite o raio (m): "))
        dados = calcular_cafe(raio)
        dados["cultura"] = "Café"
        culturas.append(dados)

    else:
        print("Opção inválida.")

def listar_dados():
    if not culturas:
        print("Nenhum dado cadastrado.")
        return

    for i, c in enumerate(culturas):
        print(f"\nID {i} | Cultura: {c['cultura']} | Área: {c['area']:.2f} m²")
        if c["cultura"] == "Cana-de-açúcar":
            print(f"Ruas: {c['ruas']} | Sulco total: {c['sulco_total']} m")
        else:
            print(f"Plantas: {c['plantas']}")
        print(f"N: {c['N']:.2f} g | P: {c['P']:.2f} g | K: {c['K']:.2f} g")

def atualizar_dados():
    idx = int(input("Digite o ID do registro para atualizar: "))
    if 0 <= idx < len(culturas):
        print("Atualize os dados novamente.")
        del culturas[idx]
        inserir_dados()
    else:
        print("ID inválido.")

def deletar_dados():
    idx = int(input("Digite o ID do registro para deletar: "))
    if 0 <= idx < len(culturas):
        culturas.pop(idx)
        print("Registro deletado.")
    else:
        print("ID inválido.")
