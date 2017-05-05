#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 9 12:48:00 2017

@author: Nitin
"""
import pandas as pd
import json
import urllib
import os
import logging
import sqlite3

dbpath=os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/db/tradediff.db'
conn = sqlite3.connect(dbpath)

path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/logs'
try:
    print ('Initiating log sequence')
    logging.basicConfig(filename=path+'/'+'trade_diff.log',level=logging.DEBUG)
except IOError:
    print ('Failed to identify /logs path for the trade_diff, Check if the folder is created and permissions are available')

# ------------------------------------------------------------------------------
json_url = "http://www.suntradingllc.com/interview_exercises/sun_trades_sample.json"
#json_url = "http://www.suntradingllc.com/interview_exercises/sun_trades_insight.json"
csv_url = "http://www.suntradingllc.com/interview_exercises/counterparty_trades_sample.csv"
#csv_url = "http://www.suntradingllc.com/interview_exercises/counterparty_trades_insight.csv"
    
class TradeDiff:
    
    def __init__(self, json_url, csv_url):
      self.json_url = json_url
      self.csv_url = csv_url
    
    def read_data(self,json_url, csv_url):
        logger = logging.getLogger("read_data")
        logger.info('Entered into read_data method')
        try:
            logger.info('trying to estabish connection with json url')        
            response_json_url = urllib.urlopen(json_url)
        except:
            logger.error('Connection with the JSON source failed')
        data = json.loads(response_json_url.read())
        columns = ["trade_date","symbol","buy_sell","quantity","price"]
        df_json = pd.DataFrame(data['data'], columns = columns)
        try:
            logger.info('trying to estabish connection with json url')        
            df_csv = pd.read_csv(csv_url, usecols = ["TradeDate","Symbol","Side",
                                                     "ExecutionPrice","Shares"])
        except:
            logger.error('Connection with the JSON source failed')
        df_csv.columns = columns
        logger.info('Exited into read_data method')
        return (df_json, df_csv)
        
    def data_cleanse(self,df_json, df_csv):
        logger = logging.getLogger("data_cleanse")
        logger.info('Entered into data_cleanse method')
        df_csv.ix[df_csv.buy_sell == "Sell", 'buy_sell'] = "S"
        df_csv.ix[df_csv.buy_sell == "Buy", 'buy_sell'] = "B"
        df_json[['quantity','price']] = df_json[['quantity','price']].apply(pd.to_numeric)
        logger.info('Exited into data_cleanse method')
        return (df_json, df_csv)
    
    def json_Sourced(self,c):
        logger = logging.getLogger("json_Sourced")
        logger.info('Entered into json_Sourced method')
        if c['_merge'] == 'left_only':
            logger.info('Exited into json_Sourced method')
            return int(1)
        else:
            logger.info('Exited into json_Sourced method')
            return int(0)
    
    def csv_Sourced(self,c):
        logger = logging.getLogger("csv_Sourced")
        logger.info('Entered into csv_Sourced method')
        if c['_merge'] == 'right_only':
            logger.info('Exited into csv_Sourced method')
            return int(1)
        else:
            logger.info('Exited into csv_Sourced method')
            return int(0)
    
    def find_changes(self,df_json, df_csv):
        logger = logging.getLogger("find_changes")
        logger.info('Entered into find_changes method')
        comp_df = pd.merge(df_csv,df_json,how='outer', indicator=True)
        comp_df = comp_df[comp_df._merge != 'both']
        comp_df.insert(1, 'Exchange', 'TONKOTSU')
        comp_df['Our Count'] = 0
        comp_df['Exchange Count'] = 0
        comp_df['Our Count'] = comp_df.apply(self.json_Sourced, axis = 1)
        comp_df['Exchange Count'] = comp_df.apply(self.csv_Sourced, axis = 1)
        del comp_df['_merge']
        columns = ["TradeDate","Exchange","Symbol","Buy/Sell","Price","Quantity","Our Count","Exchange Count"]
        comp_df.columns = columns
        comp_df = comp_df.sort_values(by = columns)
        comp_df.to_sql('tradediff',con = conn, index = False, if_exists='append')
        df = pd.read_sql_query('SELECT * FROM tradediff',conn)
        print df
        htmlfile = os.path.join(os.getcwd(), os.pardir) + '/result.html'
        try:
            with open(htmlfile, 'w') as fo:
                fo.write(comp_df.to_html())
        except IOError:
            logger.error('failed to update results to html file')
            raise SystemExit('failed to update results to html file')
        logger.info('Exited into find_changes method')
        
    def trade_diff(self):
        t = TradeDiff(self.json_url, self.csv_url)
        df_json, df_csv = t.read_data(self.json_url, self.csv_url)
        t.data_cleanse(df_json, df_csv)
        t.find_changes(df_json, df_csv)

if __name__ == '__main__':
    
    #Run this for the first time
    #createdb()
    TradeDiff(json_url, csv_url).trade_diff()