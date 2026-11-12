import argparse

from indice_invertido import buscar, buscar_e, buscar_ou, construir_indice


def main():
    parser = argparse.ArgumentParser(description="Busca palavras em um arquivo de texto.")
    parser.add_argument("arquivo", help="Caminho para um arquivo de texto em UTF-8")
    args = parser.parse_args()

    try:
        with open(args.arquivo, encoding="utf-8") as arquivo:
            indice = construir_indice(arquivo.read())
    except (OSError, UnicodeError) as erro:
        parser.exit(1, f"Erro ao ler o arquivo. {erro}\n")

    while True:
        print("\n1. Busca simples | 2. Busca E | 3. Busca OU | 0. Sair")
        try:
            opcao = input("Opção: ").strip()
            if opcao == "0":
                break
            if opcao not in ("1", "2", "3"):
                print("Escolha uma opção do menu.")
                continue

            palavras = input("Digite a(s) palavra(s): ").split()
        except EOFError:
            break

        if opcao == "1" and len(palavras) == 1:
            resultado = buscar(indice, palavras[0])
        elif opcao in ("2", "3") and len(palavras) >= 2:
            if opcao == "2":
                resultado = buscar_e(indice, palavras)
            else:
                resultado = buscar_ou(indice, palavras)
        else:
            print("Digite uma palavra na busca simples ou duas ou mais nas buscas E e OU.")
            continue

        print("Linhas encontradas:", resultado)


if __name__ == "__main__":
    main()
