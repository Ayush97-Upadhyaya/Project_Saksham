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

s_key=[]
s_count=[]
sv_key=[]
sv_count=[]
ch_key=[]
ch_count=[]
l_key=[]
l_count=[]

def get_data():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
      print('Yay Connect')
    else:
      print('Awww it could not connect!')

    res_source =es.search(index="log",doc_type="windows", body={"aggs" : {"uniq_name" : {"terms" : { "field" : "source" }}},
                    "size":"0",
                    })

    res_severity_value =es.search(index="log",doc_type="windows", body={"aggs" : {"uniq_name" : {"terms" : { "field" : "SeverityValue" }}},
                    "size":"0",
                    })
    res_channel = es.search(index="log",doc_type="windows", body={"aggs" : {"uniq_name" : {"terms" : { "field" : "Channel" }}},
                    "size":"0",
                    })
    res_level = es.search(index="log",doc_type="windows", body={"aggs" : {"uniq_name" : {"terms" : { "field" : "level" }}},
                    "size":"0",
                    })


    for result in res_source['aggregations']['uniq_name']['buckets']:
        s_count.append(result['doc_count'])
        s_key.append(result['key'])
    for result in res_severity_value['aggregations']['uniq_name']['buckets']:
        sv_count.append(result['doc_count'])
        # sv_key.append(result['key'])
        asdasd=result['key']
        if asdasd=="2":
            sv_key.append("High")
        elif asdasd=="3":
            sv_key.append("Medium")
        elif asdasd=="4":
            sv_key.append("Low")
        else:
            sv_key.append("Medium")
    for result in res_channel['aggregations']['uniq_name']['buckets']:
        ch_count.append(result['doc_count'])
        ch_key.append(result['key'])
    # print(ch_key)
    # print(ch_count)
    # print(sv_count)
    for result in res_level['aggregations']['uniq_name']['buckets']:
        l_count.append(result['doc_count'])
        l_key.append(result['key'])
    return
#
# get_data()
#
# external_stylesheets = ['H:\PS2\Dashboard\external_stylesheet.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def get_tab_layout():
    get_data()
    return (
        html.Div([
            dcc.Graph(id='basic-interactions_bar',
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=s_key,
                            y=s_count,
                            # name='Source Errors',
                            marker=go.bar.Marker(
                                color='rgb(55, 83, 109)'
                            )
                        ),],
                    layout=go.Layout(
                        title='Source Errors',
                        #showlegend=True,
                        # legend=go.layout.Legend(
                        #     x=0,
                        #     y=1.0
                        # ),
                        # margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                    )
                ),
                style={'height': 300},
            ),
            html.Div(id='click-data_bar'),
            html.Div(id='tab2_resolve_data_table'),
            html.Div(style={'width':'50%', 'display': 'inline-block', 'float':'left'},children=[
                dcc.Graph(id="asdasd",
                    figure=go.Figure({
                        "data": [
                            {
                              "values": sv_count,
                              "labels":sv_key,
                            #  "domain": {"x": [0, .48]},
                              #"name": "Severity Value",
                              "hoverinfo":"label+percent",
                              "hole": .3,
                              "type": "pie",
                              #"marker" : {"colors":color_palette_1}
                            }],
                        "layout":{
                                "title":"Severity Value"
                        }

                        },
                    )
                )
            ]),
            html.Div(style={'width':'50%', 'display': 'inline-block', 'float':'left'},children=[
                dcc.Graph(id='asd',
                    figure=go.Figure({
                        "data": [
                            {
                              "values": ch_count,
                              "labels":ch_key,
                              #"domain": {"x": [0, .48]},
                              #"name": "Different Channels",
                              "hoverinfo":"label+percent",
                              "hole": .3,
                              "type": "pie",
                              #"marker" : {"colors":color_palette_1}
                            }],
                            "layout":{
                                    "title":"Channels"
                            }

                        }
                    )
                )
            ]),


        ])
    )
