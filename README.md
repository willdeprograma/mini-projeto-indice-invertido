# Índice invertido para busca textual

Mini-projeto de Estruturas de Dados do IFAL Maceió.

O programa busca palavras em um arquivo de texto e mostra os números das linhas em que elas aparecem. O índice é um dicionário que guarda um conjunto de linhas para cada palavra.

## Como rodar

Com o Python 3 instalado, abra o terminal na pasta do projeto e rode o comando abaixo.

~~~bash
python programa.py texto_exemplo.txt
~~~

- Escolha `1` e digite `python` para ver as linhas `[1, 3, 5]`.
- Escolha `2` e digite `python estruturas` para buscar as duas palavras na mesma linha. O resultado é `[3]`.
- Escolha `3` e digite `python estruturas` para buscar linhas com pelo menos uma das palavras. O resultado é `[1, 2, 3, 4, 5]`.
- Escolha `0` para sair.

Para usar outro arquivo, troque `texto_exemplo.txt` pelo caminho de um texto em UTF-8.

## Testes e medições

~~~bash
python testes_indice.py
python experimento.py
~~~

O experimento usa um texto de 2.400 linhas gerado pelo próprio programa. Os tempos estão no [relatório](relatorio.md).
