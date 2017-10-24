import sys
import time
import logging
import json
import dumper
import click
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

"""
1. check last block on database
2. check if new block was created, parse block and insert to database
3. if re-table argrument we will delete database collection and create new again
4. verify hash on database
"""

class DetectBlockHandler(PatternMatchingEventHandler):
    patterns = ["*.dat"]

    def on_any_event(self, event):
        super(DetectBlockHandler, self).on_any_event(event)
        logging.info("File %s was just added" % event.src_path)
        """check file name in database, new file update ?"""

    def on_created(self, event):
        super(DetectBlockHandler, self).on_created(event)
        logging.info("File %s was just created.....!!! " % event.src_path)

def start_watcher(coin, path):
    logging.info("Coin: %s process was started on path: %s" % (coin, path))
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

def start_middleware():
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def readconfig():
    with open('./config/app.json', 'r') as config_file:
        config = json.load(config_file)
        if config is None:
            return False
        else:
            return config

def build_config(args, server):
    if args == 'bitcoin':
        path = readconfig()[args][server]['block_path']
        if path == "":
            logging.error('Please set the path of configuration to provide block')
            sys.exit(0)
        return path


@click.command()
@click.option('-c', default='bitcoin', type=click.Choice(['bitcoin', 'litecoin']), multiple=True, help='Coin to enable, bitcoin, litecoin')
@click.option('-s', default='mainnet', type=click.Choice(['mainnet', 'testnet']), help='Network protocol of blockchain')
def cli(c, s):
    """Examle: python run.py -c bitcoin"""

    for coin in c:
        path = build_config(coin, s)
        if path is None or path == '':
            logging.error('%s not have configuration, let check your config...' % coin)
        else:
            logging.info('Working on = %s! ' % coin)
            start_watcher(coin, path)

if __name__ == '__main__':
    start_middleware()
    cli()
