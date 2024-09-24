import ssdeep

# Reading files and computing SSDEEP hashes
with open('dummy1.txt', 'rb') as file1:
    file1_data = file1.read()

with open('dummy2.txt', 'rb') as file2:
    file2_data = file2.read()

hash1 = ssdeep.hash(file1_data)
hash2 = ssdeep.hash(file2_data)

# Comparing the hashes
similarity_score = ssdeep.compare(hash1, hash2)

print(f"SSDEEP hash of file1: {hash1}")
print(f"SSDEEP hash of file2: {hash2}")
print(f"Similarity score: {similarity_score}")
