line = input()
try:
    while True:
        print(line)
        line = input()
except EOFError:
    pass
