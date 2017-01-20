# -*- coding: utf-8 -*-
import re
import Queue
from chapter1 import download, get_links, get_robots, Throttle, normalize
from chapter2_callback import ScrapeCallback

def link_crawler(seed_url, link_regex=None, delay=5, user_agent='wswp', max_urls=-1,
                 max_depth=1, headers=None, proxy=None, num_retries=1, ScrapeCallback=None):
    # Crawl from the given seed URL following links matched by link_regex
    crawl_queue = Queue.deque([seed_url])

    # 设置深度
    seen = {seed_url: 0}
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
        if rp.can_fetch(user_agent, url):  #当传的是headers，user_agent=headers['User-Agent']!!!
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)
            links = []
            if ScrapeCallback:
                ScrapeCallback(url, html)

            depth = seen[url]
            if depth != max_depth:
                # can still craql further
                if link_regex:
                    # filter for links matching our regular expression
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))
                for link in links:
                    link = normalize(seed_url, link)
                    # check whether already crawled this link
                    if link not in seen:
                        seen[link] = depth + 1
                        crawl_queue.append(link)

            # check whether have reached downloaded maxinum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print 'Blocked by robots.txt:', url


if __name__ == '__main__':
    scrap_callback = ScrapeCallback()
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler',
                 ScrapeCallback=scrap_callback)
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, max_depth=1,
                 user_agent='GoodCrawler', ScrapeCallback=scrap_callback)