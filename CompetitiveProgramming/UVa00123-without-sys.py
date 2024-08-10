import sys

ignore = set()
line = input()
while line != "::":
    ignore.add(line.lower())
    line = input()

list = []
count = 0

try:
    while True:
        line = input()
        start = 0
        line = line.lower()
        for end in range(len(line) + 1):
            if end == len(line) or not line[end].isalpha():
                if start != len(line) and line[start].isalpha() and line[start:end] not in ignore:
                    list.append((line[start:end], count, line[0:start] + line[start:end].upper() + line[end:]))
                    count += 1
                start = end + 1
except EOFError:
    pass
list.sort()

for end in range(len(list)):
    print(list[end][2])
