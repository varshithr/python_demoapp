"""
Created on Sun Apr 08 10:45:56 2017

@author: Nitinkumar
"""
import pandas as pd
import json
import urllib
import os
import logging
import json2html
import csv

#path=os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/logs'

csv_filter_file_path = os.path.join(os.getcwd(),"csv_filter_file.csv")
json_filter_file_path = os.path.join(os.getcwd(),"json_filter_file.csv")
final_output_file_path = os.path.join(os.getcwd(),"final_result.csv")
'''
try:
    print ('Initiating log sequence')
    logging.basicConfig(filename=path+'/'+'trade_diff.log',level=logging.DEBUG)
except IOError:
    print ('Failed to identify /logs path for the trade_diff, Check if the folder is created and permissions are available')
'''

#json_url = "http://www.suntradingllc.com/interview_exercises/sun_trades_sample.json"
json_url = "http://www.suntradingllc.com/interview_exercises/sun_trades_insight.json"
#csv_url = "http://www.suntradingllc.com/interview_exercises/counterparty_trades_sample.csv"
csv_url = "http://www.suntradingllc.com/interview_exercises/counterparty_trades_insight.csv"

def filter_json (json_url):
    response_json_url = urllib.urlopen(json_url)
    data = json.loads(response_json_url.read())

    json_filter = csv.writer(open(json_filter_file_path,"wb+"))
    json_filter.writerow(["TradeDate","Symbol","Side","ExecutionPrice","Shares"])
    for x in range(0,len(data["data"])):
        # write required data only into csv format
        json_filter.writerow([data["data"][x]["trade_date"], data["data"][x]["symbol"],data["data"][x]["buy_sell"],data["data"][x]["price"], data["data"][x]["quantity"]])
    print "[SUCCESS]... json_filter_file created : ",json_filter_file_path

def filter_csv (csv_url):
    response_csv = urllib.urlopen(csv_url)
    reader_csv_url = csv.reader(response_csv)
    data_csv= list(reader_csv_url)

    csv_filter = csv.writer(open(csv_filter_file_path,"wb+"))
    # converting  Side column data from "Sell"--> "S" and "Buy"-->"B"
    for x in range(len(data_csv)):
        if (data_csv[x][9] == "Sell"):
            data_csv[x][9] = "S"
        elif (data_csv[x][9] == "Buy"):
            data_csv[x][9] = "B"
        # write required data only into csv format
        csv_filter.writerow([data_csv[x][3], data_csv[x][8], data_csv[x][9], data_csv[x][11], data_csv[x][10]])
    print "[SUCCESS]... csv_filter_file created : ",csv_filter_file_path

def comparator (json_filter_file_path,csv_filter_file_path,final_output_file_path):
    json_file = open(json_filter_file_path, 'rb')
    csv_file = open (csv_filter_file_path, "rb")
    final_output = csv.writer(open(final_output_file_path,"wb+"))
    csv_reader = csv.reader(csv_file)
    json_reader = csv.reader(json_file)
    # one more column added "Resource"
    final_output.writerow(["TradeDate","Symbol","Side","ExecutionPrice","Shares","Resource"])

    from collections import defaultdict

    ## creating csv dictionry which has unique key "Symbol" and multiple value (type list )
    data_dict = defaultdict(list)
    for rows in csv_reader:
        data_dict[rows[1]].append(rows[0:])
    #print data_dict

    ## creating json dictionry which has unique key "Symbol" and multiple value (type list )
    json_dict = defaultdict(list)
    for rows in json_reader:
        json_dict[rows[1]].append(rows[0:])
    #print json_dict

    from sets import Set
    diffkeys = set([k for k in data_dict if data_dict[k] != json_dict[k]])
    diffkeys.update([k for k in json_dict if data_dict[k] != json_dict[k]])
    #print diffkeys
    for k in diffkeys:
        #print k
        if (json_dict[k] == []):  #  only csv resource has record but json doesn't has
            for i in range(len(data_dict[k])):
                #print "k: ",k,"i:0","CSV: ",data_dict[k]
                c=data_dict[k][i]
                c.extend(['Our Count'])
                print c
                final_output.writerow(c)
        elif (data_dict[k] == []):  #  only json resource has record but csv doesn't has
            for i in range(len(json_dict[k])):
                #print "k: ",k,"i:0","JSON",json_dict[k]
                c=json_dict[k][i]
                c.extend(['Exchange Count'])
                print c
                final_output.writerow(c)
        else:
            ### if CSV and JSON have more than one values with same "Symbol"
            n = 'init'
            for i in range(len(data_dict[k])):
                for j in range(len(json_dict[k])):
                    #print  data_dict[k][i] ,'--->', json_dict[k][j]
                    if (data_dict[k][i] == json_dict[k][j]):
                        if (i < (len(data_dict[k]))):
                            #n.append(i)
                            n = 'equal'
                            i+=1
                        break
                if (i == (len(data_dict[k]))):
                    break
                if (n != 'equal' or n == 'init'):
                    #print "k: ",k,"i:",i,"CSV: ",data_dict[k][i]
                    c=data_dict[k][i]
                    c.extend(['Our Count'])
                    print c               
                    final_output.writerow(c)
                n = 'notequal'
            n = 'init'
            for i in range(len(json_dict[k])):
                for j in range(len(data_dict[k])):
                    #print  json_dict[k][i] ,'--->', data_dict[k][j]
                    if (json_dict[k][i] == data_dict[k][j]):
                        if (i < (len(json_dict[k]))):
                            #print "k: ",k,"i:",i,'json: ',json_dict[k][i]
                            n = 'equal'
                            i+=1
                        break
                if (i == (len(json_dict[k]))):
                    break
                if (n != 'equal' or n == 'init'):
                    #print "k: ",k,"i:",i,'json: ',json_dict[k][i]
                    c=json_dict[k][i]
                    c.extend(['Exchange Count'])
                    print c
                    final_output.writerow(c)
                n = 'notequal'
    print "[SUCCESS]... final_output.csv created : ", final_output_file_path


def html_view(final_output_file_path):
    df_csv = pd.read_csv(final_output_file_path, usecols = ["TradeDate","Symbol","Side","ExecutionPrice","Shares","Resource"])
    columns = ["TradeDate","Symbol","Side","ExecutionPrice","Shares","Resource"]
    df_csv.columns = columns
    print df_csv
    df_csv = df_csv.sort_values(by = columns)
    with open('result_file.html', 'w') as fo:
        fo.write(df_csv.to_html())
    print df_csv.to_html()

if __name__ == '__main__':
    filter_json(json_url)
    filter_csv(csv_url)
    comparator (json_filter_file_path,csv_filter_file_path,final_output_file_path)
    html_view(final_output_file_path)