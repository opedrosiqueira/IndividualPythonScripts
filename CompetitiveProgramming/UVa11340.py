# não consegui resolver, deu time limit exceded. tentei usando tanto dicionário quanto endereçamento direto, e por incrível que pareca, endereçamento direto é pior que dicionário, por conta da chamada à função ord(). esse artigo fala sobre a entrada ser iso8859-1 e muito grande pra usar um simples input() ou print: https://www.redgreencode.com/solving-uva-11340-in-java/

import io
from sys import stdin, stdout

input_stream = io.TextIOWrapper(stdin.buffer, encoding="iso-8859-1")
read = input_stream.readline
write = stdout.write

n = int(read())

for _ in range(n):
    char_values = {}
    k = int(read())

    for _ in range(k):
        char, value = read().split()
        char_values[char] = int(value)

    m = int(read())
    total_payment = 0

    for _ in range(m):
        article_line = read()
        for char in article_line:
            if char in char_values:
                total_payment += char_values[char]

    write(f"{(total_payment / 100):.2f}$\n")

"""
import io
from sys import stdin, stdout

input_stream = io.TextIOWrapper(stdin.buffer, encoding="iso-8859-1")
read = input_stream.readline
write = stdout.write

n = int(read())

for _ in range(n):
    char_values = [0] * 511 # `[0] * size` eh mais rapido que `[0 for _ in range(size)]`

    k = int(read())

    for _ in range(k):
        char, value = read().split()
        char_values[ord(char)] = int(value)

    m = int(read())
    total_payment = 0

    for _ in range(m):
        article_line = read()
        for char in article_line:
            total_payment += char_values[ord(char)]

    write(f"{(total_payment / 100):.2f}$\n")
"""

"""
from collections import defaultdict
import io
from sys import stdin, stdout

input_stream = io.TextIOWrapper(stdin.buffer, encoding="iso-8859-1")
read = input_stream.readline
write = stdout.write

n = int(read())

for _ in range(n):
    char_values = defaultdict(int)
    k = int(read())

    for _ in range(k):
        char, value = read().split()
        char_values[char] = int(value)

    m = int(read())
    total_payment = 0

    for _ in range(m):
        article_line = read()
        for char in article_line:
            total_payment += char_values[char]

    write(f"{(total_payment / 100):.2f}$\n")
"""

"""
import io
from sys import stdin, stdout

input_stream = io.TextIOWrapper(stdin.buffer, encoding="iso-8859-1")
write = stdout.write

data = input_stream.read().split("\n")
index = -1


def read():
    global index
    index += 1
    return data[index]


n = int(read())

for _ in range(n):
    char_values = {}
    k = int(read())

    for _ in range(k):
        char, value = read().split()
        char_values[char] = int(value)

    m = int(read())
    total_payment = 0

    for _ in range(m):
        article_line = read()
        for char in article_line:
            if char in char_values:
                total_payment += char_values[char]

    write(f"{(total_payment / 100):.2f}$\n")
"""