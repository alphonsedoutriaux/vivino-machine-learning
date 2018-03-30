# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import unicodedata

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst



def to_string(text):
	if isinstance(text, unicode):
		text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
	return(text)

def strip_html(text):
    p = re.compile(r'<.*?>')
    return(p.sub('', text))

def name_cleaner(text):
	text = text.replace(" (AOC)", "")
	text = text.lower()
	return(text)

def production_volume_finder(text):
	text_to_list = text.split("\n")
	for index, element in enumerate(text_to_list):
		if element.lower() == "production":
			return(text_to_list[index+1])

def production_volume_cleaner(text):
	text = text.replace("hectolitres", "hl")
	text = text.split("hl")[0]
	text = text.replace(" ", "")
	text = int(text)
	return(text)

def area_finder(text):
	text_to_list = text.split("\n")
	for index, element in enumerate(text_to_list):
		if element.lower() == "superficie plantee":
			return(text_to_list[index+1])

def area_cleaner(text):
	text = text.replace("hectares", "ha")
	text = text.replace("hectare", "ha")
	text = text.split("ha")[0]
	text = text.replace(',', '.')
	text = text.replace(' ', '')
	text = round(float(text), 0)
	text = int(text)
	return(text)

class AOC(scrapy.Item):
    
    name = scrapy.Field(
    	input_processor=MapCompose(strip_html, to_string, name_cleaner),
		output_processor=TakeFirst()
		)

    area = scrapy.Field(
    	input_processor=MapCompose(strip_html, to_string, area_finder, area_cleaner),
		output_processor=TakeFirst()
		)

    production_volume = scrapy.Field(
    	input_processor=MapCompose(strip_html, to_string, production_volume_finder, production_volume_cleaner),
		output_processor=TakeFirst()
		)
    pass
