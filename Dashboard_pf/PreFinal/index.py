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
from datetime import datetime as dt
from textwrap import dedent as d
import datetime
from dateutil.parser import parse
df=[]

##### es Data------------------------------------------------

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Yay Connect')
else:
    print('Awww it could not connect!')
now_date=datetime.datetime.now()
#### index layout-------------------------------------------------------
## Function for generating div blocks for issues lis
def query_gen(inp,*av):
    if inp=='today':
        return { "query": {
            "range" : {
                "timestamp" : {
                    "gte" :"2018-12-05T03:50:57.000Z",
                    "lt" :  "2018-12-05T04:07:59.000Z",
                    "format" : "yyyy-MM-dd'T'HH:mm:ss.SSSZ"
                }
            }
        },
        "sort":[{"timestamp":{"order":"desc"}}],"size":24,
        }
    elif inp=='sdt':
        format_str = '%Y-%m-%d' # The format
        print('av 0 : ' + str(av[0]))
        print('av 1 : ' + str(av[1]))
        datetime_obj1 = datetime.datetime.strptime(av[0], format_str)
        print("test")
        d1=datetime_obj1.date()
        datetime_obj2 = datetime.datetime.strptime(av[1], format_str)
        d2=datetime_obj2.date()
        d11=str(d1)+'T00:00:00.000Z'
        d12=str(d2)+'T23:59:59.000Z'
        print('d11  : ' + d11)
        print(d12)
        return { "query": {
            "range" : {
                "timestamp" : {
                    "gte" : d11,
                    "lte" :  d12,
                    "format" : "yyyy-MM-dd'T'HH:mm:ss.SSSZ"
                }
            }
        },
        "sort":[{"timestamp":{"order":"desc"}}],"size":24,
        }
    elif inp=='yesterday':
        return { "query": {
            "range" : {
                "timestamp" : {
                    "gte" : "now-2d/d",
                    "lt" :  "now-1d/d",
                    "format" : "yyyy-MM-dd'T'HH:mm:ss.SSSZ"
                }
            }
        },
        "sort":[{"timestamp":{"order":"desc"}}],"size":24,
        }

    return
def tab1_content():
    #### random_date + number
    def random_date_generator(start_date, range_in_days):
        days_to_add = np.arange(0, range_in_days)
        random_date = np.datetime64(start_date) + np.random.choice(days_to_add)
        return random_date
    x=list()
    for i in range(25):
        #today's date -7 days till today
        x.append(random_date_generator('2018-11-13',50))
    date_x=list(set(x))
    #print(x)
    #call elasticsearch
    date_y=np.random.randint(10, size=len(x))


    return html.Div(children=[
            #html.Br(),
            # html.Br(),
            # html.Br(),
            # html.Br(),

            html.Div(children=[
                dcc.Graph(
                id='datewise_no_of_incidents_graph',
                figure={'data':[{'x':date_x,'y':date_y}],'layout':{'title':'No. of issues raised',}},
                style={'height': 300},)
            ]),

                html.Div(style={'width':'30%','padding':'4%', 'display': 'inline-block', 'float':'left'}, children=[
                dcc.Dropdown(
                                    id='my-dropdown',
                                    options=[
                                        {'label': 'Today', 'value': 'today'},
                                        {'label': 'Yesterday', 'value': 'yesterday'},
                                        {'label': 'Select date Range', 'value': 'sdt'}
                                    ],
                                    value='today'
                                ),
                        ]),
                        # html.Div(id='output-container'),
                html.Div(style={'width':'30%', 'display': 'inline-block', 'float':'left'}, children=[
                    dcc.Markdown(d("""
                            Select Date Range
                    """)),

                            html.Div(style={"padding":"2%"},children=[
                                dcc.DatePickerRange(
                                    id='my-date-picker-range',
                                    min_date_allowed=dt(1995, 8, 5),
                                    max_date_allowed=dt(2025, 9, 19),
                                    initial_visible_month=dt(now_date.year, now_date.month, now_date.day),
                                    # end_date=dt(2018,8 , 8)
                                ),
                            html.Button("Search",id='search_button',style={"padding":"2%"}),
                            ]),
                ]),
                html.Div(id='output-container-date-picker-range',style={"display":"none"}),
                html.Div(style={'width':'25%', 'display': 'inline-block', 'float':'right'}, children=[
                        dcc.Markdown(d("""
                            Click here to resolve this issue
                        """)),
                        html.Button("Resolve this issue",id='resolve_button',style={"padding":"2%"}),
                        html.Div(id='tab2_button_extra_piece')
                        ]),


                # html.Div(style={'width':'80%','padding':'0.1%', 'display': 'inline-block','float':'left'},children=[
                html.Br(),html.Br(),html.Br(),
                html.Div(id='tab1_data_table'),
                html.Div(id='tab1_resolve_data_table')
            ])

def tab2_content():
    z=[]
    yaaa={}
    res =es.search(index="test",doc_type="1", body={"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}})

    for hit in res['hits']['hits']:
        z.append(hit['_source'])
# print(x)
    styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
        }
    }
    data_es_id=[]
    data_es_occ=[]
    data_es_name=[]
    for i in range(0,len(z)):
        yaaa.update(z[i])
        #print(z[i])
        key_list_z_i=z[i].keys()
        if 'id' in key_list_z_i:
            data_es_id.append(yaaa['id'])
        if 'occupation' in key_list_z_i:
            data_es_occ.append(yaaa['occupation'])
        if 'name' in key_list_z_i:
            data_es_name.append(yaaa['name'])
    return (
    dcc.Graph(
        id='basic-interactions',
        figure={
            'data':[
                      {
                'x': data_es_id,
                'y':data_es_name,
                'text': data_es_occ,
                'customdata': data_es_name,
                'name': 'Trace 1',
                'mode': 'markers',
                'marker': {'size': 12}
            },
                  ]
            }
    ),
    html.Div(className='row',children=[
        html.Div(children=[
            dcc.Markdown(d("""
                **Hover Data**

                Mouse over values in the graph.
            """)),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div(children=[
            dcc.Markdown(d("""
                **Click Data**

                Click on points in the graph.
            """)),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div(children=[
            dcc.Markdown(d("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.
            """)),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),

        html.Div(children=[
            dcc.Markdown(d("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """)),
            html.Pre(id='relayout-data', style=styles['pre']),
        ], className='three columns')
    ])
    )

def tab3_content():
    return pie_chart.get_tab_layout()


def tabbed_layout():
    return (html.Div([
                dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Issues', value='tab-1',children=tab1_content()),
                    #dcc.Tab(label='Template_Graph', value='tab-2', children=tab2_content()),
                    dcc.Tab(label='Reporting', value='tab-3', children=tab3_content()),
                ]),
                html.Div(id='tabs-content')
            ])
        )

#### Layout Base ---------------------------------------
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


#dtatable
@app.callback(
    Output('div-out','children'),
    [Input('datatable', 'data'),
     Input('datatable', 'selected_rows')])
def f(df_table,selected_row_indices):
    selected_rows=[df_table[i] for i in (selected_row_indices or [])]
    if selected_rows:
        app2.setasd(str(selected_rows[0]['_id']))
    return ""

#graph click callback
@app.callback(
    Output('div-out_click','children'),
    [Input('datatable_json', 'data'),
     Input('datatable_json', 'selected_rows')])
def f_(df_table_,selected_row_indices_):
    selected_rows_=[df_table_[i] for i in (selected_row_indices_ or [])]
    if selected_rows_:
        app2.setasd2(str(selected_rows_[0]['_id']))
    return ""

######### CallBacks----------------------------------------
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        # app2.setasd(['asd','sdf','qwe'])
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/':
        return tabbed_layout()



##### tab2 CallBacks------------------------------------------------
#Resolve path + data
# @app.callback(Output('url', 'pathname'),
#             [Input('div-out','children'),],
#               [State('resolve_button', 'n_clicks'),
#               # Input('resolve_button_click_data','n_clicks'),
#               # Input('div-out_click','children')
#               ])
# def resolve(n_clicks,selected_row_id):#,n_clicks_click_data,selected_row_id_click):
#     if n_clicks:#or n_clicks_click_data:
#         if n_clicks>0:
#             print('setasd : '+str(selected_row_id))
#             app2.setasd(str(selected_row_id))
#             return '/apps/app2'
#         # if n_clicks_click_data>0:
#         #     print('setasd : '+str(selected_row_id_click))
#         #     app2.setasd(str(selected_row_id_click))
#         #     return '/apps/app2'
#     return '/'



#click on graph data########################################################################
@app.callback(
    Output('click-data_bar', 'children'),
    [Input('basic-interactions_bar', 'clickData')])
def display_click_data(clickData):
    data_=json.loads(json.dumps(clickData, indent=2))
    #print(data_["points"][0]["x"])
    # print(df_source)
    #app1.set_soure_value(data_["points"][0]["x"])
    if data_:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if es.ping():
          print('Yay Connect')
        else:
          print('Awww it could not connect!')

        res_ =es.search(index="log",doc_type="windows", body={
                #"_source" :["source","level",],
            "query":{"bool":{"must":[{   "term": {
                "source": data_["points"][0]["x"]
            }}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[{"timestamp":{"order":"desc"}}],"aggs":{}})

        x_json=[]
        for hit in res_['hits']['hits']:
            z_json={}
            z_json.update(hit['_source'])
            #print(hit['_id'])
            z_json.update({'_id':hit['_id']})
            x_json.append(z_json)
        df_json = json_normalize(x_json)

        for i in range(0,10):
            if df_json.at[i,"SeverityValue"]=="4":
                vvv="high"
            elif df_json.at[i,"SeverityValue"]=="3":
                vvv="medium"
            elif df_json.at[i,"SeverityValue"]=="2":
                vvv="low"
            else:
                vvv="medium"
            df_json.set_value( i ,"SeverityValue",vvv)
            msg = df_json.at[i,'message']
            msg_split=msg.split('.')
            df_json.set_value( i ,"message",msg_split[0])
            date_time = df_json.at[i,'timestamp']
            date_time_converted = parse(date_time)
            df_json.set_value( i ,"timestamp",date_time_converted)
        cols={}
        cols=[{"name":"Timestamp","id":"timestamp"},{"name":"Source","id":"source"}]
        for i in df_json.columns:
            if i not in ["timestamp","source","_id"]:
                cols.append({"name":i,"id":i})
        # print(cols)
        # print(df.to_dict("rows"))
        return html.Div([
            html.Br(),html.Br(),
            html.Div(style={'width':'25%', 'display': 'inline-block', 'float':'right'}, children=[
                    dcc.Markdown(d("""
                        Click here to resolve this issue
                    """)),
                    html.Button("Resolve this issue",id='resolve_button_click_data'),
                    html.Div(id='tab2_button_extra_piece_click')
                    ]),
            html.Div(style={'float':'left'},children=[
                            dash_table.DataTable(
                                id='datatable_json',
                                columns=cols,
                                #[
                                    #{"name": i, "id": i, "deletable": True} for i in df.columns

                                    #{"name":"Channel","id":"Channel"},{"name":"SeverityValue","id":"SeverityValue"},
                                    #,"source","level","channel","severity value"
                                #],
                                data=df_json.to_dict("rows"),
                                #editable=True,
                                #filtering=True,
                                sorting=True,
                                #enable_drag_and_drop=True,
                                sorting_type="multi",
                                row_selectable="single",
                                row_deletable=True,
                                selected_rows=[],
                                #n_fixed_rows=1,
                                #n_fixed_columns=1,
                                style_table={
                                    'table-layout':'fixed',
                                     'maxHeight': '500',
                                    'overflowX': 'scroll',
                                     'overflowY': 'scroll',
                                },
                                style_cell_conditional=[
                                        {'if': {'column_id': '_id'},
                                         'width': '1px'},
                                    ],
                                 style_cell={
                                    # all three widths are needed
                                    'minWidth': '100px', 'width': '200px', 'maxWidth': '550px',
                                    'whiteSpace': 'nowrap','textAlign': 'left'
                                },
                                css=[{
                                    'selector': '.dash-cell div.dash-cell-value',
                                    'rule': 'display: inline; white-space: nowrap; overflow: inherit; text-overflow: inherit;'
                                }],
                            ),
                            html.Div(id='div-out_click'),

                    ])
        ])



##### date DatePickerRange

@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

##### tab1 CallBacks------------------------------------------------
@app.callback(
    Output('hover-data', 'children'),
    [Input('basic-interactions', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=3)


@app.callback(
    Output('click-data', 'children'),
    [Input('basic-interactions', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('selected-data', 'children'),
    [Input('basic-interactions', 'selectedData')])
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@app.callback(
    Output('relayout-data', 'children'),
    [Input('basic-interactions', 'relayoutData')])
def display_selected_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


@app.callback(
    dash.dependencies.Output('tab1_data_table', 'children'),
    [Input('search_button','n_clicks')],
    [dash.dependencies.State('my-dropdown', 'value'),
    dash.dependencies.State('my-date-picker-range', 'start_date'),
     dash.dependencies.State('my-date-picker-range', 'end_date')],)
def update_output(n_click,value,start_date,end_date):
    flag=False
    if value=='today' and not (end_date==now_date.date()):
        q=query_gen(value)
        res =es.search(index="log",doc_type="windows", body=q )
        flag=True
    elif value=='yesterday':
        q=query_gen(value)
        res =es.search(index="log",doc_type="windows", body=q )
        flag=True
    elif value=='sdt':
        if start_date and end_date :
            q=query_gen(value,start_date,end_date)
            print("std date q : " + str(q))
            res =es.search(index="log",doc_type="windows", body=q )
            # print('res =' +str(res))
            flag=True
        # {
            #"_source" :["source","level",],
        # "query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":24,"sort":[{"timestamp":{"order":"desc"}}],"aggs":{}})
    if flag:
        x=[]
        for hit in res['hits']['hits']:
            z={}
            z.update(hit['_source'])
            #print(hit['_id'])
            z.update({'_id':hit['_id']})
            x.append(z)
        dfff = json_normalize(x)
        r,c=(dfff.shape)
        print('dfff size = ' + str(r))
        del(x)
        for i in range(0,r):
            #print(dfff.at[i,"SeverityValue"])
            if dfff.at[i,"SeverityValue"]=="4":
                vvv="high"
            elif dfff.at[i,"SeverityValue"]=="3":
                vvv="medium"
            elif dfff.at[i,"SeverityValue"]=="2":
                vvv="low"
            else:
                vvv="medium"
            dfff.at[i ,"SeverityValue"]=vvv
            msg = dfff.at[i,'message']
            msg_split=msg.split('.')
            dfff.at[i ,"message"]=msg_split[0]
            print("msggg   :::  " + msg_split[0])
            date_time = dfff.at[i,'timestamp']
            date_time_converted = parse(date_time)
            dfff.at[i ,"timestamp"]=date_time_converted
        cols={}
        cols=[{"name":"Timestamp","id":"timestamp"},{"name":"Source","id":"source"}]
        for i in dfff.columns:
            if i not in ["timestamp","source","_id","Channel","level"]:
                cols.append({"name":i,"id":i})
            # if i in ["SeverityValue"]:
            #     print(i)
            #     if i=="2":
            #         vvv="high"
            #     elif i=="3":
            #         vvv="medium"
            #     elif i=="4":
            #         vvv="low"
            #     else:
            #         vvv="medium"
                # cols.append({"name":i,"id":i})
        cols.append({"name":'Issue Id',"id":'_id'})
        return  html.Div([
                html.Br(),html.Br(),html.Br(),
                dash_table.DataTable(
                id='datatable',
                columns=cols,
                #[
                    #{"name": i, "id": i, "deletable": True} for i in df.columns

                    #{"name":"Channel","id":"Channel"},{"name":"SeverityValue","id":"SeverityValue"},
                    #,"source","level","channel","severity value"
                #],
                data=dfff.to_dict("rows"),
                #editable=True,
                #filtering=True,
                sorting=True,
                #enable_drag_and_drop=True,
                sorting_type="multi",
                row_selectable="single",
                row_deletable=True,
                selected_rows=[],
                #n_fixed_rows=1,
                #n_fixed_columns=1,
                style_table={
                    #'table-layout':'fixed',
                     'maxHeight': '500',
                    'overflowX': 'scroll',
                     'overflowY': 'scroll',
                },
                style_cell_conditional=[
                        {'if': {'column_id': '_id'},
                         'width': '1px'},
                    ],
                 style_cell={
                    # all three widths are needed
                    'minWidth': '100px', 'width': '200px', 'maxWidth': '550px',
                    'whiteSpace': 'nowrap','textAlign': 'left'
                },
                css=[{
                    'selector': '.dash-cell div.dash-cell-value',
                    'rule': 'display: inline; white-space: nowrap; overflow: inherit; text-overflow: inherit;'
                }],
            ),
            html.Div(id='div-out'),
        ]),

#################################################
@app.callback(
    Output('tab1_resolve_data_table', 'children'),
    [Input('resolve_button', 'n_clicks')])
def tab1_res(n_clicks):
    if n_clicks>0:
        return app2.get_layout("tab1")
@app.callback(
    Output('tab2_resolve_data_table', 'children'),
    [Input('resolve_button_click_data', 'n_clicks')])
def tab2_res(n_clicks):
    if n_clicks>0:
        return app2.get_layout("tab2")



if __name__ == '__main__':
    app.run_server(debug=True,port = 8070)
