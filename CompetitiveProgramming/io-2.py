import os


r = os.read(0, 2**32).decode("utf-8")
output = []
for line in r.split("\r\n"):
    output.append(line)
os.write(1, "\n".join(output).encode("utf-8"))
