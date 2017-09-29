# -*- coding: utf-8 -*-

import csv
from zipfile import ZipFile
from StringIO import StringIO
from downloader import Downloader

# Demonstrate how to download zip file, unzip it, and read the unzipped csv file.
def alexa():
    D = Downloader()
    zipped_data = D('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip')
    urls = [] # top 1 million URL's will be stored in this list
    with ZipFile(StringIO(zipped_data)) as zf:
        csv_filename = zf.namelist()[0]     # zip only contains one file.
        print 'csv_filename: ', csv_filename
        # csv file contains 2 columns: seq(id), and top domain name.
        for _, website in csv.reader(zf.open(csv_filename)):
            urls.append('http://' + website)
    return urls


if __name__ == '__main__':
    print len(alexa())
