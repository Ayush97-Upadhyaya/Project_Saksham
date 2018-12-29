import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from elasticsearch import Elasticsearch
from app import app
import dash_table
# from pandas.io.json import json_normalize
import json
import dash_table
import pandas as pd
from pandas.io.json import json_normalize
from dateutil.parser import parse
from textwrap import dedent as d

df=[]
asd=[]
asd2=[]
def setasd(aasas):
    asd.append(aasas)
    #print("asd : " +asd)
def setasd2(aasa1s):
    asd2.append(aasa1s)

def get_layout(name):
    return (html.Div(id = 'main',children=[
                #html.Button("Display Data",style={'float':'left'},id=('display_id_data_button_' + name)),
                html.Br(),
                html.Br(),



                html.Div(id=('display_id_data_' + name)),

                html.Br(),
                html.Br(),
                html.Div(children=[dcc.ConfirmDialogProvider(
                    children=html.Button(
                        'Permanently resolve this issue',
                    ),
                    message='This will permanently close this issue. Are you sure you want to continue?',
                    id=('id_but_' + name),
                ),
                html.Div(id=('id_msg_' + name) ),
                ]),

                html.Div(id=('output-confirm_' + name) ),
                html.Div(id=( 'display_id_data_2_'+ name)),

            ])
)

@app.callback(Output('id_msg_tab1', 'children'),
              [Input('id_but_tab1', 'submit_n_clicks')])
def update_output(submit_n_clicks):
    if submit_n_clicks:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if es.ping():
            print('Yay Connect')
        else:
            print('Awww it could not connect!')

        es.delete(index="log",doc_type="windows",id=asd)
        print("deleted")
        try:
            res = es.get(index="log", doc_type='windows', id=asd    )
        except:
            print("cannot find log with id :",asd[-1])
        return 'Issue resolved'



@app.callback(Output('display_id_data_tab1','children'),
                [Input('resolve_button','n_clicks')])
def display_id_data_button_data(n_clicks):
    if n_clicks>0:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if es.ping():
            print('Yay Connect')
        else:
            print('Awww it could not connect!')
            print(asd[-1])
        gt_=str(int(asd[-1])-10)
        lt_=str(asd[-1])
        # print(gt_)
        # print('lt :'+lt_)
        #res =es.search(index="log",doc_type="windows", body={"_source" :["source","level"], "query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":1,"sort":[],"aggs":{}})


        return_data=[]
        for i in range(0,10):
            iddd=(int(asd[-1])-(10-i))
            if iddd>0:
                try:
                    res = es.get(index="log", doc_type='windows', id=iddd)
                except:
                    continue
                z={}
                z.update(res['_source'])
                #print(hit['_id'])
                z.update({'_id':res['_id']})
                return_data.append(z)

        #print(res['_source'])
        # print('Print return data : ' + str(return_data))
        df=[]
        df = json_normalize(return_data)
        for i in range(0,10):
            if df.iloc[i]["SeverityValue"]=="4":
                vvv="high"
            elif df.iloc[i]["SeverityValue"]=="3":
                vvv="medium"
            elif df.iloc[i]["SeverityValue"]=="2":
                vvv="low"
            else:
                vvv="medium"
            df.set_value( i ,"SeverityValue",vvv)
            msg = df.iloc[i]['message']
            msg_split=msg.split('.')
            df.set_value( i ,"message",msg_split[0])
            date_time = df.iloc[i]['timestamp']
            date_time_converted = parse(date_time)
            df.set_value( i ,"timestamp",date_time_converted)
        cols={}

        cols=[{"name":"Timestamp","id":"timestamp"},{"name":"Source","id":"source"}]
        for i in df.columns:
            if i not in ["timestamp","source","_id"]:
                cols.append({"name":i,"id":i})
        # print(cols)
        # print(df.to_dict("rows"))
        return html.Div(style={'float':'left'},children=[
                        dash_table.DataTable(
                            id='datatable_tab1',
                            columns=cols,
                            #[
                                #{"name": i, "id": i, "deletable": True} for i in df.columns

                                #{"name":"Channel","id":"Channel"},{"name":"SeverityValue","id":"SeverityValue"},
                                #,"source","level","channel","severity value"
                            #],
                            data=df.to_dict("rows"),
                            #editable=True,
                            #filtering=True,
                            sorting=True,
                            #enable_drag_and_drop=True,
                            sorting_type="multi",
                            #row_selectable="single",
                            row_deletable=True,
                            #selected_rows=[],
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
                                'whiteSpace': 'nowrap'
                            },
                            css=[{
                                'selector': '.dash-cell div.dash-cell-value',
                                'rule': 'display: inline; white-space: nowrap; overflow: inherit; text-overflow: inherit;'
                            }],
                        ),
                        html.Div(id='div-out_app2_tab1'),

                ])

@app.callback(Output('id_msg_tab2', 'children'),
              [Input('id_but_tab2', 'submit_n_clicks')])
def update_output(submit_n_clicks):
    if submit_n_clicks:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if es.ping():
            print('Yay Connect')
        else:
            print('Awww it could not connect!')

        es.delete(index="log",doc_type="windows",id=asd)
        print("deleted")
        try:
            res = es.get(index="log", doc_type='windows', id=asd    )
        except:
            print("cannot find log with id :",asd[-1])
        return 'Issue resolved'



@app.callback(Output('display_id_data_tab2','children'),
                [Input('resolve_button_click_data','n_clicks')])
def display_id_data_button_data2(n_clicks):
    if n_clicks>0:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if es.ping():
            print('Yay Connect')
        else:
            print('Awww it could not connect!')
        print("asd2 -1 : "+asd2[-1])
        gt_=str(int(asd2[-1])-10)
        lt_=str(asd2[-1])
        # print(gt_)
        # print('lt :'+lt_)
        #res =es.search(index="log",doc_type="windows", body={"_source" :["source","level"], "query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":1,"sort":[],"aggs":{}})


        return_data=[]
        for i in range(0,10):
            iddd=(int(asd2[-1])-(10-i))
            if iddd>0:
                try:
                    res = es.get(index="log", doc_type='windows', id=iddd)
                except:
                    continue
                z={}
                z.update(res['_source'])
                #print(hit['_id'])
                z.update({'_id':res['_id']})
                return_data.append(z)

        #print(res['_source'])
        # print('Print return data : ' + str(return_data))
        df=[]
        df = json_normalize(return_data)
        for i in range(0,10):
            if df.iloc[i]["SeverityValue"]=="4":
                vvv="high"
            elif df.iloc[i]["SeverityValue"]=="3":
                vvv="medium"
            elif df.iloc[i]["SeverityValue"]=="2":
                vvv="low"
            else:
                df.set_value( i ,"SeverityValue",vvv)
            msg = df.iloc[i]['message']
            msg_split=msg.split('.')
            vvv="medium"
            df.set_value( i ,"message",msg_split[0])
            date_time = df.iloc[i]['timestamp']
            date_time_converted = parse(date_time)
            df.set_value( i ,"timestamp",date_time_converted)
        cols={}

        cols=[{"name":"Timestamp","id":"timestamp"},{"name":"Source","id":"source"}]
        for i in df.columns:
            if i not in ["timestamp","source","_id"]:
                cols.append({"name":i,"id":i})
        # print(cols)
        # print(df.to_dict("rows"))
        return html.Div(style={'float':'left'},children=[
                        dash_table.DataTable(
                            id='datatable_tab2',
                            columns=cols,
                            style_as_list_view=True,
                            #[
                                #{"name": i, "id": i, "deletable": True} for i in df.columns

                                #{"name":"Channel","id":"Channel"},{"name":"SeverityValue","id":"SeverityValue"},
                                #,"source","level","channel","severity value"
                            #],
                            data=df.to_dict("rows"),
                            #editable=True,
                            #filtering=True,
                            sorting=True,
                            #enable_drag_and_drop=True,
                            sorting_type="multi",
                            #row_selectable="single",
                            row_deletable=True,
                            #selected_rows=[],
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
                                     {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                                        }
                                ],
                             style_cell={
                                # all three widths are needed
                                'minWidth': '100px', 'width': '200px', 'maxWidth': '550px',
                                'whiteSpace': 'nowrap'
                            },
                            css=[{
                                'selector': '.dash-cell div.dash-cell-value',
                                'rule': 'display: inline; white-space: nowrap; overflow: inherit; text-overflow: inherit;'
                            }],
                        ),
                        html.Div(id='div-out_app2_tab2'),

                ])



# @app.callback(Output('display_id_data_2','children'),
#                 [Input('display_id_resolve_button','n_clicks')])
# def display_id_data_button_data(n_clicks):
#     if n_clicks>0:
#         return
# #
# @app.callback(
#     Output('div-out_app2','children'),
#     [Input('datatable_', 'data'),
#      Input('datatable_', 'selected_rows')])
# def f_(df_table_,selected_row_indices_):
#     selected_rows_=[df_table_[i] for i in (selected_row_indices_ or [])]
#     print(selected_rows_)
#     return str(selected_rows_[0]['_id'])
#
#


# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/apps/app1':
#         # app2.setasd(['asd','sdf','qwe'])
#         return app1.layout
#     elif pathname == '/apps/app2':
#         return app2.layout
#     elif pathname == '/':
#         return tabbed_layout()
