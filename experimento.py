import argparse
import platform
from statistics import median
from time import perf_counter

from indice_invertido import buscar, buscar_e, buscar_ou, construir_indice, separar_palavras


FRASES = (
    "Python é uma linguagem de programação.",
    "Algoritmos organizam dados para facilitar a busca.",
    "As estruturas de dados ajudam a resolver problemas.",
    "Python tem listas, conjuntos e dicionários.",
    "A tabela hash dá acesso rápido a uma chave.",
    "A programação exige prática e atenção aos detalhes.",
    "Os conjuntos guardam elementos sem repetição.",
    "Um índice ajuda a buscar palavras no texto.",
)

CONSULTAS = (
    ("simples", ("python",)),
    ("simples", ("java",)),
    ("simples", ("programação",)),
    ("simples", ("1200",)),
    ("e", ("estruturas", "dados")),
    ("e", ("python", "dados", "algoritmos")),
    ("ou", ("hash", "python")),
    ("ou", ("índice", "programação", "java")),
)

BUSCAS = {"simples": buscar, "e": buscar_e, "ou": buscar_ou}
REPETICOES = 3


def gerar_texto(quantidade):
    linhas = []
    for numero in range(1, quantidade + 1):
        frase = FRASES[(numero - 1) % len(FRASES)]
        linhas.append(f"{numero}. {frase}")
    return "\n".join(linhas)


def buscar_varredura(texto, consulta):
    tipo, palavras = consulta
    termos = set(palavras)
    linhas = []

    for numero, linha in enumerate(texto.splitlines(), start=1):
        palavras_da_linha = set(separar_palavras(linha))
        if tipo == "ou":
            encontrou = bool(termos & palavras_da_linha)
        else:
            # Para a busca simples, termos tem um único elemento.
            encontrou = termos <= palavras_da_linha

        if encontrou:
            linhas.append(numero)

    return linhas


def buscar_com_indice(indice, consulta):
    tipo, palavras = consulta
    if tipo == "simples":
        return buscar(indice, palavras[0])
    return BUSCAS[tipo](indice, palavras)


def executar_buscas(busca, fonte, consultas):
    for consulta in consultas:
        busca(fonte, consulta)


def medir_ms(funcao, *argumentos):
    inicio = perf_counter()
    funcao(*argumentos)
    return (perf_counter() - inicio) * 1000


def construir_e_buscar(texto, consultas):
    indice = construir_indice(texto)
    executar_buscas(buscar_com_indice, indice, consultas)


def executar_experimento(texto):
    consultas = [CONSULTAS[i % len(CONSULTAS)] for i in range(1000)]
    indice = construir_indice(texto)
    for consulta in CONSULTAS:
        if buscar_com_indice(indice, consulta) != buscar_varredura(texto, consulta):
            raise ValueError(f"As estratégias discordaram na consulta {consulta!r}")

    construcao = medir_ms(construir_indice, texto)
    varredura = medir_ms(executar_buscas, buscar_varredura, texto, consultas)
    indexadas = medir_ms(executar_buscas, buscar_com_indice, indice, consultas)

    totais = []
    for quantidade in (*range(1, 11), 100, 1000):
        lote = consultas[:quantidade]
        tempos_varredura = []
        tempos_indice = []
        for _ in range(REPETICOES):
            tempos_varredura.append(medir_ms(executar_buscas, buscar_varredura, texto, lote))
            tempos_indice.append(medir_ms(construir_e_buscar, texto, lote))
        totais.append((quantidade, median(tempos_varredura), median(tempos_indice)))

    print(f"Python {platform.python_version()} | {platform.system()} | {len(texto.splitlines())} linhas")
    print("\nExperimento 1 (ms)")
    print(f"Construção do índice: {construcao:.3f}")
    print(f"1.000 buscas por varredura: {varredura:.3f}")
    print(f"1.000 buscas com índice: {indexadas:.3f}")
    print("\nExperimento 2 (mediana em ms)")
    print("Consultas | Varredura | Construção + índice")
    for quantidade, tempo_varredura, tempo_indice in totais:
        print(f"{quantidade:9} | {tempo_varredura:9.3f} | {tempo_indice:19.3f}")


def main():
    parser = argparse.ArgumentParser(description="Compara busca indexada e varredura.")
    parser.add_argument("arquivo", nargs="?", help="Arquivo UTF-8 para usar no experimento")
    args = parser.parse_args()

    if args.arquivo:
        try:
            with open(args.arquivo, encoding="utf-8") as arquivo:
                texto = arquivo.read()
        except (OSError, UnicodeError) as erro:
            parser.exit(1, f"Erro ao ler o arquivo. {erro}\n")
    else:
        texto = gerar_texto(2400)

    executar_experimento(texto)


if __name__ == "__main__":
    main()
