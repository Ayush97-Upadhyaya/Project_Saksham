import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
from numpy.random import randint

import json
from textwrap import dedent as d

external_stylesheets = ['H:\PS2\Dashboard\external_stylesheet.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

issues=['iss1234laiuefEFDHLISUDLKJADSBLKjabdlAJBDLJabdsljABDSLJadsblJADSBHLajdsblaJDSBHajldsbLAJDSBHLAjdsbhlaJDSBHlajdsbhlAJDSBHLajdsbhlaJDSBHLjadsblAJDSBLajdsb2','ytdrfghcjhg','76rfu76fuvi']

## Function for generating div blocks for issues list
def issues_(iss,idx):
    id_msg=str(idx)+'_message'
    id_but=str(idx)+'_button'
    print('\n'+id_msg+'\n'+id_but+'\n')
    return (html.Div(style={'width':'80%', 'display': 'inline-block', 'float':'left'},children=[
        html.P(iss),
    ]),
    html.Div(style={'width':'20%', 'display': 'inline-block', 'float':'left'},children=[
        dcc.ConfirmDialogProvider(
            children=html.Button(
                'Resolve',
            ),
            message='Danger danger! Are you sure you want to continue?',
            id=id_but,
        ),
        html.Div(id=id_msg),
    ]),)
def issues_list_func(array_issues):
    cmpnt=[]
    for i in array_issues:
        a,b=issues_(i,array_issues.index(i))
        cmpnt.append(a)
        cmpnt.append(b)
    print(cmpnt)
    print('\n')
    return html.Div(cmpnt)

def tab2_content():
    return html.Div(children=[
            html.Div(style={'width':'20%', 'display': 'inline-block', 'float':'left'},children=[
                dcc.Markdown(d("""
                    Filters
                """)),
            ]),

            html.Div(style={'width':'60%', 'display': 'inline-block'},children=[
                    dcc.Markdown(d("""
                        **Hover Data**
                    """)),

                    html.Div(style={'display': 'inline','word-wrap': 'break-word'},children=issues_list_func(issues))

                ]),
            html.Div(style={'width':'20%', 'display': 'inline-block', 'float':'right'},children=[
                dcc.Markdown(d("""
                    ycvjgvhg
                """)),
            ]),
        ])



app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1',children=html.Div([
            html.H3('Tab content 1')
        ])),
        dcc.Tab(label='Tab two', value='tab-2', children=tab2_content()),
    ]),
    html.Div(id='tabs-content')
])
app.config.supress_callback_exceptions = True

#
# @app.callback(Output('tabs-content', 'children'),
#               [Input('tabs', 'value')])
# def render_content(tab):
#     if tab == 'tab-1':
#         return html.Div([
#             html.H3('Tab content 1')
#         ])
#     elif tab == 'tab-2':
#         return html.Div([
#             html.H3('Tab content 2')
#         ])


for i in range(0,len(issues)):
    id_msg=str(i)+'_message'
    id_but=str(i)+'_button'
    @app.callback(Output( id_msg, 'children'),
                  [Input( id_but, 'submit_n_clicks')])
    def update_output(submit_n_clicks):
        if not submit_n_clicks:
            return ''
        return """
            It was dangerous but we did it!
            Submitted {} times
        """.format(submit_n_clicks)




if __name__ == '__main__':
    app.run_server(debug=True,port=8050)
