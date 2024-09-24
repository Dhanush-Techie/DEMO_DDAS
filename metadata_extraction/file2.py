import hashlib
import os

def compute_file_hash(file_path, chunk_size=8192):
    blake2b = hashlib.blake2b()  # Correctly name the hash function
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                blake2b.update(chunk)  # Update hash with chunks
        return blake2b.hexdigest()
    except Exception as e:
        print(f"Error hashing file {file_path}: {e}")
        return None

# Correct file paths using double backslashes or raw strings
file_path = "C:Users\\pravi\\Pictures\\human_AI.jpeg"  # Replace with your actual file path
file_hash = compute_file_hash(file_path)

# file_path2 = "D:\Games\duplicate.docx"  # Replace with your actual file path
# file_hash2 = compute_file_hash(file_path2)

# print()
# print(file_hash, file_hash2,sep="\n")

# if file_hash == file_hash2:
#     print("EQUAL")
# else:
#     print("Not Equal")
print(file_hash)