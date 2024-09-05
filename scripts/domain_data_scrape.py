'''
This file is dedicated to scrape and download data from domain.com.au
Yuecheng Wang Aug 30, modify from ./scripts/scrape.py
'''


# built-in imports
import pandas as pd
import re
from json import dump
from tqdm import tqdm

from collections import defaultdict
import urllib.request

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os


# constants
BASE_URL = "https://www.domain.com.au"


# set up different type of properties
properties = [("flat1b", "/rent/?ptype=apartment&bedrooms=1&price=50-any&sort=default-desc&state=vic", 50), 
              ("flat2b", "/rent/?ptype=apartment&bedrooms=2&price=50-any&sort=default-desc&state=vic", 50),
              ("flat3b", "/rent/?ptype=apartment&bedrooms=3&price=50-any&sort=default-desc&state=vic", 31),
              ("house2b", "/rent/?ptype=house&bedrooms=2&price=50-any&sort=default-desc&state=vic", 35),
              ("house3b", "/rent/?ptype=house&bedrooms=3&price=50-any&sort=default-desc&state=vic", 50),
              ("house4b", "/rent/?ptype=house&bedrooms=4&price=50-any&sort=default-desc&state=vic", 50)]

# save scraped data to files
for ptype, purl, ppage in properties:
    url_links = []
    property_metadata = defaultdict(dict)
    N_PAGES = range(1, ppage + 1)
    # generate list of urls to visit
    for page in N_PAGES:
        url = BASE_URL + f"{purl}&page={page}"
        print(f"Visiting {url}")
        bs_object = BeautifulSoup(urlopen(Request(url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "html.parser")
    
        # find the unordered list (ul) elements which are the results, then
        # find all href (a) tags that are from the base_url website.
        index_links = bs_object \
            .find(
                "ul",
                {"data-testid": "results"}
            ) \
            .findAll(
                "a",
                href=re.compile(f"{BASE_URL}/*") # the `*` denotes wildcard any
            )
    
        for link in index_links:
            # if its a property address, add it to the list
            if 'address' in link['class']:
                url_links.append(link['href'])
    
    # for each url, scrape some basic metadata
    pbar = tqdm(url_links[1:])
    success_count, total_count = 0, 0
    for property_url in pbar:
        bs_object = BeautifulSoup(urlopen(Request(property_url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "html.parser")
        total_count += 1
        
        try: 
            # looks for the header class to get property name
            property_metadata[property_url]['name'] = bs_object \
                .find("h1", {"class": "css-164r41r"}) \
                .text
    
            # looks for the div containing a summary title for cost
            property_metadata[property_url]['cost_text'] = bs_object \
                .find("div", {"data-testid": "listing-details__summary-title"}) \
                .text
    
            # get rooms and parking
            rooms = bs_object \
                    .find("div", {"data-testid": "property-features"}) \
                    .findAll("span", {"data-testid": "property-features-text-container"})
    
            # rooms
            property_metadata[property_url]['rooms'] = [
                re.findall(r'\d+\s[A-Za-z]+', feature.text)[0] for feature in rooms
                if 'Bed' in feature.text or 'Bath' in feature.text
            ]
            # parking
            property_metadata[property_url]['parking'] = [
                re.findall(r'\S+\s[A-Za-z]+', feature.text)[0] for feature in rooms
                if 'Parking' in feature.text
            ]
    
            property_metadata[property_url]['desc'] = re \
                .sub(r'<br\/>', '\n', str(bs_object.find("p"))) \
                .strip('</p>')
            success_count += 1
            
        except AttributeError:
            print(f"Issue with {property_url}")
    
        pbar.set_description(f"{(success_count/total_count * 100):.0f}% successful")
    
    # output to example json in data/raw/domain
    
    output_relative_dir = '../../data/raw/domain/'
    if not os.path.exists(output_relative_dir):
        os.makedirs(output_relative_dir)

    file_path = f'../../data/raw/domain/{ptype}.json'
    with open(file_path, 'w') as f:
        dump(property_metadata, f)







