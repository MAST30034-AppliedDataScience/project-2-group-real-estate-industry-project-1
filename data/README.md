# Datasets
For this project, we gathered many dataset from internet relate to property data to predict future rental price.

### 1. Domain rental data
For the domain data dataset, we first proceeded to obtain the past dataset through the website dffh.vic.gov.au [https://www.dffh.vic.gov.au/moving-annual-rent-suburb-december-quarter-2023-excel], stored at data/raw/domain/past_data.csv. then manually grabbed the postcode corresponding to each suburb appearing in the past data, saved them as a json file in the path:. /data/raw/suburb_to_postcodes.json. After that we scraped the property information corresponding to these suburb postcodes from the website (domain.com.au) and stored it. suburb areas and store them.

Scraped dataset is stored at data/raw/domain/all_properties_combined.csv which is immediately preprocessed to remove duplicate and negotiation price ones. Which become data/raw/domain/all_properties_preprocessed.csv

### 2. External dataset from ABS (Australian Bereau of Statistics)
ABS is good source...
##### 2.1 Population

##### 2.2 Income

### 3. Other external datasets
Other feature mainly distance but crime and shit...
##### 3.1 Crime

##### 3.2 PTV