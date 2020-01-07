# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PTTArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=scrapy.Field()
    articel_id=scrapy.Field()
    articel_author=scrapy.Field()
    articel_title=scrapy.Field()
    articel_date=scrapy.Field()
    articel_content=scrapy.Field()
    ip=scrapy.Field()
    message_count=scrapy.Field()
    messages=scrapy.Field()

