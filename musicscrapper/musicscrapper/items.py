# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
import scrapy
from Music.models import Albums,Songs,Office

class MusicscrapperItem(DjangoItem):
    django_model = Office
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GoogleSearchItem(DjangoItem):
    name =  scrapy.Field()
    region = scrapy.Field()
    url = scrapy.Field()
    html = scrapy.Field()
    query = scrapy.Field()
    crawled = scrapy.Field()
