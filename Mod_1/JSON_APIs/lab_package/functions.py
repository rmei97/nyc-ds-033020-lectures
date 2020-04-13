#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
from keys import client_id, api_key
import pandas as pd
import os
import seaborn as sns
import numpy as np


# In[ ]:


def yelp_call(url_params, api_key):
    url =  'https://api.yelp.com/v3/businesses/search'
    headers = {
        'Authorization': 'Bearer {}'.format(api_key),}
    response = requests.get(url, headers=headers, params=url_params)
    data = response.json()
    return data


# In[ ]:


def parse_results(results):
    parsed_results = []
    for business in results['businesses']:
        biz_list = [business['id'],
                    business['name'], 
            ', '.join(business['location']['display_address']),business['rating']]
        if 'price' in business.keys(): 
            biz_list.append(business['price'])
        else: 
            biz_list.append('n/a')
        parsed_results.append(biz_list)
    return parsed_results


# In[ ]:


def data_save(parsed_results, csv_filename):
    f = open(csv_filename)
    columns = ['Business ID','Name','Address','Rating','Price',]
    data = pd.read_csv(f, index_col = 0)
    df1 = pd.DataFrame(data,columns=columns)
    df2 = pd.DataFrame(parsed_results,columns=columns)
    df3 = pd.concat([df1,df2])
    df3.to_csv('yelp_lab.csv')
    # your code to save the current results with all of the other results. 
    # I would save the data every time you pull 50 results
    # in case something breaks in the process.


# In[ ]:


#create new file
def make_or_clear_business_csv(csv_filename):
    #clear the stuff in csv except the header
    headers = pd.DataFrame(columns = ['Business ID','Name','Address','Rating','Price'])
    if os.path.exists(csv_filename):
        #clear it
        f = open(csv_filename, 'w')
        f.truncate() #eviscerated
        headers.to_csv(csv_filename, mode='a')
    else:
        headers.to_csv(csv_filename)


# # <h>Making review frame code<h>

# In[ ]:


# write Pandas code to pull back all of the business ids 
# you will need these ids to pull back the reviews for each restaurant
def get_ids(csv_filename):
    '''
    Return the ID numbers of restaurants from given file
    '''
    file = open('yelp_lab.csv')
    columns = ['Business ID','Name','Address','Rating','Price',]
    business_data = pd.read_csv(file)
    business_df = pd.DataFrame(business_data,columns=columns)
    return business_df['Business ID'].values


# In[ ]:


def get_reviews(bus_id,api_key):
    '''
    Return dictionary of reviews
    '''
    dict_reviews = {}
    url = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(bus_id)
    headers = {
        'Authorization': 'Bearer {}'.format(api_key),
    }
    url_params = {'id' : bus_id}
    results = requests.get(url, headers = headers, params = url_params)
#     dict_reviews[bus_id] = results.json()
    response = results.json()
    return response


# In[ ]:


# Write a function to parse out the relevant information from the reviews
def review_parse(result):
    list_parsed_reviews = []
    total = result['total']
    for review in result['reviews']:
        list_parsed_reviews_temp = [
            review['text'],
            review['rating'],
            review['time_created'],
            total
        ]
        list_parsed_reviews.append(list_parsed_reviews_temp)
#         list_parsed_reviews.append(result['total'])
    return list_parsed_reviews


# In[ ]:


def save_reviews(parsed_results,csv_filename):
    '''
    parsed_resuls to dataframe, add the data
    '''
    columns = ['Review','Review Rating','Time','Total Reviews','Business ID']    
    
    parse_frame = pd.DataFrame(parsed_results,columns = columns)
    
    f = open(csv_filename)
    original = pd.read_csv(f, index_col = 0)
    original_dataframe = pd.DataFrame(original, columns = columns)
    
    updated = pd.concat([original_dataframe,parse_frame])
    
    updated.to_csv(csv_filename)


# In[ ]:


def make_or_clear_csv(csv_filename):
    #clear the stuff in csv except the header
    headers = pd.DataFrame(columns = ['Review','Review Rating','Time','Total Reviews','Business ID'])
    if os.path.exists(csv_filename):
        #clear it
        f = open(csv_filename, 'w')
        f.truncate() #eviscerated
        headers.to_csv(csv_filename, mode='a')
    else:
        headers.to_csv(csv_filename)

