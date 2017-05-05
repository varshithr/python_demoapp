"""
Created on Sun Apr 09 10:45:56 2017

@author: varshith
"""
import pandas as pd
import json
import urllib
import os
import logging
import json2html

path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/logs'
try:
    print ('Initiating log sequence')
    logging.basicConfig(filename=path+'/'+'trade_diff.log',level=logging.DEBUG)
except IOError:
    print ('Failed to identify /logs path for the trade_diff, Check if the folder is created and permissions are available')

# ------------------------------------------------------------------------------
#json_url = "http://www.suntradingllc.com/interview_exercises/sun_trades_sample.json"
json_url = "http://www.suntradingllc.com/interview_exercises/sun_trades_insight.json"
#csv_url = "http://www.suntradingllc.com/interview_exercises/counterparty_trades_sample.csv"
csv_url = "http://www.suntradingllc.com/interview_exercises/counterparty_trades_insight.csv"
    

def read_data(json_url, csv_url):
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
    
def data_cleanse(df_json, df_csv):
    logger = logging.getLogger("data_cleanse")
    logger.info('Entered into data_cleanse method')
    df_csv.ix[df_csv.buy_sell == "Sell", 'buy_sell'] = "S"
    df_csv.ix[df_csv.buy_sell == "Buy", 'buy_sell'] = "B"
    df_json[['quantity','price']] = df_json[['quantity','price']].apply(pd.to_numeric)
    logger.info('Exited into data_cleanse method')
    return (df_json, df_csv)

def json_Sourced(c):
    logger = logging.getLogger("json_Sourced")
    logger.info('Entered into json_Sourced method')
    if c['_merge'] == 'left_only':
        logger.info('Exited into json_Sourced method')
        return int(1)
    else:
        logger.info('Exited into json_Sourced method')
        return int(0)

def csv_Sourced(c):
    logger = logging.getLogger("csv_Sourced")
    logger.info('Entered into csv_Sourced method')
    if c['_merge'] == 'right_only':
        logger.info('Exited into csv_Sourced method')
        return int(1)
    else:
        logger.info('Exited into csv_Sourced method')
        return int(0)

def find_changes(df_json, df_csv):
    logger = logging.getLogger("find_changes")
    logger.info('Entered into find_changes method')
    comp_df = pd.merge(df_csv,df_json,how='outer', indicator=True)
    comp_df = comp_df[comp_df._merge != 'both']
    comp_df.insert(1, 'Exchange', 'TONKOTSU')
    comp_df['Our Count'] = 0
    comp_df['Exchange Count'] = 0
    comp_df['Our Count'] = comp_df.apply(json_Sourced, axis = 1)
    comp_df['Exchange Count'] = comp_df.apply(csv_Sourced, axis = 1)
    del comp_df['_merge']
    columns = ["TradeDate","Exchange","Symbol","Buy/Sell","Price","Quantity","Our Count","Exchange Count"]
    comp_df.columns = columns
    comp_df = comp_df.sort_values(by = columns)
    with open('result_file.html', 'w') as fo:
        fo.write(comp_df.to_html())
    print comp_df.to_html()
    '''
    print type(comp_df)
    print comp_df['Symbol'].tolist()
    #json_result = comp_df.to_json()
    json_result = comp_df.to_json(path_or_buf=None, orient='index', date_format='epoch', double_precision=10, force_ascii=True, date_unit='ms', default_handler=None, lines=False)
    jsonfile = os.path.join(os.getcwd(), os.pardir) + '/result.json'
    try:
        with open(jsonfile, 'w') as outfile:
            json.dump(json_result, outfile)
    except IOError:
        logger.error('failed to update results to JSON file')
        raise SystemExit('failed to update results to JSON file')
    logger.info('Exited into find_changes method')
    print type(json_result)
    s = json_result
    print s
    import ast
    s2 = ast.literal_eval(s)
    print type (s2)
    print s2
    df_s2 = pd.DataFrame(data=s2)
    print df_s2
    df_s2_2 = df_s2.fillna(' ').T
    print df_s2_2
    print df_s2_2.to_html()
    try:
        #jsonfile = open()
        print jsonfile
        #jsonfile2 = str(open(jsonfile, 'r'))
        #s = jsonfile2
        print type(jsonfile)
        logger.info('json-html start')
        #infoFromJson = json.loads(s)
        infoFromJson = json.loads(jsonfile)
        print intoFromJson 
        print json2html.convert(json = infoFromJson)
        logger.info('json-html converted')
    except:
        print " Not done"
        logger.error('failed to display results JSON to html view.')
    '''



if __name__ == '__main__':
    df_json, df_csv = read_data(json_url, csv_url)
    data_cleanse(df_json, df_csv)
    find_changes(df_json, df_csv)