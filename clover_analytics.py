#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:46:19 2020

@author: jharnadohotia
"""


# import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np

def readCsv():
    df = pd.read_csv(r'/Users/jharnadohotia/Desktop/Xorai_Py_Demo/order_det_all.csv')
    return df

def sales():
    df = readCsv()
    df_most_sold = pd.DataFrame(df.groupby('elements.lineItems.elements.name').sum()['elements.lineItems.elements.unitQty']).reset_index()
    df_most_sold = df_most_sold.rename(columns = {'elements.lineItems.elements.name':'ProductName' ,'elements.lineItems.elements.unitQty':'Quantity Sold'})
    # df_most_sold = df_most_sold.rename(columns = {'elements.lineItems.elements.name': 'Product Name'})

    product_sales = df_most_sold.to_json(orient = 'table')
    return product_sales


def salespervar(): 
    """**Product Sales (drilled down to Product Variation)**"""
    df = readCsv()
    df_var = df.groupby(['elements.lineItems.elements.name','elements.lineItems.elements.modifications.elements.name']).size().reset_index()
    df_var = df_var.rename(columns = {'elements.lineItems.elements.name':'Item_Name' , 'elements.lineItems.elements.modifications.elements.name' : 'Variation' , 0 :'Quantity_Sold'})
    prod_var = df_var.to_json(orient = 'table')
    return prod_var