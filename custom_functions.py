# -*- coding: utf-8 -*-
from collections import OrderedDict


def convert(input):
    if isinstance(input, dict):
        return dict((convert(key), convert(value)) for key, value in input.iteritems())
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def params_list_list(page): # gets the list of possible params combination given the prices ranges and the wine types
	params_list_list = []

	wine_types = {
		'red':'1',
		'white':'2',
		'mousseux':'3',
		'rose':'4'}

	price_ranges_list = [[5, 15], [15, 30], [30, 50], [50, 100], [100, 500]]

	for wine_type in wine_types:
		for price_range in price_ranges_list:

			params_list = OrderedDict([
				("vc_only" , ""),
				("country_code", "fr"),
				("state", ""),
				("wine_type_ids[]", str(wine_types[wine_type])), # 1 for red, 2 for white, 3 for Mousseux, 4 for rosé
				("price_range_min", str(price_range[0])),
				("price_range_max", str(price_range[1])),
				("min_rating", "1"),
				("page", str(page))])
			
			params_list_list.append(params_list)
	return(params_list_list) #returns the list of possible params list

