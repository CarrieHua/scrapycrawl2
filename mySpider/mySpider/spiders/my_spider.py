#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Spider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from mySpider.items import MyspiderItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MySpider(Spider):
    name = "mySpider"
    
    def start_requests(self):
        url = "https://bugs.eclipse.org/bugs/buglist.cgi?bug_status=REOPENED&classification=Tools&query_format=advanced"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
         self.log('Hi, this is an item pages! %s' % response.url)
         item = MyspiderItem()
         #item['url'] = response.xpath('//td[@class="first-child bz_id_column"]/a/@href').extract()
         #print item['url']
         item['bug_id'] = response.xpath('//td[@class="first-child bz_id_column"]/a/text()').extract()
         return item


        
