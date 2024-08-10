import sys

input = sys.stdin.readline
print = sys.stdout.write

ignore = set()
line = input()
while line != "::\n":
    ignore.add(line.rstrip().lower())
    line = input()

list = []
count = 0  # como títulos com mesmas palavras-chaves são ordenados por quem veio primeiro, eu mantenho a ordem das inserções nessa variável
for line in sys.stdin:
    start = 0
    line = line.lower()
    for end in range(len(line)):
        if line[end].isspace():
            if line[start].isalpha() and line[start:end] not in ignore:
                list.append((line[start:end], count, line[0:start] + line[start:end].upper() + line[end:]))
                count += 1
            start = end + 1

list.sort()  # ao ordenar tuplas, o padrão é ordenar pelo primeiro campo, quando houver empate, desempata pelo segundo campo, e assim sucessivamente. se não houvesse o campo `count`, os empates seriam desempatados pela ordem alfabética dos títulos, que não é o que o enunciado pediu.

for end in range(len(list)):
    print(list[end][2])
