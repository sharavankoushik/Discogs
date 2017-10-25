# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import CrawlSpider, BaseSpider, Rule
from scrapy.selector import Selector
import json

class TestSpider(BaseSpider):
    name = "test"
    allowed_domains = ["https://www.discogs.com"]
    form_data = {'title': "Witness", 'artist': "Katy Perry", 'type': "master"}
    start_urls = ['https://www.discogs.com/search/?type=' + form_data.get('type') + '&title=' + form_data.get(
        'title') + '&artist=' + form_data.get('artist')]
    records = "Album_info.json"

    def parse(self, response):
        hxs = Selector(response)
        master_records = hxs.xpath('//*[@id="search_results"]//a[@class="search_result_title"]/@href').extract()
        #redirect to the master records
        url2 = ''.join(self.allowed_domains+master_records)
        new_request =  Request(url=url2,callback=self.parse_records,dont_filter=True)
        yield new_request

    def parse_records(self,response):
        hxs = Selector(response)
        Album_logo= hxs.xpath('//span[@class="thumbnail_center"]//img/@src').extract_first()
        Album_Genre = hxs.xpath('//div[@itemprop="genre"]//a//text()').extract()
        tracklist = response.xpath(
            '//table[@class="playlist"]//td//span[contains(@itemprop, "name")]//text()').extract()
        timespan = response.xpath(
            '//table[@class="playlist"]//td[@class="tracklist_track_duration"]//span//text()').extract()
        Album_info = [{"trackname":tlist,"duration":span} for tlist,span in zip(tracklist,timespan)]
        data = []
        data.append({
            "Album":self.form_data.get('title'),
            "Artist":self.form_data.get('artist'),
            "Albumart":Album_logo,
            "Genre":Album_Genre,
            "Album Info":Album_info
        })

        try:
            print("print to File")
            with open(self.records, 'a+') as f:
                json.dump(data, f)
        except IOError as err:
            print("I/O error: {0}".format(err))
        return data





