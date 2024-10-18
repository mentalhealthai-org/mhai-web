import time
from threading import Timer

import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Lock



class Watcher:
    def __init__(self, directory_to_watch: str, command: str):
        self.directory_to_watch = directory_to_watch
        self.command = command
        self.observer = Observer()
        self.is_command_running = False  # Flag to track if a command is running
        self.lock = Lock()  # Lock to synchronize access

    def run(self):
        event_handler = Handler(self.command, self)
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, command: str, watcher: Watcher):
        self.command = command
        self.watcher = watcher
        self.debounce_timer = None  # Timer to debounce events
        self.debounce_delay = 1  # 1 second delay

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type in ('modified', 'created', 'deleted'):
            print(f'Event type: {event.event_type}  Path: {event.src_path}')
            # Cancel the previous debounce timer if it exists
            if self.debounce_timer:
                self.debounce_timer.cancel()

            # Start a new debounce timer
            self.debounce_timer = Timer(self.debounce_delay, self.run_command_in_sequence)
            self.debounce_timer.start()

    def run_command_in_sequence(self):
        with self.watcher.lock:
            if not self.watcher.is_command_running:
                self.watcher.is_command_running = True
                try:
                    print(f"[II] Running command: {self.command}")
                    subprocess.run(self.command, shell=True)
                finally:
                    self.watcher.is_command_running = False
                print(f"[II] DONE")


if __name__ == '__main__':
    # Specify the directory to watch and the system command to execute
    directory_to_watch = "src/frontend/src"
    system_command = "makim reactjs.build"

    # Create and run the watcher
    watcher = Watcher(directory_to_watch, system_command)
    watcher.run()
