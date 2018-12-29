import dash
import dash_table
import pandas as pd
from pandas.io.json import json_normalize
from elasticsearch import Elasticsearch

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
res =es.search(index="test",doc_type="1", body={"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}})

x=[]
for hit in res['hits']['hits']:
    x.append(hit['_source'])
df = json_normalize(x)
app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True} for i in df.columns
        ],
        data=df.to_dict("rows"),
        editable=True,
        filtering=True,
        sorting=True,
        sorting_type="multi",
        row_selectable="multi",
        row_deletable=True,
        selected_rows=[],
    ),
    html.Div(id='datatable-interactivity-container')
])

@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_graph(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    if rows is None:
        dff = df
    else:
        dff = pd.DataFrame(rows)
    return

if __name__ == '__main__':
    app.run_server(debug=True)

#style_as_list_view=True,

    # style_cell_conditional=[
    #     {
    #         'if': {'row_index': 'odd'},
    #         'backgroundColor': 'rgb(248, 248, 248)'
    #     }
    # ] + [
    #     {
    #         'if': {'column_id': c},
    #         'textAlign': 'left'
    #     } for c in ['Date', 'Region']
    # ],
    #   style_header={
    #     'backgroundColor': 'white',
    #     'fontWeight': 'bold'
    # }
