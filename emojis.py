# Keyboard module in Python
import threading
import keyboard
import json
import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

config_file = sys.argv[1]
dir_of_config_file = os.path.dirname(config_file)

mappings = {}


def clear_mappings():
    global mappings
    for key in mappings:
        keyboard.remove_abbreviation(key)
    mappings = {}


def load_from_config_file():
    global mappings
    global config_file
    clear_mappings()

    with open(config_file, encoding='utf-8') as f:
        for line in f.readlines():
            [shortcut, emoji] = line.split('->')
            mappings[shortcut] = emoji.strip()

    for key in mappings:
        keyboard.add_abbreviation(key, mappings[key])


def load_from_config_file_protected():
    try:
        load_from_config_file()
    except:
        print('Unable to load shortcuts')


class FileChangedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        load_from_config_file_protected()


load_from_config_file()

event_handler = FileChangedHandler()
observer = Observer()
observer.schedule(event_handler, path=dir_of_config_file, recursive=False)
observer.start()

while True:
    time.sleep(1000000)
