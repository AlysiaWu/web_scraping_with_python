# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from financialnews.items import FinancialnewsItem
from items import FinancialnewsItem
import re

class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['www.financialnews.com.cn']
    start_urls = ['http://www.financialnews.com.cn/']

    rules = (
        Rule(LinkExtractor(allow='/hg/'), follow=True),     # 宏观，只有一级目录
        Rule(LinkExtractor(allow='/pl/'), follow=True),     # 评论，有二级目录
        Rule(LinkExtractor(allow='/t\d{8}_\d*.html$'), callback='parse_news'),
    )

    def parse_news(self, response):
        item = FinancialnewsItem()
        titles = response.css('div.content_title').extract()
        item['title'] = self.normalLize(titles[0]) if len(titles) > 0 else ''
        timestamps = response.css('div.content_info span:nth-child(3)').extract()
        item['timestamp'] = self.normalLize(timestamps[0]) if len(timestamps) > 0 else ''
        contents = response.css('div.content_body div.TRS_Editor div.Custom_UnionStyle').extract()
        item['content'] = self.normalLize(contents[0]) if len(contents) > 0 else ''
        return item

    def normalLize(self, html):
        if type(html) == 'unicode':
            html = html.encode('utf-8')
        dr = re.compile(r'<[^>]+>', re.S)
        res = dr.sub('',html)
        return res
