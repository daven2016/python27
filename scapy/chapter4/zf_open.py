import csv
from zipfile import ZipFile
from StringIO import StringIO

def get_urls():
    with open('top-1m.csv.zip', 'rb') as f:
        zipped_data = f.read()
        urls = []

        with ZipFile(StringIO(zipped_data)) as zf:
            csv_filename = zf.namelist()[0]
            for _, website in csv.reader(zf.open(csv_filename)):
                urls.append('http://' + website)
        #print len(urls)
    return urls

class AlexaCallback:
    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        #self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
        self.filename = r'E:\learngit\python27\scapy\chapter4\top-1m.csv.zip'
    def __call__(self):
        with open(self.filename, 'rb') as f:
            zipped_data = f.read()
            urls = []
            i = 1
            with ZipFile(StringIO(zipped_data)) as zf:
                csv_filename = zf.namelist()[0]
                for _, website in csv.reader(zf.open(csv_filename)):
                    if i > self.max_urls:
                        break
                    urls.append('http://' + website)
                    i += 1
                    # print len(urls)
            return urls

if __name__ == '__main__':
    callback = AlexaCallback(100)
    print len(callback())