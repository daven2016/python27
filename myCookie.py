# -*- coding: utf-8 -*-
import urllib2
import cookielib
'''
#Cookie 的保存：
#****************************************************************
#方法一：保存到时文件中
#设置保存cookie的文件，同级目录下的cookie.txt
filename = 'cookie.txt'

#声明一个MozillaCookieJar对象实例来保存cookie,之后定入文件
cookie = cookielib.MozillaCookieJar(filename)

#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)

#通过 handler 来构建 opener
opener = urllib2.build_opener(handler)

#此处的open方法同urllib2的方法，也可以传入Request
response = opener.open('http://www.baidu.com')

#保存cookie到文件,在这里，我们将这两个全部设置为True。
#ignore_discard的意思是即使cookies将被丢弃也将它保存下来，
#ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入.
cookie.save(ignore_discard=True, ignore_expires=True)


#方法二：保存到变量中
#声明一个CookieJar对象实例来保存cookie
#cookie = cookielib.CookieJar()

#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)

#通过 handler 来构建 opener
opener = urllib2.build_opener(handler)

#此处的open方法同urllib2的方法，也可以传入Request
response = opener.open('http://www.baidu.com')

for item in cookie:
    print 'Name = ' + item.name
    print 'Value = ' + item.value

#*********************************************************************

#2、从文件中获取Cookie并访问
#********************************************************************
#创建MozillaCookieJar实例对象
cookie = cookielib.MozillaCookieJar()

#从文件中读取cookie内容到变量
cookie.load('cookie.txt',ignore_discard=True,ignore_expires=True)

#创建请求的request
req = urllib2.Request('http://www.baidu.com')

#利用urllib2的build_opener方法创建一个opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)
print response.read()
#********************************************************************
'''
#3、利用cookie模拟网站登录
#********************************************************************
import urllib

filename = 'cookie.txt'
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({
    'susername':'583626952@qq.com',
    'ppassword':'lode1214'})

loginUrl = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'
req = urllib2.Request(loginUrl,postdata)
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
result = opener.open(req)
cookie.save(ignore_discard=True,ignore_expires=True)

#anotherUrl = 'http://my.csdn.net/my/score'
#result = opener.open(anotherUrl)
print result.read()
#********************************************************************
