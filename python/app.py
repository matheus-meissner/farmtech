from dados import culturas, inserir_dados, listar_dados, atualizar_dados, deletar_dados
from utils import salvar_csv

def menu():
    while True:
        print("\n--- FARMTECH SOLUTIONS ---")
        print("1 - Inserir dados")
        print("2 - Listar dados")
        print("3 - Atualizar dados")
        print("4 - Deletar dados")
        print("5 - Salvar e sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            inserir_dados()
        elif opcao == "2":
            listar_dados()
        elif opcao == "3":
            atualizar_dados()
        elif opcao == "4":
            deletar_dados()
        elif opcao == "5":
            salvar_csv(culturas)
            print("Dados salvos em 'dados.csv'. Encerrando...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
