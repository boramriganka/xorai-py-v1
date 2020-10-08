#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 2 14:46:53 2020

@author: jharnadohotia
"""


import requests
import json
import sys
import pandas as pd
import flatten_json


#Constants

#Square

access_token = 'EAAAEJ08pnV67p_PVqaBw7Ydryn1BpKudrKcgTMpJaY_q-MQUipUDCrUaf9sZ1m'
loc_url = "https://connect.squareupsandbox.com/v2/locations"
sq_url = "https://connect.squareupsandbox.com/v2/orders/search"

#Clover

muid = "G6ZYXRGX6VPY1"
mid = "RCTST0000008099"
api_token = "d2dc3c50-9183-8f6f-e688-c1343e02eadd"
environment = "https://sandbox.dev.clover.com/"
endpoint1 = "v3/merchants/"+muid+"/orders?expand=lineItems&expand=payment&expand=lineItems.modifications&expand=serviceCharge&expand=customers"
cl_url = environment+endpoint1

def get_square_locs(url,access_token):
    payload = {}
    headers = {
      'Authorization': 'Bearer '+access_token
    }
    
    response = requests.request("GET", url, headers=headers, data = payload)
    
    # Transform the JSON array of locations into a Python list
    #Parse JSON content
    elements = json.loads(response.content)[u"locations"]
    #print(json.dumps(elements,indent = 1))
    locIds = []
    for i in range(0, len(elements)):
        locIds.append(str(elements[i][u"id"]))
    return locIds    
    
    #print(locIds)]

def get_square_data(url,access_token,loc):        
    payload = "{\n  \"location_ids\": [\n  \t\""+loc+"\"\n  \t]\n}"
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer EAAAEJ08pnV67p_PVqaBw7Ydryn1BpKudrKcgTMpJaY_q-MQUipUDCrUaf9sZF1m'
    }
    
    response = requests.request("POST", url, headers=headers, data = payload)
    square_elements = json.loads(response.content)
    #print(response.text.encode('utf8'))
    #print(json.dumps(elements,indent = 1))
    return square_elements

def get_clover_data(cl_url,api_token):
    url = environment + endpoint1 
    headers = {"Authorization": "Bearer " + api_token}
    
    response = requests.get(url, headers=headers)
    
    if (response.status_code != 200):
        print(str(response.text.encode('utf8'))+"Something went wrong fetching this merchant's orders")
        sys.exit()
    clover_data = json.loads(response.content)
    #print(elements)
    
    #order_c = json.dumps(paid,indent = 1)
    
    ##dumping all JSON response data to a file
    #with open(r'/Users/jharnadohotia/Desktop/SFR AI ML/clover_all_orders.json', 'w', encoding='utf-8') as f:
        #json.dump(paid, f, ensure_ascii=False, indent=4)
    
    return clover_data


locIds = get_square_locs(loc_url, access_token)
for i in locIds:
    sq_raw = get_square_data(sq_url,access_token,i)
    sq_data = flatten_json.flatten(sq_raw)
    sq_df = pd.DataFrame.from_dict(sq_data)
    sq_df.to_csv(r'/Users/jharnadohotia/Desktop/Xorai_Py_Demo/square_orders_loc__'+i+'.csv', index = False)
    

cl_raw = get_clover_data(cl_url,api_token)
cl_data = flatten_json.flatten(cl_raw)
cl_df = pd.DataFrame.from_dict(cl_data)
cl_df.to_csv(r'/Users/jharnadohotia/Desktop/Xorai_Py_Demo/clover_orders.csv', index = False)

    


    
    
    