# -*- coding: utf-8 -*-
import lxml.html
import urllib2, urllib
import pprint
import cookielib
import browsercookie
import os
import time
import json
import glob

LOGIN_URL = 'http://example.webscraping.com/user/login'
LOGIN_EMAIL = 'daven_long@foxmail.com'
LOGIN_PASSWORD = '326326326'

def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}

    for e in tree.cssselect('form input'):
        #print e.get('name'), e.get('value')
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data

def login_url(url):
    # 添加cookie (_formkey 的值会保存在cookie中，然后该值会与提交的登录表单数据中的_formkey值进行对比)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    # 获取登录的隐藏域
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)

    # 设置登录邮箱和密码域
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD

    encoded_data = urllib.urlencode(data)
    req = urllib2.Request(url, encoded_data)
    response = opener.open(req)
    print response.geturl()
    return opener

def load_ff_sessions(session_filename):
    cj = cookielib.CookieJar()
    if os.path.exists(session_filename):
        json_data = json.loads(open(session_filename, 'rb').read())
        for window in json_data.get('windows', []):
            for cookie in window.get('cookies', []):
                c = cookielib.Cookie(0, cookie.get('name', ''),
                    cookie.get('value', ''), None, False,
                    cookie.get('host', ''),
                    cookie.get('host', '').startswith('.'),
                    cookie.get('host', '').startswith('.'),
                    cookie.get('path', ''), False, False,
                    str(int(time.time()) + 3600 * 24 * 7),
                    False, None, None, {})
                cj.set_cookie(c)
    else:
        print 'Session filename does not exist:', session_filename
    return cj


def find_ff_sessions():
    paths = [
        '~/.mozilla/firefox/*.default',
        '~/Library/Application Support/Firefox/Profiles/*.default',
        'C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/7p70qzqu.default/sessionstore-backups'
    ]
    for path in paths:
        filename = os.path.join(path, 'recovery.js')

        matches = glob.glob(os.path.expanduser(filename))
        if matches:
            return matches[0]

if __name__ == '__main__':
    #login_url(LOGIN_URL)

    URL = 'http://example.webscraping.com/edit/United-Kingdom-239'
    opener = login_url(LOGIN_URL)
    country_html = opener.open(URL).read()

    data = parse_form(country_html)
    pprint.pprint(data)
    data['population'] = int(data['population']) + 3
    encoded_data = urllib.urlencode(data)
    req = urllib2.Request(URL, encoded_data)
    response = opener.open(req)
    '''
    # 获取Firefox浏览器recovery.js文件中的cookie
    session_filename = find_ff_sessions()
    print session_filename
    cj = load_ff_sessions(session_filename)
    processor = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(processor)
    url = 'http://example.webscraping.com'
    html = opener.open(url).read()
    tree = lxml.html.fromstring(html)
    print tree.cssselect('ul#navbar li a')[0].text_content()
    '''