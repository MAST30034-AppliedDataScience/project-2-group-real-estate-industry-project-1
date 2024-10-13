# MAST30034 project 2 group 1

**Group Members:**  
Yuecheng Wang, 1266382
Ran Zhang, 1266233
Wanyu Xu, 1167872
Zehua HU, 1159107
Yiting Wang, 1309191

### This project aiming to predict rental price for 2025-2027 in Victoria Australia using various data source.

### All files in this project are listed in time order, same number at same root means run at any order, e.g. you can run 1_xxx folders in any order, but must run 0_xxx before and 2_xxx after

### In `notebooks/`, `0_domain_data` collects property data from domain.com.au, all 1_xxx is external data collection with `2_api_distance` calculate route distance for some facilities

### forecast models located at `models/3_forecasting_model` was used to fill some data and `models/6_prediction_model` are models used in prediction the rental prices

### folder 4, 5, 7, 8 were analysis and some data processing all in `notebooks/`

### `notebooks/X_aggregate_data` contain approach that we later discarded, as well as any file start with 'X'

### For motivation and analysis, as well as detailed approach, go to `notebooks/summary _notebook.ipynb`

This project has been modified to run the pipeline with current data stored on `data/manual` for testing purposes, in order to rebuild the entire pipeline, some code that got commented for testing purposes need to be uncommented.
for now, the project run all just works on same data stored on github.
