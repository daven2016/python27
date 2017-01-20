# -*- coding: utf-8 -*-
import urllib2
import random
import urlparse
import datetime
import time

# 下载类：能够实现网页的下载和缓存
class Downloader:
    def __init__(self, delay=5, user_agent='wswp', proxies=None, num_retries=1, cache=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url is not available in cache
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # server error so ignore result from cache
                    result = None
        if result is None:
            # result was not loaded from cache, so still need to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-Agent': self.user_agent}
            result = self.download(url, headers, proxy, self.num_retries)
            if self.cache:
                self.cache[url] = result
            return result['html']

    # 下载网页，返回一个字典 {'html': html, 'code': code}
    def download(self, url, headers, proxy, num_retries, data=None):
        print 'Downloading {}'.format(url)
        # 一定要加'headers='
        req = urllib2.Request(url, headers=headers)
        opener = urllib2.build_opener()
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            response = opener.open(req, data)
            html = response.read()
            code = response.code
            return {'html': html, 'code': code}
        except urllib2.URLError as e:
            print 'Download Error：'.format(e.reason)

            if num_retries > 0:
                # 当发生5**错误时，可以进行重试下载网页
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.download(url, headers, proxy, num_retries-1, data=None)


# 下载限速
class Throttle:
    # Add a delay between downloads to the same domain
    def __init__(self, delay=5):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                time.sleep(sleep_secs)

        # update the last accessed time
        self.domains[domain] = datetime.datetime.now()


import csv
import lxml.html
import re

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))
        self.fields = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld',
                       'currency_code', 'currency_name', 'phone', 'postal_code_format',
                       'postal_code_regex', 'languages', 'neighbours')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
            self.writer.writerow(row)