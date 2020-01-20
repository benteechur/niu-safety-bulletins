# Criminal Trend Analysis based on NIU Safety Bulletins
Campus Safety is always an important issue for both students and faculties. Northern Illinois University Police and Public Safety has been posting notifications which include crimes and safety alerts happened in DeKalb since 2017. These data is scrapped, cleaned, and analyzed in this repository, aiming to uncover interesting facts and hidden patterns behind the data.

## Quick Links
1. [Raw data](https://www.niu.edu/publicsafety/emergency/safetybulletin/index.shtml) --> Original safety bulletin notifications on NIU website
2. [Data collection programs](https://github.com/benteechur/niu-safety-bulletins/blob/master/scrapeAndClean/BeautifulSoup/data_collection_both.py) --> Web scrapping and data cleaning program 
3. [Feature engineering programs](https://github.com/benteechur/niu-safety-bulletins/blob/master/featureEngineering/rz_feature_engineering.py) --> Attributes manipulation (you'll be asked to **type in the API key through the command line**)
4. Data visualizations

## Instructions
Running above programs, the following Python packages and Google Map API key are required:
1. Python packages:

   `bs4`, `pandas`, `googlemaps`
   
   To install above packages, you can run the following code in the command line to install a single package:
   
   `pip install *package_name*` 
   
   For example:
   
   `pip install googlemaps`
   
   To install several packages at the same time, simply pass them as a space-delimited list, for example:
   
   `pip install bs4 pandas googlemaps`
   
2. Google Map API:

   Google Map API was used in the feature engineering program to get coordinates so that crime locations can be plotted in Tableau. If 
   user wants to get the final dataset, Google Map API key is needed.
   
   To get a Google Map API key, you can follow the instruction [here](https://elfsight.com/blog/2018/06/how-to-get-google-maps-api-key-guide/). 
   
   How to use Google Map API key? --> If you run the programs appropriately, you'll be asked to **type in the API key through the command line**.
   
   The pricing of using Google Geocoding API is shown [here](https://developers.google.com/maps/documentation/geocoding/usage-and-billing). You can get $200 credit each month which means if you only use Geocoding API and send requests less than 40,000, you won't be charged. The data in this repository is not big at all, only contains less than 100 records. So you don't have to worry about getting charged if using properly.

## Data Collection

The data is originally posted on NIU website by the Department of Police and Public Safety. The original posts can be found under "[Current Safety Notifications](https://www.niu.edu/publicsafety/emergency/safetybulletin/index.shtml)" and "[Archived Safety Notifications](https://www.niu.edu/publicsafety/emergency/safetybulletin/archive.shtml)". "Current Satety Notifications" includes the most recent couple of months' records while "Archived Safety Notifications" includes older records. After a period of time, some of the "current" posts will be transformed into "archived" category.

To collect the data, we implemented two methods to do web scrapping, [BeautifulSoup](https://github.com/benteechur/niu-safety-bulletins/blob/master/scrapeAndClean/BeautifulSoup/data_collection_both.py) and [Regular Expression](https://github.com/benteechur/niu-safety-bulletins/blob/master/scrapeAndClean/regularExpressions/main.py) methods. The intention of using both methods was to compare the final results and see which method will generate better results. So far, BeautifulSoup method gets better results, so it's highly recommended to run the code under the "BeautifulSoup" folder. If you want to refer to regular expression method, here's the [link](https://github.com/benteechur/niu-safety-bulletins/tree/master/scrapeAndClean/regularExpressions).

After running "[data_collection_both.py](https://github.com/benteechur/niu-safety-bulletins/blob/master/scrapeAndClean/BeautifulSoup/data_collection_both.py)" file, two .csv files are supposed to be generated on your desktop under the "Test" folder:

* "webscrape_bulletin.csv" --> It is generated immediately after webscrapping, you can get an idea of what the raw data looks like. The "webscrape_bulletin.csv" file includes both "current" and "archived" notifications. 
* "clean_bulletin.csv" --> As you can see, in the webscrap_bulletin.csv" file, there are useless columns and useless characters in vlues. So "clean_bulletin.csv" provides a relatively cleaned dataset.

## Feature Engineering
After deleted useless columns, there are only 4 attributes which are "Incident", "Date Occurred", "Location", and "Details". It's hard to do suficient analysis based on only 4 columns. So feature engineering is conducted to manipulate current columns and create new columns based on existing ones. After feature engineering, 6 more columns are generated from existing ones, all of the attributes are shown below along with explanations:

  * `Incident`: the title of the crime. It usually includes the type of notification, the type of crime, and location
  * `Crime Type` (new): generated based on `Incident`
  * `Date Occurred`: the date when the incident happened
  * `Time_24` (new): extracted from `Details` column. It indicates the approximate time of when the incident happened. (Note: some records don't have this value usually becuase it's originally not specified in `Details`)
  * `Dayofweek` (new): generated based on `Date Occurred`
  * `Location`: spefifies the location where the incident happened. (Note: some of the records don't have this value mostly beacause of the type of notifications. For example, if the notification is about crime then it's supposed to have location, but if it's just a community awareness notification then it might not have location)
  * `Location_map` (new): generated based on `Location`. It will be used for ploting the location on maps either in Google Map or Tableau
  * `Latitude` (new): generated based on `Location_map` using Google Map API. It will be used in plotting location in Tableau
  * `Longitud` (new): generated based on `Location_map` using Google Map API. It will be used in plotting location in Tableau
  * `Details`: inlcudes more detailed information about the incidents
  
Two files are supposed to be generated, agian, under the "Test" folder on your desktop after running "[rz_feature_engineering.py](https://github.com/benteechur/niu-safety-bulletins/blob/master/featureEngineering/rz_feature_engineering.py)":
* "feature_bulletin_tableau.csv" --> this file is ready to be imported in Tableau or other data visualization tools (only tested in Tableau)
* "feature_bulletin_mymap.csv" --> this file is recommended to be used in plotting incidents in Google My Map.

## Data Visualizations
(work in progress)
