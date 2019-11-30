# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class YelpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hospital_id = scrapy.Field()
    url = scrapy.Field()
    review = scrapy.Field()
    review_date = scrapy.Field()
    rating = scrapy.Field()