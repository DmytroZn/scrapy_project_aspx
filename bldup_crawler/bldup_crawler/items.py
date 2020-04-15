# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

import datetime


class BldupCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    date: datetime = scrapy.Field()
    type: str = scrapy.Field()
    book: str = scrapy.Field()
    page_num: str = scrapy.Field()
    doc_num: str = scrapy.Field()
    city: str = scrapy.Field()
    description: str = scrapy.Field()
    cost: float = scrapy.Field()
    street_address: str = scrapy.Field()
    state: str = scrapy.Field()
    zip: str = scrapy.Field()
