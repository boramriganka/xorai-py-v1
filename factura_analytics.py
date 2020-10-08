#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 00:43:49 2020

@author: jharnadohotia
"""


# import requests
# import json, csv
# from random import randint
# import sys
# from time import sleep
import pandas as pd
# import matplotlib.pyplot as plt
# from itertools import chain, starmap

def readData():
    df = pd.read_csv(r'/Users/jharnadohotia/Desktop/SFR AI ML/factura_sample_2019_20.csv')
    # Datetime formatting
    c=pd.to_datetime((df['issuedAt']))
    df['createdDate']=c.dt.date
    df['year']=c.dt.year
    df['month']=c.dt.month
    #column for name of day of week
    df['weekday'] =c.dt.day_name
    #column for Week Number
    df['week_no'] = c.dt.week
    
    return df

def sales():
    df = readData()
    df_most_sold = pd.DataFrame(df.groupby('items.description').sum()['items.quantity']).reset_index()
    df_most_sold = df_most_sold.rename(columns = {'items.description':'ProductName','items.quantity':'Quantity Sold'})

    product_sales = df_most_sold.to_json(orient = 'table')
    return product_sales

def topCust():
    df = readData()
    df_var = df.groupby(['receiver.name']).size().reset_index()
    df_var = df_var.nlargest(5, [0])
    df_var = df_var.rename(columns = {'receiver.name':'Customer', 0 :'Purchased Items'})
    df_var.set_index(['Customer'], inplace = True)
    topcust = df_var.to_json(orient = 'table')
    return topcust

def weekly():
    df = readData()
    df_weekly = pd.DataFrame(df.groupby(['week_no','year']).sum()['amount'])
    weekly = df_weekly.to_json(orient = 'table')
    return weekly

def monthly():
    df = readData()
    df_monthly = pd.DataFrame(df.groupby(['month','year']).sum()['amount'])
    monthly = df_monthly.to_json(orient = 'table')
    return monthly

def month_sales(month_var):
    df = readData()
    df_monthly = pd.DataFrame(df.groupby(['month','year']).sum()['amount']).reset_index()
    df_reqmonth = df_monthly.loc[(df_monthly['year'] == 2020) & (df_monthly['month'] == month_var)]
    monthly = df_reqmonth.to_json(orient = 'table')
    return monthly

def yearly():
    df = readData()
    df_yearly = pd.DataFrame(df.groupby(['year']).sum()['amount'])
    yearly = df_yearly.to_json(orient = 'table')
    return yearly
    
    
    
    
    
    
    
    
    
    
    