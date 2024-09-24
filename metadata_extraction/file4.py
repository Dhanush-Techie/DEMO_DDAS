import hashlib
import requests

def download_and_hash(url, output_path, chunk_size=8192):
    """
    Downloads a file from the given URL to a specified path and computes its SHA-256 hash in real-time.

    Args:
        url (str): The URL of the file to download.
        output_path (str): The local file path where the downloaded file will be saved.
        chunk_size (int): The size of each chunk to read during download (default is 8192 bytes).

    Returns:
        str: The SHA-256 hash of the downloaded file.
    """
    sha256_hash = hashlib.blake2b()  # Initialize the SHA-256 hash object
    response = requests.get(url, stream=True)  # Stream the download to handle large files

    if response.status_code == 200:
        with open(output_path, "wb") as file:  # Open the file in binary write mode
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:  # Filter out keep-alive chunks
                    file.write(chunk)  # Write chunk to file
                    sha256_hash.update(chunk)  # Update hash with chunk data
        return sha256_hash.hexdigest()  # Return the hex digest of the hash
    else:
        raise Exception(f"Failed to download file: {response.status_code}")

# Example usage
# IP Address: 10.10.10.10
# Port: 80
# username: admin
# password: admin

url = 'https://web.mit.edu/16.070/www/lecture/hashing.pdf'
output_path = 'D:/Games/downloaded_file.pdf'
hash_value = download_and_hash(url, output_path)

print(f"SHA-256 Hash: {hash_value}")
