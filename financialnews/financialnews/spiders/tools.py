# -*- coding: utf-8 -*-


import re
import urlparse
import urllib2
# import sys
# type = sys.getfilesystemencoding()
import zlib

def download(url, proxy = None, num_retries = 1, data=None):
    print 'Downloading:', url
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    request = urllib2.Request(url, data, headers)
    request.add_header('Accept-encoding', 'gzip')
    opener = urllib2.build_opener()

    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        response = opener.open(request)
        html = response.read()
        gzipped = response.headers.get('Content-Encoding')
        # http://blog.csdn.net/ws491360104/article/details/50534863
        if gzipped:
            html = zlib.decompress(html, 16+zlib.MAX_WBITS)
        code = response.code
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                html = download(url, headers, proxy, num_retries-1, data)
        else:
            code = None
    return html

def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

if __name__ == '__main__':
    # html = download('http://www.douban.com')
    html = download('http://www.financialnews.com.cn').decode("utf-8")
    links = get_links(html)
    print(links)
