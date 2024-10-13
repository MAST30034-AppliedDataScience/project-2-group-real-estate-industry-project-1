# Datasets
For this project, we gathered many dataset from internet relate to property data to predict future rental price.

### 1. Domain rental data
For the domain data dataset, we first proceeded to obtain the past dataset through the website dffh.vic.gov.au `https://www.dffh.vic.gov.au/moving-annual-rent-suburb-december-quarter-2023-excel`, stored at `data/raw/domain/past_data.csv`. then manually grabbed the postcode corresponding to each suburb appearing in the past data, saved them as a json file in the path:. `/data/raw/suburb_to_postcodes.json`. After that we scraped the property information corresponding to these suburb postcodes from the website (domain.com.au) and stored it. suburb areas and store them.

### 2. External dataset from ABS (Australian Bereau of Statistics)
`https://www.abs.gov.au/` Australian Bereau of Statistics is explored for population and income data, those data change over the years so we collected as much as we can.
##### 2.1 Shapefiles
`data/raw/ABS_LGA/` and `data/raw/ABS_SA2/` stores shapefiles we collected on ABS for 2 granularity.
##### 2.2 Population
`/data/raw/ABS_population/` stores files of Victoria population data, distributed by SA2 area, as well as output from forecasting model for future population.
##### 2.3 Income
`/data/raw/Past_income_population_proprecessed` stores files of Victoria income data, distributed by SA2 area, as well as output from forecasting model for future income.
##### 2.4 Merged
`/data/raw/merge_past_forecasting_data/` stores complete files of population , income, and crime data from 2015 to 2027, including predictions

### 3. Other external datasets
Other feature, mainly various facilities, and crime records for each LGA, collected from various websites.
##### 3.1 Crime
`https://www.crimestatistics.vic.gov.au/` We collect crime data from this site and put in `/data/raw/Crime/`.
##### 3.2 PTV
`https://www.ptv.vic.gov.au/` We collected PTV data and put in `/data/raw/PTV`.
##### 3.3 Hospital
`https://d28rz98at9flks.cloudfront.net/149331/149331_01_0.csv` We collected hospital data  and put in `/data/raw/Hospital`
##### 3.4 Coles_WWS
`https://www.seibertron.com/sightings/stores/stores.php?chain_id=35&country=AU&state=101` & `https://coles.supermarketlocationmaps.com/en/aus/victoria` We collected Coles and WWS data and put in `/data/landing/Coles_WWS`
##### 3.5 Electricity_Infrastructure
`https://services.ga.gov.au/gis/rest/services/Foundation_Electricity_Infrastructure/MapServer/1/query?outFields=*&where=1%3D1&f=geojson` & `https://services.ga.gov.au/gis/rest/services/Foundation_Electricity_Infrastructure/MapServer/0/query?outFields=*&where=1%3D1&f=geojson` We collected transmission_substations and power_stations data and put in `/data/landing/Foundation_Electricity_Infrastructure`
##### 3.6 Three external 
`https://s3.ap-southeast-2.amazonaws.com/cl-isd-prd-datashare-s3-delivery/Order_9M07T0.zip` We collected library, tourist attraction and park data and put in `/data/landing/three_external`












