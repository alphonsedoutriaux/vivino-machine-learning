# -*- coding: utf-8 -*-

import scrapy
from wikipedia.items import AOC
from scrapy.loader import ItemLoader


class QuotesSpider(scrapy.Spider):



    name = "wikipedia"



    def start_requests(self):
		url = "https://fr.wikipedia.org/wiki/Liste_des_vins_AOC_fran%C3%A7ais"
		yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):

        # go to aoc page
        for aoc in response.css('td:nth-child(1) a'):
            aoc_short_link = str(aoc.css('a::attr(href)').extract_first())
            aoc_page_link = "https://fr.wikipedia.org" + aoc_short_link
            yield response.follow(aoc_page_link, self.parse_aoc_details)

    def parse_aoc_details(self, response):

        loader = ItemLoader(item=AOC(), response=response, selector=response)
        loader.add_css('name', '#firstHeading')
        loader.add_css('area', '.infobox_v2')
        loader.add_css('production_volume', '.infobox_v2')
        
        return loader.load_item()