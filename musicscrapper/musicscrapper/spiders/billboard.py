# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime, timedelta
import scrapy

class BillboardSpider(scrapy.Spider):
    name = "billboard"
    allowed_domains = ["www.billboard.com"]
    start_urls = ['https://www.billboard.com/']
    billboard_url = 'http://www.billboard.com/charts/billboard-200/'
    currDate = datetime.now()
    startDate = datetime(2017, 1, 9)
    records = "records.json"
    Albums = []
    Artists = []
    def start_requests(self):
        date = self.startDate
        while date <= self.currDate:  # requests and enqueue all the articles from start_date to now
            new_request = scrapy.Request(self.generate_url(date),callback=self.parse)  # generate and request next URL
            new_request.meta["date"] = date
            yield new_request
            date += timedelta(weeks=1)
        pass
    def generate_url(self, date):
        url = self.billboard_url + date.strfqtime("%Y-%m-%d")
        return url

    def parse(self, response):
        # generate new requests here
        date = response.meta['date']
        try:
            #ipdb.set_trace()
            album_details = response.xpath('//div[@class="chart-row__main-display"]').extract()
            Albums_list = response.xpath('//h2[@class="chart-row__song"]//text()').extract()
            artist_list = response.xpath('//a[@class="chart-row__artist"]//text()').extract()
            Albums_and_Artists = response.xpath('//h2[@class="chart-row__song"]//text()' or
                                                '//a[@class="chart-row__artist"]//text()').extract()
            container = response.xpath('//div[@class="chart-row__container"]//text()').extract()
            Albums_and_Artists_1 = iter(Albums_and_Artists)
            Albums_and_Artists_2 = list(zip(Albums_and_Artists_1,Albums_and_Artists_1))
            for album in Albums_list:
                self.Albums.append(album.strip())
            for artist in artist_list:
                self.Artists.append(artist.strip())
            if(len(self.Albums) == len(self.Artists)):
                Records = {"Day":date.day,
                           "Month":date.month,
                           "Records":[{'Albums': albums,
                                       'Artists':artists} for albums, artists in zip(self.Albums, self.Artists)]}

                # sort records if a list
            #Records.sort(key=lambda chart: timedelta(chart['year'], chart['month'], chart['day']).total_seconds())
                try:
                    print("print to File")
                    with open(self.records,'a+') as f:
                        json.dump([ Records ],f,sort_keys=True)
                    return Records
                except IOError as err:
                    print("I/O error: {0}".format(err))

        except IndexError as err:
            print("The list index differs from Albums to Artists".format(err))
