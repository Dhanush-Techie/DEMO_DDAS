import hashlib
import os
import requests
import concurrent.futures

def compute_file_hash(file_path, chunk_size=8192):
    """
    Computes SHA-256 hash for a local file.
    
    :param file_path: Path to the local file.
    :param chunk_size: Size of each read chunk.
    :return: SHA-256 hash of the file.
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Error hashing file {file_path}: {e}")
        return None

def compute_online_file_hash(url, chunk_size=8192):
    """
    Computes SHA-256 hash for a file accessed via a URL.
    
    :param url: URL of the file.
    :param chunk_size: Size of each read chunk.
    :return: SHA-256 hash of the file.
    """
    sha256 = hashlib.sha256()
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=chunk_size):
                sha256.update(chunk)
            return sha256.hexdigest()
        else:
            print(f"Failed to get file from {url}, status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error processing file from {url}: {e}")
        return None

def compute_hash(file_path_or_url):
    """
    Determines if the input is a local file path or an online URL and computes its hash accordingly.
    
    :param file_path_or_url: Local file path or online URL.
    :return: SHA-256 hash of the file or None if error occurs.
    """
    if file_path_or_url.startswith('http://') or file_path_or_url.startswith('https://'):
        return compute_online_file_hash(file_path_or_url)
    else:
        return compute_file_hash(file_path_or_url)

def compute_hashes_concurrently(file_paths_or_urls):
    """
    Computes hashes for multiple files concurrently.
    
    :param file_paths_or_urls: List of local file paths or online URLs.
    :return: List of hashes corresponding to each file path or URL.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(compute_hash, path) for path in file_paths_or_urls]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    return results

# Example usage
file_paths_or_urls = [
    'C:/Users/pravi/Documents/Pravin_Resume.pdf',                     
    'C:/Users/pravi/Pictures/Screenshots/check.pdf', 
    'http://h10032.www1.hp.com/ctg/Manual/c03730648.pdf',                     
    'https://bit.ly/3z8jDAt'  
]

hashes = compute_hashes_concurrently(file_paths_or_urls)
for file_path_or_url, file_hash in zip(file_paths_or_urls, hashes):
    if file_hash:
        print(f"Hash for {file_path_or_url}: {file_hash}")
    else:
        print(f"Error processing {file_path_or_url}")
