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
