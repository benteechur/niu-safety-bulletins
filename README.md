# Criminal Trend Analysis based on NIU Safety Bulletins
Campus Safety is always an important issue for both students and faculty. Northern Illinois University Police and Public Safety have been posting notifications which include crime and safety alerts for DeKalb since 2017. This data was scraped, cleaned, and analyzed in this repository, aiming to uncover interesting facts and hidden patterns.

## Quick Links
1. [Raw data](https://www.niu.edu/publicsafety/emergency/safetybulletin/index.shtml) --> Original safety bulletin notifications on NIU's website
2. [Data collection programs](https://github.com/benteechur/niu-safety-bulletins/blob/master/scrapeAndClean/BeautifulSoup/data_collection_both.py) --> Web scraping and data cleaning program 
3. [Feature engineering programs](https://github.com/benteechur/niu-safety-bulletins/blob/master/featureEngineering/rz_feature_engineering.py) --> Attributes manipulation (you'll be asked to **type in the API key through the command line**)
4. Data visualizations

## Instructions
To run the above programs, the following Python packages and a Google Maps API key are required:
1. Python packages:

   `bs4`, `pandas`, `googlemaps`
   
   To install the above packages, you can run the following code in the command line to install a single package:
   
   `pip install *package_name*` 
   
   For example:
   
   `pip install googlemaps`
   
   To install several packages at the same time, simply pass them as a space-delimited list, for example:
   
   `pip install bs4 pandas googlemaps`
   
2. Google Maps API:

   Google Maps API was used in the feature engineering program to get coordinates for street addresses so that crime locations could be plotted in Tableau. If the
   user wants to get the final dataset, a Google Maps API key is needed.
   
   To get a Google Maps API key, you can follow the instruction [here](https://elfsight.com/blog/2018/06/how-to-get-google-maps-api-key-guide/). 
   
   How to use Google Maps API key? --> If you run the programs appropriately, you'll be asked to **type in the API key through the command line**.
   
   The pricing for Google Geocoding API is shown [here](https://developers.google.com/maps/documentation/geocoding/usage-and-billing). You can get a $200 credit for free each month. This means if you send requests less than 40,000 per month to the Geocoding API, you won't be charged. The data in this repository rather small, containing only about 100 records, so you don't have to worry about getting charged if you use the programs properly.

## Data Collection

The data is originally posted on NIU website by the Department of Police and Public Safety. The original posts can be found under "[Current Safety Notifications](https://www.niu.edu/publicsafety/emergency/safetybulletin/index.shtml)" and "[Archived Safety Notifications](https://www.niu.edu/publicsafety/emergency/safetybulletin/archive.shtml)". "Current Satety Notifications" includes the most recent couple of months' records while "Archived Safety Notifications" includes older records. After a period of time, the "current" posts will be transferred into the "archived" category.

To collect the data, we implemented two methods to do web scraping, [BeautifulSoup](https://github.com/benteechur/niu-safety-bulletins/blob/master/scrapeAndClean/BeautifulSoup/data_collection_both.py) and [Regular Expressions](https://github.com/benteechur/niu-safety-bulletins/blob/master/scrapeAndClean/regularExpressions/main.py). The intention of using both methods was to compare the final results and see which method would generate better results. So far, the BeautifulSoup method achieves better results, so it's highly recommended to run the code under the "BeautifulSoup" folder. If you want to refer to regular expression method, here's the [link](https://github.com/benteechur/niu-safety-bulletins/tree/master/scrapeAndClean/regularExpressions).

Assuming you are running Windows 10, after running "[data_collection_both.py](https://github.com/benteechur/niu-safety-bulletins/blob/master/scrapeAndClean/BeautifulSoup/data_collection_both.py)" file, two .csv files will be generated on your desktop under the "Test" folder:

* "webscrape_bulletin.csv" --> This is generated immediately after webscraping. You can get an idea of what the raw data looks like by inspecting this file. The "webscrape_bulletin.csv" file includes both "current" and "archived" notifications. 
* "clean_bulletin.csv" --> As you can see, in the webscrap_bulletin.csv" file, there are many useless columns and characters in values. So "clean_bulletin.csv" provides a relatively cleaned dataset.

## Feature Engineering
After deleting the extra columns, there are only 4 attributes which are "Incident", "Date Occurred", "Location", and "Details". It's hard to do suficient analysis based on only 4 columns, so feature engineering was conducted to manipulate current columns and create new columns based on existing ones. After feature engineering, 6 more columns are generated from existing ones. All of the attributes are shown below along with explanations:

  * `Incident`: the title of the crime. It usually includes the type of notification, the type of crime, and location
  * `Crime Type` (new): generated based on `Incident`
  * `Date Occurred`: the date when the incident happened
  * `Time_24` (new): extracted from the `Details` column. It indicates the approximate time of the incident. (Note: some records don't have this value because it was originally unspecified in `Details`)
  * `Dayofweek` (new): generated based on `Date Occurred`
  * `Location`: specifies the location where the incident happened. (Note: some of the records don't have this value because of the type of notification. For example, if the notification is about crime then it's supposed to have location, but if it's just a community awareness notification then it might not have location)
  * `Location_map` (new): generated based on `Location`. This was used for importing data into Google My Maps
  * `Latitude` (new): generated based on `Location_map` using the Google Maps API. It will be used in plotting location in Tableau
  * `Longitude` (new): generated based on `Location_map` using the Google Maps API. It will be used in plotting location in Tableau
  * `Details`: includes more detailed information about the incidents
  
Two additional files will be generated under the "Test" folder on your desktop after running "[rz_feature_engineering.py](https://github.com/benteechur/niu-safety-bulletins/blob/master/featureEngineering/rz_feature_engineering.py)":
* "feature_bulletin_tableau.csv" --> this file is ready to be imported into Tableau or another data visualization tools (only tested in Tableau)
* "feature_bulletin_mymap.csv" --> this file was used for plotting incidents on Google Maps

## Data Visualizations
(work in progress)

[This map](https://drive.google.com/open?id=1FiawtAnmyKVsgoig--g0h_7iPoOZ575L&usp=sharing) was created using "feature_bulletin_mymap.csv"
