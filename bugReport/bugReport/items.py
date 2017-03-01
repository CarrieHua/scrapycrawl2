# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BugreportItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    bug_id = scrapy.Field()
    Status = scrapy.Field()
    Product = scrapy.Field()
    Component = scrapy.Field()
    Version = scrapy.Field()
    Platform = scrapy.Field()
    Importance = scrapy.Field()
    AssignedTo = scrapy.Field()
    TriageOwner = scrapy.Field()
    Reported = scrapy.Field()
    Reporter = scrapy.Field()
    Modified = scrapy.Field()
    CC = scrapy.Field()
    #Attachments = scrapy.Field()
    Description = scrapy.Field()
    Comments = scrapy.Field()
    Num_comment = scrapy.Field()

