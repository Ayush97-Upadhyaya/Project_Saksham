import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
from apps import app1, app2, pie_chart
import numpy as np
from numpy.random import randint
import json
import dash_table
import pandas as pd
from pandas.io.json import json_normalize

from textwrap import dedent as d
df=[]

##### es Data------------------------------------------------

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Yay Connect')
else:
    print('Awww it could not connect!')

res =es.search(index="log",doc_type="windows", body={"_source" :["source","level"], "query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}})
x=[]
df=[]
for hit in res['hits']['hits']:
    x.append(hit['_source'])
print(x)
df=json_normalize(x)
del(x)
external_stylesheets = ['H:\PS2\Dashboard\external_stylesheet.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children = [
                dash_table.DataTable(
                    id='datatable',
                    columns=[
                        {"name": i, "id": i, "deletable": True} for i in df.columns
                    ],
                    data=df.to_dict("rows"),
                    #editable=True,
                    filtering=True,
                    sorting=True,
                    sorting_type="multi",
                    row_selectable="single",
                    row_deletable=True,
                    selected_rows=[],
                    n_fixed_rows=1,
                    style_table={
                         'maxHeight': '700',
                        # 'overflowX': 'scroll',
                         'overflowY': 'scroll',
                    },
                ),
            ])

if __name__ == '__main__':
    app.run_server(debug=True,port=8070)
