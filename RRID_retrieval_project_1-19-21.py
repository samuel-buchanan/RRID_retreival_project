#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 09:19:18 2021

@author: sam
"""

import time
import requests
import pandas as pd
import unicodedata

input_df = pd.read_csv('Antibody Sample Kits.csv')
input_list = input_df.Name + ' ' + input_df['Catalog #']
output_list = []

# starting loop here
for i in range(len(input_list)):
        
    search_string = input_list[i]
    if pd.isna(search_string) == True:
        output_list.append(search_string)
        continue
    
    # sanitize search_string from the stray alpha and beta in the text
    search_string = unicodedata.normalize('NFKD', search_string).encode('ascii', 'ignore').decode()
    # may also need to add something here to get this working with forward slashes in the search string
    
    params = (('api_key', 'put in your API key here'), )
    # have to use double braces to except them in the string when using .format
    data = '\n{{\n  "size": 20,\n  "from": 0,\n  "query": {{\n    "bool": {{\n      "must": [\n        {{\n          "query_string": {{\n            "fields": [\n              "*"\n            ],\n            "query": "{}",\n            "type": "cross_fields",\n            "default_operator": "and",\n            "lenient": "true"\n          }}\n        }}\n      ],\n      "should": [\n        {{\n          "match": {{\n            "item.name": {{\n              "query": "{}",\n              "boost": 20\n            }}\n          }}\n        }}\n      ]\n    }}\n  }}\n}}'.format(search_string, search_string)
    
    response = requests.post('https://scicrunch.org/api/1/elastic/RIN_Antibody_pr/_search', params=params, data=data)
    
    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # response = requests.post('https://scicrunch.org/api/1/elastic/RIN_Antibody_pr/_search?api_key=4yCxin9XE8AKGGDXofub4jL3PKGS2JXT', data=data)
    
    # print(response.json()) gives properly formatted json
    # print(response.text) gives raw text, which we might want for parsing later
    
    # getting RRID number from output 
    # response.json() returns a dict, which we can parse through via [] statements
    ql = response.json()
    try:
        print(ql['error']['root_cause'][0]['type'])
    except:
        if ql['hits']['total'] == 0:
            output = 'RRID not found'
            # just in case nothing is found for the search string
        else:
            output_preformat = ql['hits']['hits'][0]['_source']['rrid']['curie']
            # hopefully they all fit this pattern, or my program gets more complex
            # they seem to, at least the top hit
            output = output_preformat[5:]
            # this assumes that the first 5 characters were 'RRID:'        
    else:
        output = 'Exception when searching'
            
    output_list.append(output)
    time.sleep(2)
    # don't want to hammer the website, sleeping for 2 sec here



# export output list to csv
output_df = input_df[["Name", "Catalog #"]].copy()
output_df['RRID'] = output_list

output_df.to_csv('Antibody Sample Kitsfinal.csv')
