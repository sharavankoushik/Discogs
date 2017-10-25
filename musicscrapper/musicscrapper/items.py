# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
import scrapy
from Music.models import Album,Songs


class AlbumItemScraper(DjangoItem):
    DjangoItem.django_model = Album
    #DjangoItem.django_model = Songs
    # define the fields for your item here like:
    # name = scrapy.Field()cls
    pass
