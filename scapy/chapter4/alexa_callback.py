from zf_open import AlexaCallback
from downloader import Downloader
from link_crawler import link_crawler
from disk_cache import DiskCache

cache = DiskCache()
down = Downloader(cache=cache)
urls = AlexaCallback(100)

# -*- coding: utf-8 -*-

import sys
from threaded_crawler import threaded_crawler

from alexa_cb import AlexaCallback


def main(max_threads):
    scrape_callback = AlexaCallback()
    cache = DiskCache()
    #cache.clear()
    threaded_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache, max_threads=max_threads, timeout=10)


if __name__ == '__main__':
    max_threads = int(sys.argv[1])
    main(max_threads)





