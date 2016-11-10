import scrapy
import urlparse
import re
import os.path
from lxml import etree
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from craigslist_sample.items import TelegraphItem
from scrapy.utils.response import body_or_str

class MySpider(CrawlSpider):
    name = "tel"
    allowed_domains = ["telegraph.co.uk"]
    start_urls = ["http://www.telegraph.co.uk/"]

    base_url = 'http://www.telegraph.co.uk/archive/'
    year = ['2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005']
    month = ['12','11','10','09','08','07','06','05','04','03','02','01']
    day = ['31','30','29','28','27','26','25','24','23','22','21',
        '20','19','18','17','16','15','14','13','12','11','10',
          '9','8','7','6','5','4','3','2','1']

    def parse(self,response):
        for y in self.year:
            for m in self.month:
                for d in self.day:
                    url = self.base_url+y+'-'+m+'-'+d+'.html#News'
                    yield scrapy.Request(url,self.parseList)

    def parseList(self, response):
        sel = Selector(response)
        articles = sel.xpath('//div[@class="summary"]/h3/a/@href').extract()
        for article in articles:
            yield scrapy.Request(urlparse.urljoin('http://www.telegraph.co.uk', article[1:]), callback=self.parse_items)

    def parse_items(self, response):
        hxs = Selector(response)
        items = []
        item = TelegraphItem()
        item["title"] = hxs.xpath('//h1[@itemprop="headline name"]/text()').extract()[0]
        article = hxs.xpath('//div[contains(@class, "firstPar") or contains(@class, "secondPar") or contains(@class, "thirdPar") or contains(@class, "fourthPar") or contains(@class, "fifthPar")]/p/text()').extract()
        item["article"] = "\n".join(article).encode('utf8')
        item['link'] = response.url
        item["date"] = hxs.xpath('//meta[@name="last-modified"]/@content').extract()[0].encode('utf8')
        items.append(item)

        return items