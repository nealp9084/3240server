__author__ = 'morganpietruszka'

import logging
import os
import datetime
import sys
import time

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def dateChange(base_path, filename):
    t = os.path.getmtime(os.path.join(base_path, filename))
    return datetime.datetime.fromtimestamp(t)

def dirChange(base_path):
    for file in os.listdir(base_path):
        print file, dateChange(base_path, file)

def timeRecord(dateTime):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dateTime - epoch
    return delta.total_seconds()

def milliSecs(dateTime):
    return timeRecord(dateTime) * 1000.0