import os
import mimetypes
import requests
import socket
from datetime import datetime
from urllib.parse import urlparse

def get_file_metadata(file_path_or_url):
    if file_path_or_url.startswith('http://') or file_path_or_url.startswith('https://'):
        return get_online_file_metadata(file_path_or_url)
    else:
        return get_local_file_metadata(file_path_or_url)

def get_local_file_metadata(file_path):
    try:
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        file_stats = os.stat(file_path)
        creation_time = datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        modification_time = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        access_time = datetime.fromtimestamp(file_stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')
        location = os.path.abspath(file_path)

        metadata = {
            'filename': filename,
            'file_size': file_size,
            'mime_type': mime_type,
            'creation_time': creation_time,
            'modification_time': modification_time,
            'access_time': access_time,
            'location': location
        }
        return metadata
    except Exception as e:
        print(f"Error retrieving metadata: {e}")
        return None

def get_online_file_metadata(url):
    try:
        response = requests.head(url)
        if response.status_code == 200:
            filename = url.split('/')[-1]
            file_size = response.headers.get('Content-Length')
            file_size = int(file_size) if file_size else 'Unknown'
            mime_type = response.headers.get('Content-Type')
            last_modified = response.headers.get('Last-Modified', 'Unknown')
            
            parsed_url = urlparse(url)
            domain = parsed_url.hostname
            ip_address = socket.gethostbyname(domain) if domain else 'Unknown'

            metadata = {
                'filename': filename,
                'file_size': file_size,
                'mime_type': mime_type,
                'last_modified': last_modified,
                'domain': domain,
                'ip_address': ip_address
            }
            return metadata
        else:
            print(f"Failed to get metadata, status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error retrieving metadata: {e}")
        return None

# Example usage for both local and online files
file_input = "http://h10032.www1.hp.com/ctg/Manual/c03730648.pdf"  # Replace with your local file path or online URL
metadata = get_file_metadata(file_input)

if metadata:
    print("File Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")
