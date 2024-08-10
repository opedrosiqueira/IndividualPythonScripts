import sys

input = sys.stdin.readline
print = sys.stdout.write

d = {}
entry = input()
while entry != "\n":
    vl, ch = entry.split()
    d[ch] = vl
    entry = input()


for entry in sys.stdin:
    print(d.get(entry.strip(), "eh")+"\n")
