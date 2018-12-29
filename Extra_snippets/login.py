import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_auth


external_stylesheets = ['H:\PS2\Dashboard\external_stylesheet.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
VALID_USERNAME_PASSWORD_PAIRS=[['123','123'],['qwe','qwe']]
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div(children=[

    html.H1(children=''' Welcome to SAKSHAM '''
        ),
    html.Div(children='''
        Please enter your credentials
    '''),

    #username
    html.Div(children=[
                dcc.Input(id='ip1', type='text', placeholder='Enter value1...',value =''),
                dcc.Input(id='ip2', type='text', placeholder='Enter value2...',value =''),
                html.Button(id='submit-button', n_clicks=0, children='Submit'),
                html.Div(id='output-state'),
    ])
])



@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('ip1', 'value'),
               State('ip2', 'value')])
def update_output(n_clicks, input1, input2):
        return u'''
            The Button has been pressed {} times,
            Input 1 is "{}",
            and Input 2 is "{}"
        '''.format(n_clicks, input1, input2)


if __name__ == '__main__':
    app.run_server(debug=True)
