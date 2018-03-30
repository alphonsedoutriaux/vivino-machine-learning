# -*- coding: utf-8 -*-
import requests
import json
import numpy as np 
import time
import random
import csv

from collections import OrderedDict
from urllib import urlencode

# import the vintage_id list
vintage_ids = np.loadtxt("wines.csv", usecols=[0], dtype='str', delimiter=",", skiprows=1).tolist()
# here we split the vintages_ids in sublists of length 25 in order not to overload vivino.com
vintage_ids_25 = [vintage_ids[x:x+25] for x in range(0, len(vintage_ids),25)]

# the request url is sth like /api/prices?vintage_ids[]=XXX&vintage_ids[]=XXX
# we can not pass a dict as request params as a dict cannot have duplicate keys
# we append a string with the ids of a sublist...
url_end = ""
i=0
set_cookie_parameter = "_ruby-web_session=UEJzNjVYNmdHTGRqL0VNeEQxd3o2S3pRMFhlYmxiRXduL01vZlkvOEpTUHRqZHdQYjRrMnlPRWVpdFpqS3pWcXNGclhzT2lDQlRiSy93YjYvYnQ3eTNKSEEwTk1POGJkdTVFTXdQbkFYREZEb2UwWUJwQzJJVlR4OHVNazlPTlhPMW9lV2VuektrLzU0dFlGNGplak5IYytHTmFFZEs0bjhWVDdiWGdrUjlNRzNKNWxvQWhnTXBLbnJoWDlzTEVWWGlPa2Y1RFZzUEw4MEIvQzVxM25pTDhSRGhrdDcyNzBwUVM5bzE3RDVkODE3emFQcFYrT2paN1BLVDhQTEtFMWcxdll6V1lkT2tUcUZSamQ2V0lSd1E9PS0teHBvaWx4aWRsNjZOSW10Z1l4TUY4QT09--8fe71d94b267c9635a29eac737f2332449620d09"

with open('prices.csv', 'wb') as output_file:
	fieldnames = ['vintage_id','price']
	dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
	dict_writer.writeheader()

	for sublist in vintage_ids_25:
		i += 1
		url_end = ""
		for vintage_in_sublist in sublist:
			url_end = url_end + "vintage_ids[]=" + vintage_in_sublist +"&"

		headers = {
			"authority": "www.vivino.com",
			"method": "GET",
			"path": "/api/prices?" + url_end,
			"scheme": "https",
			"accept": "application/json",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
			"content-type": "application/json",
			"cookie": "eeny_meeny_wine_style_awards_2018_v1=%2B%2BSM1o7f6jcsre8RqvLcHtZ%2BKEVy%2Bp1suLg8I54bR7juOQhi%2FmLKZnkrGix038KOJO0oBCu8JMbvsfAUtA3Q5Q%3D%3D; eeny_meeny_vc_premium_v2=wXdT1jMZorB1xP8bgPmQyfkA1uUBBPhkYRG4vqKYBr1pVaH0fptVo8Q5CEHmig92UTa0DsaKKztR79PyeWXd6g%3D%3D; eeny_meeny_test_carttaxshipping_v1=RSXieQMiPLg5hH2oRo6b2zljU1gIcsGW6iZqY%2FJelCzN7%2BZB5gb%2BnHd%2Fd6te0MurvZtRtNhToe0VKhFt0NNuRg%3D%3D; eeny_meeny_test_winepage_newbrowsertab_v1=DKlHIfL6oe5gbmu9OgvIO%2BjrGmk0SGHHRFgcCMNmRLdkw7KnIO4A5fKfBz4ODjzr%2F1Xs8Xf2vXFsJ%2BLYwkGHTA%3D%3D; _ga=GA1.2.2004000077.1521706549; _gid=GA1.2.1243452271.1521706549; _gat_vivinoTracker=1; __asc=e67840ac1624cc73d88086cec3e; __auc=e67840ac1624cc73d88086cec3e; _hp2_ses_props.3503103446=%7B%22ts%22%3A1521706549025%2C%22d%22%3A%22www.vivino.com%22%2C%22h%22%3A%22%2Fexplore%22%7D; _dc_gtm_UA-49806474-1=1; _hp2_id.3503103446=%7B%22userId%22%3A%221016524470564438%22%2C%22pageviewId%22%3A%224964203751468218%22%2C%22sessionId%22%3A%228618254851976280%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; " + str(set_cookie_parameter),
			"if-none-match": "W/\"df3570f1192befe56389c0663eff3fe1",
			"referer": "https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1VctNrLA1NTBQS660TStSKwCKF9uqlSXbAgDBlQqV",
			"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
			"x-csrf-token": "undefined",
			"x-requested-with": "XMLHttpRequest"
			}

		r = requests.get("https://www.vivino.com/api/prices?" + url_end, headers=headers)
		set_cookie_parameter = r.headers['Set-Cookie']
		
		r = r.json()
		r = r['prices']['vintages']

		#delay = random.randint(2,5)
		print("Scraping prices from page " + str(i))# + " after " + str(delay) + " second(s)... (done : " + str((i-1)*100/1960) + "%)")
		#time.sleep(delay)

		for vintage_details in r:
			vintage = {
				'vintage_id' : vintage_details,
				'price' : r[str(vintage_details)]['price']['amount']
				}
			dict_writer.writerow(vintage)

