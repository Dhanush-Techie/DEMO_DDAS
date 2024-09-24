import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib
from pathlib import Path
import psutil

# Function to calculate file hash
def calculate_file_hash(file_path, algorithm='sha256'):
    hash_algo = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

# Custom event handler class
class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return  # Ignore directory creation
        if event.src_path.lower().endswith(('.apk', '.exe' , '.TMP')):
            return  # Ignore .apk and .exe files
        print(f"File created: {event.src_path}")
        try:
            file_hash = calculate_file_hash(event.src_path)
            print(f"Hash of created file: {file_hash}")
        except Exception as e:
            print(f"Error hashing file: {e}")

    def on_modified(self, event):
        if event.is_directory:
            return  # Ignore directory modifications
        if event.src_path.lower().endswith(('.apk', '.exe')):
            return  # Ignore .apk and .exe files
        print(f"File modified: {event.src_path}")
        try:
            file_hash = calculate_file_hash(event.src_path)
            print(f"Hash of modified file: {file_hash}")
        except Exception as e:
            print(f"Error hashing file: {e}")

    def on_deleted(self, event):
        if event.is_directory:
            return  # Ignore directory deletion
        if event.src_path.lower().endswith(('.apk', '.exe')):
            return  # Ignore .apk and .exe files
        print(f"File deleted: {event.src_path}")

# Function to get available drives excluding CD-ROM or read-only drives
def get_available_drives():
    drives = []
    for part in psutil.disk_partitions(all=False):
        if part.fstype != '' and 'cdrom' not in part.opts.lower():  # Skip CD-ROM or non-formatted drives
            drives.append(part.device)
    return drives

# Set up a function to monitor a folder
def monitor_folder(folder_path):
    event_handler = WatcherHandler()
    observer = Observer()
    try:
        observer.schedule(event_handler, folder_path, recursive=True)
        observer.start()
        return observer
    except Exception as e:
        print(f"Error monitoring folder {folder_path}: {e}")
        return None

if __name__ == "__main__":
    # Path to monitor C:\Downloads
    downloads_folder = r"C:\\Users\\pravi\Downloads"
    print(f"Monitoring Downloads folder: {downloads_folder}")

    # Get remaining drives (excluding C: if it's already monitored)
    drives = get_available_drives()
    print(drives)
    drives = [drive for drive in drives if drive != 'C:\\']

    observers = []
    try:
        # Start monitoring the Downloads folder
        observer = monitor_folder(downloads_folder)
        if observer:
            observers.append(observer)

        # Start monitoring other drives
        for drive in drives:
            print(f"Starting observer for drive: {drive}")
            observer = monitor_folder(drive)
            if observer:
                observers.append(observer)

        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
        for observer in observers:
            observer.join()
