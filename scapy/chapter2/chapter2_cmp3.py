# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 15:16:49 2017

@author: Administrator
"""

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld',
          'currency_code', 'currency_name', 'phone', 'postal_code_format',
          'postal_code_regex', 'languages', 'neighbours')
          
import re
def re_scraper(html):
    results = {}
    for field in FIELDS:
        results[field] = re.search('<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' % field, html).groups()[0]
    return results
    
from bs4 import BeautifulSoup
def bs_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = {}
    for field in FIELDS:
        results[field] = soup.find('table').find('tr', id='places_%s__row' % field).find('td', class_='w2p_fw').text
    return results
    
import lxml.html
def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.cssselect('table > tr#places_%s__row > td.w2p_fw' % field)[0].text_content()
    return results
    
# 三种数据抓取方法，性能对比：    
import time
from chapter1 import download

NUM_ITERATIONS = 1000 # number of times to test each scraper
url = 'http://example.webscraping.com/places/view/United-Kingdom-239'
headers = {'User-Agent':'GoodCrawler'}
html = download(url, headers) 

for name, scraper in [('Regular expressions', re_scraper), ('BeautifulSoup', bs_scraper), ('Lxml', lxml_scraper)]:
    # record start time of scrape
    start = time.time()
    for i in range(NUM_ITERATIONS):
        if scraper == re_scraper:
            re.purge() #默认情况下，正则表达式模块会缓存搜索结果，为了公平，清除缓存
        result = scraper(html)
        #check scrapedd result is as expected
        assert(result['area'] == '244,820 square kilometres')
    #record end time of scrape and output the total
    end = time.time()
    print '%s: %.2f seconds' % (name, end - start)