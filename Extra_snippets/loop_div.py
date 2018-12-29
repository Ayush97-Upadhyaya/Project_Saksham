
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

title = 'TItle'
def gridRow(r, c):
    card = []
    for c in range(1, c + 1):
        card.append(makeCard(r,c))
    return html.Div(card, className = 'row', id = str(r))

def makeCard(r, c):
    return html.Div(style={'width':'30%', 'display': 'inline-block', 'float':'left'},children=[
        html.Div([
            html.Div([
                html.Div(title + str(c), className = 'boxHeader'),
                html.Div('LTD Unique Users', className = 'boxLabel'),
                html.Div('916k', className = 'boxNumbers')
            ], className = 'boxText')
        ], className = 'innerBox' )
    ], className = 'cardBox', id= '_'.join(['row', str(r), str(c)]))

gridLayout = []
for r in range(1, 20):
    gridLayout.append(gridRow(r, 3))

app.layout = html.Div(gridLayout)

if __name__ == '__main__':
    app.run_server(debug=True,port=8070)
