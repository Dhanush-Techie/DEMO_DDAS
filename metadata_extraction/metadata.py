import os
import hashlib
from PIL import Image
from pymediainfo import MediaInfo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["USER"]
collection = db["FileData"]

# Function to compute the hash value using BLAKE2b
def compute_file_hash(file_path, chunk_size=8192):
    blake2b = hashlib.blake2b()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                blake2b.update(chunk)
        return blake2b.hexdigest()
    except Exception as e:
        print(f"Error hashing file {file_path}: {e}")
        return None

# Function to check if a hash value already exists in the database
def check_hash_in_db(hash_value):
    return collection.find_one({"HashValue": hash_value})

# Function to insert metadata into the database
def insert_file_metadata(metadata):
    collection.insert_one(metadata)

# Function to get basic metadata for any file (general file handler)
def get_file_metadata(file_path):
    file_stat = os.stat(file_path)
    Filename = os.path.basename(file_path)
    Filesize = file_stat.st_size
    Format = os.path.splitext(file_path)[1].lower()
    Directory = os.path.abspath(file_path)  # Store complete directory path
    HashValue = compute_file_hash(file_path)

    metadata = {
        "Filename": Filename,
        "Filesize": Filesize,
        "Format": Format,
        "Directory": Directory,  # Store complete file path
        "HashValue": HashValue
    }

    return metadata, HashValue

# Function to extract basic metadata from image files
def get_basic_image_attributes(image_path):
    try:
        with Image.open(image_path) as img:
            Filename = os.path.basename(image_path)
            Filesize = os.path.getsize(image_path)
            Format = img.format
            Directory = os.path.abspath(image_path)  # Store complete directory path
            HashValue = compute_file_hash(image_path)

            metadata = {
                "Filename": Filename,
                "Filesize": Filesize,
                "Format": Format,
                "Directory": Directory,  # Store complete file path
                "HashValue": HashValue
            }
            return metadata, HashValue
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None, None

# Function to extract basic metadata from video files
def get_basic_video_attributes(video_path):
    try:
        media_info = MediaInfo.parse(video_path)
        for track in media_info.tracks:
            if track.track_type == "Video":
                Filename = os.path.basename(video_path)
                Filesize = os.path.getsize(video_path)
                Format = track.format
                Directory = os.path.abspath(video_path)  # Store complete directory path
                HashValue = compute_file_hash(video_path)

                metadata = {
                    "Filename": Filename,
                    "Filesize": Filesize,
                    "Format": Format,
                    "Directory": Directory,  # Store complete file path
                    "HashValue": HashValue
                }
                return metadata, HashValue
        return None, None
    except Exception as e:
        print(f"Error processing {video_path}: {e}")
        return None, None

# Function to extract basic metadata from audio files
def get_basic_audio_attributes(audio_path):
    try:
        media_info = MediaInfo.parse(audio_path)
        for track in media_info.tracks:
            if track.track_type == "Audio":
                Filename = os.path.basename(audio_path)
                Filesize = os.path.getsize(audio_path)
                Format = track.format
                Directory = os.path.abspath(audio_path)  # Store complete directory path
                HashValue = compute_file_hash(audio_path)

                metadata = {
                    "Filename": Filename,
                    "Filesize": Filesize,
                    "Format": Format,
                    "Directory": Directory,  # Store complete file path
                    "HashValue": HashValue
                }
                return metadata, HashValue
        return None, None
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        return None, None

# Function to ask user permission for uploading duplicate files
def ask_user_permission(file_path, found_in_path):
    while True:
        user_input = input(f"Duplicate found!\nCurrent file: {file_path}\nFound in: {found_in_path}\nDo you want to upload the file again? (y/n): ").strip().lower()
        if user_input == 'y':
            return True  # User wants to upload the file again
        elif user_input == 'n':
            return False  # User does not want to upload the file again
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

# Main function to process files in a directory
def process_files_in_directory(directory):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv']
    audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']
    doc_extensions = ['.pdf', '.docx', '.ppt', '.pptx', '.csv', '.txt', '.py', '.json', '.js', '.php', '.xlsx']

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()

            # Process image files
            if file_ext in image_extensions:
                metadata, hash_value = get_basic_image_attributes(file_path)

            # Process video files
            elif file_ext in video_extensions:
                metadata, hash_value = get_basic_video_attributes(file_path)

            # Process audio files
            elif file_ext in audio_extensions:
                metadata, hash_value = get_basic_audio_attributes(file_path)

            # Process document and other general files
            else:
                metadata, hash_value = get_file_metadata(file_path)

            if metadata:
                # Check if the hash value already exists in the database
                existing_file = check_hash_in_db(hash_value)
                if existing_file:
                    # If file exists, ask for permission to upload again
                    user_permission = ask_user_permission(file_path, existing_file['Directory'])
                    if user_permission:
                        insert_file_metadata(metadata)  # Insert file metadata into database
                        print(f"File uploaded again: {file_path}")
                    else:
                        print(f"File upload skipped: {file_path}")
                else:
                    # If file doesn't exist, insert metadata into the database
                    insert_file_metadata(metadata)
                    print(f"New file added: {file_path}")

# Specify the directory to process (user input)
directory_to_process = input("Enter the directory path: ")

# Process all files in the directory
process_files_in_directory(directory_to_process)
