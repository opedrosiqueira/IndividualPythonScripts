import io
import sys


input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding="iso-8859-1")
sys.stdout.reconfigure(encoding="iso-8859-1")

for line in input_stream:
    for c in line:
        sys.stdout.write(str(ord(c)) + " ")
