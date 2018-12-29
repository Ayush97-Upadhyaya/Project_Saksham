import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from elasticsearch import Elasticsearch
from app import app

import plotly.graph_objs as go
# from pandas.io.json import json_normalize
import json
import dash_table
import pandas as pd
from pandas.io.json import json_normalize

from textwrap import dedent as d


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
  print('Yay Connect')
else:
  print('Awww it could not connect!')

res_source =es.search(index="log",doc_type="windows", body={"aggs" : {"uniq_name" : {"terms" : { "field" : "source" }}},
                "size":"0",
                })
s_key=[]
s_count=[]
styles = {
'pre': {
    'border': 'thin lightgrey solid',
    'overflowX': 'scroll'
    }
}
for result in res_source['aggregations']['uniq_name']['buckets']:
    s_count.append(result['doc_count'])
    s_key.append(result['key'])

app.layout=html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure={'data':[{'x':s_key,'y':s_count,'text': 'asdas',}],'layout':{'title':'No. of issues raised',},'mode': 'markers',},
        style={'height': 300},),
    html.Div(children=[
        dcc.Markdown(d("""
            **Click Data**

            Click on points in the graph.
        """)),
        html.Pre(id='click-data', style=styles['pre']),
    ], className='three columns'),
    html.Div(children=[
        dcc.Markdown(d("""
            **Hover Data**

            Mouse over values in the graph.
        """)),
        html.Pre(id='hover-data', style=styles['pre'])
    ], className='three columns'),

    ])
if __name__ == '__main__':
    app.run_server(debug=True,port=8090)

@app.callback(
    Output('hover-data', 'children'),
    [Input('basic-interactions', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=3)

@app.callback(
    Output('click-data', 'children'),
    [Input('basic-interactions', 'clickData')])
def display_click_data(clickData):
    print(json.dumps(clickData, indent=2))
    return json.dumps(clickData, indent=2)
