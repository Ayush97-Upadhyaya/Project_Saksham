import json
import dash_table
import pandas as pd
from pandas.io.json import json_normalize

from textwrap import dedent as d
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
  print('Yay Connect')
else:
  print('Awww it could not connect!')
#
# res =es.search(index="log",doc_type="windows", body={
#     "query": {
#         "range" : {
#             "date" : {
#                 "gte" : "2018-12-05T03:50:57.000Z",
#                 "lt" :  "2018-12-05T04:07:59.000Z",
#                 "format" : "yyyy-MM-dd'T'HHmmss.SSSZ"
#             }
#         }
#     }
#
# })
import datetime
# date_str = '29/12/2017' # The date - 29 Dec 2017
# format_str = '%d/%m/%Y' # The format
# datetime_obj1 = datetime.datetime.strptime(date_str, format_str)
# print(datetime_obj1.date())
# datetime_obj2 = datetime.datetime.strptime(date_str, format_str)
format_str = '%m/%d/%Y' # The format
datetime_obj1 = datetime.datetime.strptime('12/03/2018', format_str)
print("test")
d1=datetime_obj1.date()
datetime_obj2 = datetime.datetime.strptime('12/07/2018', format_str)
d2=datetime_obj2.date()
d11=str(d1)+'T00:00:00.000Z'
d12=str(d2)+'T23:59:59.000Z'
print('d11  : ' + d11)
print(d12)

res =es.search(index="log",doc_type="windows", body={
        #"_source" :["source","level",],
    # "query":{"bool":{"must":[{   "term": {
    #     "source": "utclmfgptwprod.abgplanet.abg.com"
    # }}],"must_not":[],"should":[]}},"from":0,"size":24,"sort":[{"timestamp":{"order":"desc"}}],"aggs":{}})

#     "query":{"bool":{"must":[{"fuzzy":{"timestamp":{"value":"2018-12-05T03:54:58.000Z","prefix_length": "17","max_expansions":"5"}}}],"must_not":[],"should":[]}},"from":0,"size":24,"sort":[{"timestamp":{"order":"desc"}}],"aggs":{}})
    "query": {
        "range" : {
            "timestamp" : {
                "gte" : d11,#"2018-12-05T03:50:57.000Z",
                                "lt" : d12, # "2018-12-05T04:07:59.000Z",
                                "format" : "yyyy-MM-dd'T'HH:mm:ss.SSSZ"
            }
        }
    },
    "sort":[{"timestamp":{"order":"desc"}}],"size":100,
    })

x=[]
for hit in res['hits']['hits']:
    z={}
    z.update(hit['_source'])
    #print(hit['_id'])
    z.update({'_id':hit['_id']})
    x.append(z)
df = json_normalize(x)
{"fuzzy":{"timestamp":{"value":"2018-12-05T03:54","max_expansions":"5"}}}
print(df)
