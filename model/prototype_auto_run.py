import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import subprocess

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        for filename in os.listdir(folder_to_track):
            file_path = os.path.join(folder_to_track, filename)
            subprocess.call(['python3', './max/generated_data/prediction.py', file_path])

# need to change
folder_to_track = 'max/generated_data/data'

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(20)
except KeyboardInterrupt:
    observer.stop()

observer.join()