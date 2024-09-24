import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'File modified: {event.src_path}')
    
    def on_created(self, event):
        print(f'File created: {event.src_path}')
    
    def on_deleted(self, event):
        print(f'File deleted: {event.src_path}')
    
    def on_moved(self, event):
        print(f'File moved: {event.src_path} to {event.dest_path}')

if __name__ == "__main__":
    path = "D:/Day 1"  # Specify the directory to monitor
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
