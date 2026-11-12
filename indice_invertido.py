import re
import unicodedata


def separar_palavras(linha):
    """Separa as palavras e mantém os acentos."""
    linha = unicodedata.normalize("NFC", linha.lower())
    # \w inclui letras, números e _, mas queremos separar pelo _ também.
    return re.findall(r"[^\W_]+", linha)


def construir_indice(texto):
    indice = {}

    for numero, linha in enumerate(texto.splitlines(), start=1):
        for palavra in separar_palavras(linha):
            if palavra not in indice:
                indice[palavra] = set()
            indice[palavra].add(numero)

    return indice


def _linhas_da_palavra(indice, palavra):
    termos = separar_palavras(palavra)
    if len(termos) != 1:
        return set()
    return indice.get(termos[0], set())


def buscar(indice, palavra):
    return sorted(_linhas_da_palavra(indice, palavra))


def buscar_e(indice, palavras):
    resultado = None

    for palavra in palavras:
        linhas = _linhas_da_palavra(indice, palavra)
        if resultado is None:
            resultado = linhas
        else:
            resultado = resultado & linhas

        if not resultado:
            return []

    return sorted(resultado) if resultado is not None else []


def buscar_ou(indice, palavras):
    resultado = set()
    for palavra in palavras:
        resultado.update(_linhas_da_palavra(indice, palavra))
    return sorted(resultado)
