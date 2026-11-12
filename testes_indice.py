from indice_invertido import buscar, buscar_e, buscar_ou, construir_indice


# Casos do enunciado
texto = "Python e dados\nDados e algoritmos\nPython e algoritmos"
indice = construir_indice(texto)

assert indice["python"] == {1, 3}
assert indice["dados"] == {1, 2}
assert indice["algoritmos"] == {2, 3}
assert buscar(indice, "python") == [1, 3]
assert buscar(indice, "java") == []
assert buscar_e(indice, ["python", "dados"]) == [1]
assert buscar_ou(indice, ["python", "dados"]) == [1, 2, 3]

# Pontuação, maiúsculas, acentos, repetição e linha vazia
texto = (
    "Python,Python e café!\n"
    "\n"
    "Dados, PYTHON e cafe.\n"
    "Dados, algoritmos e café.\n"
    "CAFÉ."
)
indice = construir_indice(texto)
esperado = {
    "python": {1, 3},
    "e": {1, 3, 4},
    "café": {1, 4, 5},
    "dados": {3, 4},
    "cafe": {3},
    "algoritmos": {4},
}

assert indice == esperado
assert buscar(indice, "CAFÉ") == [1, 4, 5]
assert buscar(indice, "cafe") == [3]
assert buscar_e(indice, ["DADOS", "e", "café"]) == [4]
assert buscar_e(indice, ["python", "dados", "java"]) == []
assert buscar_ou(indice, ["python", "dados", "café"]) == [1, 3, 4, 5]
assert buscar_ou(indice, ["cafe", "java", "cafe"]) == [3]
assert indice == esperado  # As consultas devem preservar o índice.

assert construir_indice("") == {}
assert construir_indice("\n   \n") == {}
assert buscar({}, "python") == []

print("Todos os testes passaram.")
