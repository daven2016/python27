# -*- coding: utf-8 -*-
import os
import re
import urlparse
import shutil
import zlib
from datetime import datetime, timedelta
from downloader import ScrapeCallback

try:
    import cPickle as pickle
except ImportError:
    import pickle
from link_crawler import link_crawler

class DiskCache:
    def __init__(self, cache_dir='cache', expires=timedelta(30), compress=True):
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    # 将URL映射成安全文件名
    def url_to_path(self, url):
        """Create file system path for this URL"""
        components = urlparse.urlsplit(url)
        #append index.html to empty paths
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        #replace invalid characters
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        #restrict maximum number of characters
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)

    # 从缓存中拿数据
    def __getitem__(self, url):
        """Load data from disk for this URL"""
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                return pickle.loads(data)
        else:
            # rURL has not yes been cached
            raise KeyError(url + ' does not exist!')

    # 将下载的网页缓存起来
    def __setitem__(self, url, result):
        """Load data from disk for this URL"""
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        data = pickle.dumps(result)
        with open(path, 'wb') as fp:
            if self.compress:
                data = zlib.compress(data)
            fp.write(data)

if __name__ == '__main__':
    link_crawler(seed_url='http://example.webscraping.com/', link_regex='/(index|view)', call_back=ScrapeCallback(),
                 cache=DiskCache())