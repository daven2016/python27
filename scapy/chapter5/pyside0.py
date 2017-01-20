# -*- coding: utf-8 -*-

from PySide.QtGui import QApplication
from PySide.QtCore import QUrl, QEventLoop, QTimer
from PySide.QtWebKit import QWebView
import lxml.html

app = QApplication([])
webview = QWebView()
loop = QEventLoop()
webview.loadFinished.connect(loop.quit)
webview.load(QUrl('http://example.webscraping.com/search'))
loop.exec_()
'''
html = webview.page().mainFrame().toHtml()
tree = lxml.html.fromstring(html)
print tree.cssselect('#result')[0].text_content('1000')'''

webview.show()
frame = webview.page().mainFrame()
frame.findFirstElement('#search_term').setAttribute('value', '.')
frame.findFirstElement('#page_size option:checked').setPlainText('1000')
frame.findFirstElement('#search').evaluateJavaScript('this.click()')
app.exec_()


