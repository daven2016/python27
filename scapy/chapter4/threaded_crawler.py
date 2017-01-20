import time
import threading
from downloader import Downloader

SLEEP_TIME = 5

def threaded_crawler(seed_url, max_threads=10):
    # the queue of URL's that still need to be crawled
    crawl_queue = [seed_url]
    #the URL's that have been seen
    seen = set([seed_url])
