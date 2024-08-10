import sys

input = sys.stdin.readline
print = sys.stdout.write

ignore = set()
line = input()
while line != "::\n":
    ignore.add(line.rstrip().lower())
    line = input()

list = []
count = 0
for line in sys.stdin:
    start = 0
    line = line.lower()
    for end in range(len(line)):
        if not line[end].isalpha():
            if line[start].isalpha() and line[start:end] not in ignore:
                list.append((line[start:end], count, line[0:start] + line[start:end].upper() + line[end:]))
                count += 1
            start = end + 1

list.sort()

for end in range(len(list)):
    print(list[end][2])
