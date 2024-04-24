from sys import stdin, stdout

while True:
    n, m = map(int, stdin.readline().strip().split())

    if n == m == 0:
        break

    jack = set()
    for i in range(n):
        jack.add(int(stdin.readline().strip()))

    c = 0
    for i in range(m):
        if int(stdin.readline().strip()) in jack:
            c += 1

    print(c)
