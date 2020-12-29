#-*- coding:utf-8 -*-
import os
import csv
import json
import time
import pandas
from datetime import datetime, timedelta
from toolkits.databases.esClient import EsClient
from toolkits.system.excelHelper import write_cvs
from toolkits.system.timeHelper import get_time_range_interval
# import matplotlib.pyplot as plt
import numpy
import MySQLdb
import sys
path_cur = os.path.dirname(os.path.realpath(__file__))
path_parent = "%s/../" % path_cur
sys.path.append(path_parent)
from mysql_helper import mysql_db

es_url = '***********'

def ts2date(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

def load_time_range(start_date, end_date, time_field='timer'):
    if not end_date:
        end_date = datetime.now() + timedelta(days=0, hours=8)
    if not start_date:
        start_date = end_date - timedelta(days=7, hours=0)
        start_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
    if not isinstance(end_date, str): 
        end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')
    
    time_range = {
      'range': {
        time_field: {
          'gte': start_date,
          'lte': end_date,
          'format': 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss'
        }
      }
    }
    return time_range, start_date, end_date


def read_file(filepath):
    data = []
    title = []
    with open(filepath, 'r') as f:
        for row in csv.reader(f.read().splitlines()):
            if not title:
                title = row
            else:
                if not int(row[4]) == 0: 
                    data.append(row)
    return title, data

def write_file(columns, rows, filename, writemode="wb"):
    with open(filename, writemode) as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(rows)

def save_data2mysql(columns, rows):
    db = mysql_db()
    db.insert(table_name='risk_user', data_headers=columns, data=rows)

# def show_fig(rows=None, filepath=None):
#     if rows:
#         data = numpy.array(rows)
#         name_list = list(data[:,0])
#         num_list = list(data[:,1])
#     else:
#         data = pandas.read_csv(filepath)
#         name_list = list(data['username'])
#         num_list = list(data['count'])
#     num_list = [int(i) for i in num_list]
#     num_list.reverse()
#     name_list.reverse()
#     plt.barh(range(len(num_list)), num_list,tick_label = name_list)
#     plt.show()

def system_mapping(system):
    di = {
        'bamai':'mis_bamai*',
        'mis': 'mis_new_pure_mis*',
        'mis_beatles': 'mis_beatles*',
        'wave': 'mis_wave*'
    }
    try:
        return di[system]
    except:
        return '' 


def load_topN(es_index, url, top_n=10, start_date=None, end_date=None):
    time_range, start_date, end_date = load_time_range(start_date, end_date)
    query_body = {
        "query": {
            "bool": {
                "must": [
                    time_range,
                    {
                        "term":{
                            "url.keyword":{
                                "value": url,
                                }
                            }                        
                    },
                ]
            }
        },
        "size": 0,
        "aggs": {
            "top_risk_user": {
                "terms": {
                    "field": "username.keyword",
                    'size': top_n,
                    'shard_size': 2*top_n,
                    },
                }
            }
    }
    es = EsClient(es_url)
    search_res = es.es_search(es_index, query_body)
    agg_res = search_res['aggregations']['top_risk_user']['buckets']
    return agg_res, start_date, end_date
    

def main():
    filepath = 'url-0703.csv'
    title, data = read_file(filepath)
    #system    id    备注    url    风险等级    备注
    columns = ['url', 'username', 'count', 'starttime', 'endtime']
    for d in data:
        url = d[3]
        system = d[0]
        agg_res, start_date, end_date = load_topN(system_mapping(system), "http://" + url)
        url_ = '_'.join(url.split('/'))
        rows = [[url_, item['key'], item['doc_count'], start_date, end_date] for item in agg_res]
        save_data2mysql(columns, rows)
        # rows = [[item['key'], item['doc_count']] for item in agg_res]
        # write_file(columns, rows, "%s/%s.csv" % ('results', url_))
        # show_fig(rows)

if __name__ == '__main__':   
    main()


