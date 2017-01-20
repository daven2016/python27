# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 11:12:42 2017

@author: Administrator
"""

import re
import urllib2
import itertools
import urlparse
import datetime
import time
import Queue
import robotparser

#下载网页
def download(url, headers, proxy=None, num_retries=2):
    print 'Downloading:', url
    
    req = urllib2.Request(url, headers=headers)
    
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        response = opener.open(req)
        html = response.read()
        #code = response.code
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            #当发生5**错误时，可以进行重试下载网页
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, headers, proxy, num_retries-1)
    return html
    
def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc

#一、网站地图爬虫
def crawl_sitemap(url):
    #download the sitemap file
    sitemap = download(url)
    
    #extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    
    #download each link
    for link in links:
        html = download(link)
        # scrape html here
        #...

#二、ID遍历爬虫
def crawl_id(url):
    # maxinum number of consecutive download errors allowed
    max_errors = 5
    # current number of consecutive download errors
    num_errors = 0
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/-%d' % page
        html = download(url)
        if html is None:
            #received an error trying to download this webpage
            num_errors += 1
            if num_errors == max_errors:
                #reach maximum number of consecutive errors so exit
                break
            else:
                # success - can scrape the result
                # ...
                
                num_errors = 0
                
# 三、链接爬虫
def link_crawler(seed_url, link_regex=None, delay=5, user_agent='wswp', max_urls=-1,\
max_depth=1, headers=None, proxy=None, num_retries=1):
    #Crawl from the given seed URL following links matched by link_regex
    crawl_queue = Queue.deque([seed_url])
    
    #设置深度
    seen = {seed_url:0}
    # track how many URL's have been downloaded
    num_urls = 0
    rp = get_robots(seed_url)
    
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)
            links =[]
            
            depth = seen[url]
            if depth != max_depth:
                #can still craql further
                if link_regex:
                    #filter for links matching our regular expression
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))
                for link in links:
                    link = normalize(seed_url, link)
                    #check whether already crawled this link
                    if link not in  seen:
                        seen[link] = depth + 1
                        crawl_queue.append(link)
            
            #check whether have reached downloaded maxinum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print 'Blocked by robots.txt:', url

# 匹配链接
def get_links(html):
    # Return a list of links from html
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)
    
def get_robots(url):
    """Return True if both URL's belong to same domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp

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
            


if __name__ == '__main__':
    url = 'http://example.webscraping.com'
    link_regex = '/(index|view)'
  
    link_crawler(url, link_regex,delay=5, user_agent='BadCrawler')
    link_crawler(url, link_regex,delay=5, user_agent='GoodCrawler')
    #head = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    #download(url, head)