# -*- coding: utf-8 -*-
import mechanize

LOGIN_URL = 'http://example.webscraping.com/user/login'
LOGIN_EMAIL = 'daven_long@foxmail.com'
LOGIN_PASSWORD = '326326326'
URL = 'http://example.webscraping.com/edit/United-Kingdom-239'

br = mechanize.Browser() # 创建一个Mechanize浏览器对象
br.open(LOGIN_URL) # 定位到登录URL
br.select_form(nr=0) # 选择登录表单
br['email'] = LOGIN_EMAIL  #向浏览器对象传递名称和值，来设置选定表单的输入框内容。
br['password'] = LOGIN_PASSWORD
#print br.form  # 获取提交之前的表单状态
response = br.submit()

br.open(URL)
br.select_form(nr=0)
print br.form
br['population'] = str(int(br['population']) + 1)  #需要转成字符串类型
print br.form
br.submit()