# -*- coding: utf-8 -*-


import requests
import json
import csv
import time
import random

from collections import OrderedDict
from urllib import urlencode
from custom_functions import convert, params_list_list

nb_pages_to_scrape = 80
set_cookie_parameter = "_ruby-web_session=T0xrN2lFU2ozV1hBWWRHTGVlVUNQU3NMUkI4cDFraXREcFErVVUwWW9icWNhZjZxSUgxTCt6Z0hoTC8rQy9YbnZLRU10d2JSN1BSaWtjanFleGV2Z2I4emxYeTlxOVNTMlIvcndGVkJLK1cyWUpETkZRS00ycTdQZ2FST0RJbnQ4M3lINnpLS1dUa3pVdzJzNVlyWGZFN0NjVkRaVjYydFVRc3dJd01vMW9pUnpGU1JpYThoT251b1BRUTV5eDRzQkcrQkNVY3R0ek52NGd5VlVjdERvZVFpY0pNQWswNXlLcjlkNFNXRmxaRm9Ic0FjN2tZdmlMSnh5UkRKMnRXWDBpRlJ4UXpqdkViS2QxOXNqL3hFZFE9PS0tUUF3dC9lcVJldmEzV0hLN2ZVekVHdz09--d3b63a15ec5f4a20a62a0e7aa99c122eb9481cae; path=/; expires=Fri, 22 Mar 2019 08:38:02 -0000; HttpOnly; secure; SameSite=Lax"

with open('wines_1.csv', 'wb') as output_file:
	fieldnames = ['vintage_id','vintage_name','vintage_ratings_average','vintage_ratings_count','wine_id','wine_name','wine_country','wine_region_name','winery_name','wine_year']
	dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
	dict_writer.writeheader()

	for page_nb in range(1,nb_pages_to_scrape+1):

	# insight: this api is only able to handle 2000 wines per request type. We have to make the params vary.
	# proposed strategy: for each wine_type (red, white, rose, mousseux), make 5 requests:
	# price 5-15, 15-25, 25-50, 50-100, 100-500
	# min_rating is set at 1 to cover the largest rating interval
		for params_list in params_list_list(page_nb):
			print(params_list)
			params = params_list

			headers = {
				"authority": "www.vivino.com",
				"method": "GET",
				"path": "/api/explore/explore?vc_only=&country_code=fr&state=&price_range_min=5&price_range_max=500&min_rating=1&page=3",
				"scheme": "https",
				"accept": "application/json, text/javascript, */*; q=0.01",
				"accept-encoding": "gzip, deflate, br",
				"accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
				"cookie": "_ga=GA1.2.215528436.1520868257; __auc=a5369fdf1621acff2d8e115eee9; eeny_meeny_wine_style_awards_2018_v1=uaOLi79KZx4EIPEimb9L1TYFhfInBunvupCt1QCVorNmOKeRA2t7OqpW2LDkC8cJKMvaiY%2BWRzi5zsKB3eaCGA%3D%3D; eeny_meeny_vc_premium_v1=i2PlMjxhrGWjItpZqxyYX3lBuyCOicQCBwRWQIYrdWJ9FlP%2BLJ7VgUbn08MkVzqDjRpFaSNKngE244JBvTyAgw%3D%3D; eeny_meeny_test_carttaxshipping_v1=%2FKrPX7BlS00j1d9sidUCSZdESHeapD2HneNHs3312T6Qet9SfhrBlPYDZJpimB22EzS2tXqMw%2BcqqjQHqnP2%2BQ%3D%3D; eeny_meeny_test_winepage_newbrowsertab_v1=E0tIQzG0%2BHHiCigZ1UXVdRKwB%2FrikG6TZ%2BL%2BoiJZlShMBk516EYOe9vMijsf95pQt5aadNd0WFRsrS9VFoPHcA%3D%3D; eeny_meeny_vc_premium_v2=jiqTvUgFG1C%2FBNHeFCRHomRu0wmDBLznrmB6CW4YSb3aKhGcIsJrcdvYO9Qcw0KwV9Ckj%2FcjdSGnDI9kL%2Fpq4A%3D%3D; _gid=GA1.2.240279343.1521578747; _hp2_ses_props.3503103446=%7B%22r%22%3A%22https%3A%2F%2Fwww.vivino.com%2Fexplore%3Fe%3DeJzLLbI1VMvNzLM1UMtNrLA1NTBQKy-JjrU1UUuuLAbSmSUAuWgK5A%253D%253D%22%2C%22ts%22%3A1521641244372%2C%22d%22%3A%22www.vivino.com%22%2C%22h%22%3A%22%2Fexplore%22%7D; recently_viewed=aWpjQUV3anFCK1pJVE5xV0htaWM4U2NCOUdSemxvR1pQdDV6Qm9zTWtrS3pTc1U0Um14TEdnbzNXTHRnNHR4bDRpWjlaMjJDUmJWbE9oUGovUlFzNWFSaXhGSXM0c2hWaXdTY09wS0hlNlIrbzA1L0t6OVp1UFFWejlyK2NpNzNFeTBjMmltSktZZWEva044Q0o5L2V3RmdVZlN4TWlabytQbWZNWjJxZE4xTjlyVHM5L1NZSjUvR01qdkpIS0JVZGgxUXVRSEhuaFZJbFJmeSs5eDJvZHVsQnlWT1ZPWm56T2d2eDJKVWllRT0tLTJaNmZ6N2NmeFU2RjdJY3lURVZ4UUE9PQ%3D%3D--c6685738f087aae0fa4064b1db119e5f1ebf56db; __asc=f1c6878516248e2d569d6c29ef8; _hp2_id.3503103446=%7B%22userId%22%3A%222809523036173563%22%2C%22pageviewId%22%3A%225764464538583910%22%2C%22sessionId%22%3A%225306427518517338%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; " + set_cookie_parameter,
				"referer": "https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1VctNrLA1NTBQS660TStSKwCKF9uqlSXbAgDBlQqV",
				"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
				"x-csrf-token": "iamaTBTf6vdqxjWfAHcPJHEmZ84xUGO/9xpOJvgHmzi1PSafesVQ81QsdNQhmccQQcyj54WvW7GE8CmxNzoWbA==",
				"x-newrelic-id": "Vw8OVFVTGwADVFBWBAU=",
				"x-requested-with": "XMLHttpRequest"
				}

			r = requests.get("https://www.vivino.com/api/explore/explore?", params=urlencode(params), headers=headers)			
			set_cookie_parameter = r.headers['Set-Cookie']
			r = r.json()
			r = r['explore_vintage']['records']
			r = convert(r)

			#delay = random.randint(1,2)
			print("Scraping page " + str(page_nb))# + " (after " + str(delay) + "s)...")
			#time.sleep(delay)

			for wine_card in r:

				wine = {
					'vintage_id' : wine_card['vintage']['id'],
					'vintage_name' : wine_card['vintage']['name'],
					'vintage_ratings_average' : wine_card['vintage']['statistics']['ratings_average'],
					'vintage_ratings_count' : wine_card['vintage']['statistics']['ratings_count'],
					'wine_id' : wine_card['vintage']['wine']['id'],
					'wine_name' : wine_card['vintage']['wine']['name'],
					'wine_country' : wine_card['vintage']['wine']['region']['country']['name'],
					'wine_region_name' : wine_card['vintage']['wine']['region']['name'],
					'winery_name' : wine_card['vintage']['wine']['winery']['name'],
					'wine_year' : wine_card['vintage']['year']
				}	

				dict_writer.writerow(wine)
				
