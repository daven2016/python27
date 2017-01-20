# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:18:08 2017

@author: Administrator
"""

import lxml.html
from downloader import Downloader
import json


D = Downloader()
html = D('http://example.webscraping.com/dynamic')

tree = lxml.html.fromstring(html)
print tree.cssselect('#result')[0].text_content()
'''
import string

template_url = 'http://example.webscraping.com/ajax/search.json?page={}&page_size=10&search_term={}'
countries = set()

for letter in string.lowercase:
    page = 0
    while True:
        html = D(template_url.format(page, letter))
        try:
            ajax = json.loads(html)
        except ValueError as e:
            print e 
            ajax = None
        else:
            for record in ajax['records']:
                countries.add(record['country'])
        page += 1
        if ajax is None or page >= ajax['num_pages']:
            break
open('countries.txt', 'w').write('\n'.join(sorted(countries)))


# 改进之后
import csv

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld',
          'currency_code', 'currency_name', 'phone', 'postal_code_format',
          'postal_code_regex', 'languages','neighbours')
writer = csv.writer(open('countries.csv', 'w'))
writer.writerow(FIELDS)
html = D('http://example.webscraping.com/ajax/search.json?page=0&page_size=1000&search_term=a')
ajax = json.loads(html)
for record in ajax['records']:
    row = [record[field] for field in FIELDS]
    writer.writerow(row)
'''