# Vivino Project
Author: A. Doutriaux - March 2018

Keywords: machine learning, vivino, scraping, wikipedia, wine, predictions, price, xgboost, randomforest, python regular expressions

### Abstract
I initiated this project with the objective to build a model able to predict the price of a wine , based on features found on vivino.com and wikipedia.com.
The geographical perimeter was set to *France*. Approximately 10k wines were scraped using a vivino api. 
Additional info on wine regions was found on wikipedia.com. More info below!





---

### Details 
#### Vivino data scraping
Getting data from vivino was not an easy part. My first try consisted in using scrapy to get data directly from the website: I experienced
a lot of difficulties to get enough data to run machine learning algorithms on it. As a final solution I used two APIs used on vivino.com (one for wine details and one for prices).
The python script can be found in these files :
* `api_prices_scraping.py`
* `api_wines_scraping.py`
* `custom_functions.py`


#### Data cleansing
This part of the work consisted in transforming scraped raw data into a clean dataset. More practically, it meant
* concatenate price and wine_details datasets (source vivino.com)
* for each wine, add two features concerning its region (source wikipedia.com - scripts for this part can be found in the `wikipedia-scraping` folder)
* keep only French wines
* shuffle the rows
* split into train and test sets


The notebook associated with this part is named `vivino_data_split.ipynb`. 

#### Data analysis (the machine learning part)
The aim of this part was to use regression algorithms to predict the price of a wine. Here are the main steps, you can find more details in the 
`vivino_data_analysis.ipynb` notebook. FYI, the initial train set shape was approx. 8000 x 11.
1. Preprocessing:

     1.1. Cleaning: a few more cleaning steps (for replacing `NaN` values mainly) were necessary

     1.2. Simplification of the region names: I used a custom `region_cleaner` function that used python regular expressions
     
     1.3. Extraction of premium categories and winery types using regular expressions again

     1.4. ...some extra stuffs (`is_brut` for Champagne, outliers removal, etc.)...

     1.5. One hot encoding of `wine_region_name`, `premium_category`, `winery_category`


2. Regression: two algorithm were implemented (XGBoost and RandomForest), with GridSearchCV to tune hyperparameters. 
Two important points:
* I implemented an in-house cross validation script (that does exactly the same thing as sklearn's cross_val) for more flexibility
* I also did a blending of predictions using a simple LinearRegression

3. Performance measurement on test set: the final R2 score on test set was 0.66. It it relatively modest, mainly because of the difficulties I had to get enough features.


The notebook associated with this part is named `vivino_data_analysis.ipynb`. 

Important notice: all of the above steps had *positive* impact on final scoring. I also tried to implement extra preprocessing steps, with no success. These extra useless steps are obviously not shown here.
