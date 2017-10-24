import sys
import time
import logging
import json
import dumper
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

"""
1. check last block on database
2. check if new block has created, parse block and insert to database
3. if re-table argrument we will delete database collection and create new again
4. verify hash on database
"""

class DetectBlockHandler(PatternMatchingEventHandler):
    patterns = ["*.dat"]
    def on_created(self, event):
        super(DetectBlockHandler, self).on_created(event)
        logging.info("File %s was just created" % event.src_path)

def file_watcher(path):
    logging.info("Watcher was started on path: %s" % path)
    event_handler = DetectBlockHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def load_config():
    with open('./config/app.json', 'r') as config_file:
        config = json.load(config_file)
        if config is None:
            return False
        else:
            return config
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    path = load_config()['bitcoin']['mainnet']
    if path == "":
        logging.error('Please set the path of configuration to provide block')
        sys.exit(0)

    try:
        file_watcher(path)
        # start file watcher for threading
        # fw = Thread(target = file_watcher, args = (path, ))
        # fw.start()
        # fw.join()
        # logging.info("file watcher finished..., exiting")
    except (KeyboardInterrupt, SystemExit):
        logging.info("Received keyboard interrupt, quitting threads.")
        sys.exit(0)
