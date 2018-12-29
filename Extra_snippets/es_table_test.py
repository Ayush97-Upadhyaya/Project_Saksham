import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
from numpy.random import randint

import json
from textwrap import dedent as d


#import dash_auth
external_stylesheets = ['H:\PS2\Dashboard\external_stylesheet.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(id='data-df', style={'display': 'none'}),
    html.Div(
        dcc.Input(id='event-url', value='', type='text')
    ),
    html.Br(),

    html.Div([
        dcc.Dropdown(
            id='types-menu'
        )], style={'width': '40%', 'display': 'inline-block'}
    ),
    html.Div([
        dcc.Dropdown(
        id='names-menu'
        )], style={'width': '40%', 'display': 'inline-block'}
    ),

    html.Hr(),
    html.Table(
        id='data-table')

    ]

@app.callback(
    dash.dependencies.Output('data-df', 'children'),
    [dash.dependencies.Input('event-url', 'value')]
)
def update_dataframe(url):
    df = pd.read_csv("report.csv", sep="\t", encoding="utf-8")

    return df.to_json()

@app.callback(
    dash.dependencies.Output('types-menu', 'options'),
    [dash.dependencies.Input('data-df', 'children')]
)
def update_types_menu(df):
    df = pd.read_json(df, orient='split')
    col = df['Types']

    col = col.as_matrix()

    return [{'label': i, 'value': i} for i in col]

@app.callback(
    dash.dependencies.Output('names-menu', 'options'),
    [dash.dependencies.Input('data-df', 'children')]
)
def update_names_menu(df):
    df = pd.read_json(df, orient='split')

    col = df['Names']

    col = col.drop_duplicates().as_matrix()

    return [{'label': i, 'value': i} for i in col]

@app.callback(
    dash.dependencies.Output('data-table', 'children'),
    [dash.dependencies.Input('data-df', 'children')]
)
def gen_data_table(df):

    df = pd.read_json(df, orient='split')

    return generate_table(df)
