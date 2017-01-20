# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 13:54:02 2017

@author: Administrator
"""

# Lxml 用法：
#*************************************************************************
import lxml.html
from chapter1 import download

'''
broken_html = '<ul class=country><li>Area<li>Population</ul>'
tree = lxml.html.fromstring(broken_html)  #parser the HTML
fixed_html = lxml.html.tostring(tree, pretty_print=True)
print fixed_html
'''

url = 'http://example.webscraping.com/places/view/United-Kingdom-239'
headers = {'User-Agent': 'GoodCrawler'}
html = download(url, headers)

tree = lxml.html.fromstring(html)
td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
area = td.text_content()
print area


#*************************************************************************

'''
# BeautifulSoup 用法：
#**************************************************************************
from bs4 import BeautifulSoup
from chapter1 import download

url = 'http://example.webscraping.com/places/view/United-Kingdom-239'
headers = {'User-Agent':'GoodCrawler'}
html = download(url, headers)
soup = BeautifulSoup(html, 'html.parser')

#locate the area row
tr = soup.find(attrs={'id':'places_area__row'})

td =  tr.find(attrs={'class':'w2p_fw'})  #locate the area tag
area = td.text #extract the text from this tag
print area
'''
"""
broken_html = '<ul class=country><li>Area<li>Population</ul>'

#parse the HTML
soup = BeautifulSoup(broken_html, 'html.parser')
fixed_html = soup.prettify()
print fixed_html

ul = soup.find('ul',attrs={'class':'country'})
ul.find('li')  #returns just the first match

ul.find_all('li')  #returns all match
"""
#*****************************************************************************