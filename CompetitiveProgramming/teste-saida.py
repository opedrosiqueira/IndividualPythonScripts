import sys


sys.stdout.reconfigure(encoding="iso-8859-1")

for i in range(256):
    sys.stdout.write(chr(i))
