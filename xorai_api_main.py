#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:02:57 2020

@author: jharnadohotia
"""


from flask import Flask
from flask_restx import Resource, Api
import clover_analytics
import factura_analytics

app = Flask(__name__)
api = Api(app, version='1.0', title='Xorai API',
    description='Xorai Python Analytics API',)

ns = api.namespace('xorai_analytics', description='Operations')
ns2 = api.namespace('clover_analytics', description='Operations')

@ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@ns2.route('/productsales')
class ProductSales(Resource):
    def get(self):
        sales = clover_analytics.sales()
        return sales
@ns2.route('/productsales_var')
class ProductSalesVar(Resource):
    def get(self):
        sales_var = clover_analytics.salespervar()
        return sales_var  

@ns.route('/factura/productsales')
class FacturaSales(Resource):
    def get(self):
        sales = factura_analytics.sales()
        return sales
    
@ns.route('/factura/topcust')
class FacturaTopCust(Resource):
    def get(self):
        cust = factura_analytics.topCust()
        return cust

@ns.route('/factura/weekly')
class FacturaWeekly(Resource):
    def get(self):
        weekly = factura_analytics.weekly()
        return weekly
    
@ns.route('/factura/monthly')
class FacturaMonthly(Resource):
    def get(self):
        monthly = factura_analytics.monthly()
        return monthly
    
@ns.route('/factura/yearly')
class FacturaYearly(Resource):
    def get(self):
        yearly = factura_analytics.yearly()
        return yearly

@ns.route('/factura/monthly/<int:id>')
@api.response(404, 'Invalid Input!')
class FacturaMonth(Resource):

    def get(self, id):
        """Returns sales of input month"""
        month = id
        return factura_analytics.month_sales(month)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    