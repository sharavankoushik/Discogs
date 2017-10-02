# -*- coding: utf-8 -*-
import json

from scrapy import Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider


class TestSpider(BaseSpider):
    name = "DiscogsDemo"
    allowed_domains = ["https://www.discogs.com"]
    form_data = {'title': "Rainbow", 'artist': "Kesha", 'type': "master"}
    start_urls = ['https://www.discogs.com/search/?type=' + form_data.get('type') + '&title=' + form_data.get(
        'title') + '&artist=' + form_data.get('artist')]
    records = "Album_info.json"
    urls = []
    billboardData = "musicscpapper/records.json"

    #If we get the Album name and Artists name from the json file
    def parse_json(self):
        with open(self.billboardData,'r') as f:
            jsonload = json.loads(f.read())
            for week_year_no in range(1,len(jsonload)):
                records = jsonload[week_year_no].get('Records')
                for i in range(0,len(records)):
                    Album_name = records[i].get('Albums')
                    Artist_name = records[i].get('Artists')
                    url = self.urls.append('https://www.discogs.com/search/?type=master'+'&title='+Album_name+'&artist='+Artist_name)
        return self.urls

    def parse(self, response):
        hxs = Selector(response)
        master_records = hxs.xpath('//*[@id="search_results"]//a[@class="search_result_title"]/@href').extract()
        #redirect to the master records
        url2 = ''.join(self.allowed_domains+master_records)
        import ipdb;ipdb.set_trace()
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





