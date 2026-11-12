# Relatório do mini-projeto

## Como os tempos foram medidos

O programa gerou um texto de 2.400 linhas a partir de oito frases sobre programação. As duas estratégias receberam as mesmas 1.000 consultas, na mesma ordem, com buscas simples, E e OU. A preparação do texto e a impressão ficaram fora da medição. Os tempos foram registrados com `time.perf_counter()`, usando Python 3.12.14 em Linux.

## Experimento 1 — Tempo de busca

| Medição | Tempo (ms) |
| --- | ---: |
| Construção do índice | 6,984 |
| 1.000 buscas por varredura | 5.249,983 |
| 1.000 buscas com o índice já construído | 10,352 |

## Experimento 2 — Vantagem da indexação

Cada valor é a mediana de três execuções. Em cada rodada, a última coluna inclui a construção do índice e o tempo das consultas.

| Consultas | Varredura completa (ms) | Construção do índice + consultas (ms) |
| ---: | ---: | ---: |
| 1 | 5,072 | 7,118 |
| 2 | 10,511 | 6,580 |
| 10 | 50,960 | 6,690 |
| 100 | 513,783 | 7,270 |
| 1.000 | 5.146,886 | 15,691 |

## Análise

1. Com o índice pronto, as 1.000 buscas levaram cerca de 10 ms. A varredura levou 5,25 s porque percorreu o texto todo a cada busca. Para uma consulta só, contando o tempo de montar o índice, a varredura foi mais rápida.
2. No texto testado, o índice compensou a partir de duas consultas. A varredura levou 10,511 ms e o índice, com a construção incluída, levou 6,580 ms.
3. O conjunto guarda cada número de linha uma vez. Se a mesma palavra aparece várias vezes na linha 4, o índice guarda o 4 uma única vez. Os conjuntos também permitem juntar resultados com união e interseção.
4. Encontrar uma chave no dicionário custa `O(1)` em média. Se a busca devolve `r` linhas, ordenar o resultado pode custar até `O(r log r)`.
5. Construir o índice leva `O(C)` em média, onde `C` é o número de caracteres do texto. Para conjuntos de tamanhos `a` e `b`, a união custa `O(a + b)` e a interseção custa `O(min(a, b))` em média. Com mais de duas palavras, essas operações são repetidas com os resultados intermediários.
6. O índice ocupa mais memória porque guarda as palavras distintas e os números das linhas em que elas aparecem.
