import os


# Initialize an empty list to store chunks of input
input_chunks = []

# Read chunks until there's no more data (i.e., os.read returns an empty bytes object)
while True:
    chunk = os.read(0, 2*60)  # Read in chunks (you can adjust this size)
    if not chunk:
        break  # End of input
    input_chunks.append(chunk)

os.write(1, b"".join(input_chunks))
