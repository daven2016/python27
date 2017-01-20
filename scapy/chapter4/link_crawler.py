# -*- coding: utf-8 -*-
import Queue
import re
import urlparse
import robotparser

from downloader import Downloader, ScrapeCallback

def link_crawler(seed_url, link_regex=None, delay=5, user_agent='wswp', max_urls=-1,
                 max_depth=1, proxy=None, num_retries=1, call_back=None, cache=None):
    # Crawl from the given seed URL following links matched by link_regex
    crawl_queue = Queue.deque([seed_url])

    # 设置深度
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    num_urls = 0
    rp = get_robots(seed_url)

    down = Downloader(delay=delay, user_agent=user_agent, proxies=proxy, num_retries=num_retries, cache=cache)

    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            html = down(url)

            links = []
            if call_back:
                call_back(url, html)

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


# 匹配链接
def get_links(html):
    # Return a list of links from html
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link)  # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)


def get_robots(url):
    """Return True if both URL's belong to same domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


if __name__ == '__main__':
    scrap_callback = ScrapeCallback()
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1,
                 user_agent='BadCrawler', call_back=scrap_callback)
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=3,
                 user_agent='GoodCrawler', call_back=scrap_callback)