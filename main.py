import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import dash_core_components as dcc
import plotly.graph_objs as go

from dash import Dash, dcc, html, Input, Output, State

from backend import backend
from frontend.options import options

multi_dropdown = dcc.Dropdown(options=options,
                    multi=True,
                    id='dropdown',
                    style={'width': '250px'},
                    className='m-1',
                    )

accuracyInput = dcc.Slider(
                        id='accuracy',
                        min=0.5,
                        max=1,
                        step=0.01,
                        value=0.95,
                        tooltip={"placement": "bottom", "always_visible": True}
)

budgetInput = dcc.Input(
                        id="budget",
                        type="number",
                        value=1000,
                        min=1,
                        debounce=True, 
                        placeholder="Budget"
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
                    dbc.Row(
                        [html.H1("Dashboard OBP", className="display-3 text-center")]
                    ),
                    dbc.Row([
                        dbc.Col(html.Div(), width=1),
                        dbc.Col(html.Div([
                                dbc.Row([
                                    html.P("Configuration",className="h-50"),
                                    dbc.Col(html.Div([
                                            multi_dropdown
                                        ])
                                    ),
                                    dbc.Col(html.Div([
                                        html.Div(id='output'),
                                        html.Br(),
                                        html.H3('Budget'),
                                        budgetInput,
                                        html.Br(),
                                        html.H3('Accuracy'),
                                        accuracyInput,
                                        html.Br(),
                                        html.Br(),
                                        html.Button('Run algoritms', id='button')
                                    ]))
                                ])
                            ]
                            )),
                        dbc.Col(html.Div(
                                    ['Recommendation',
                                    html.Br(),
                                    html.P('Press the run button', id='label'),
                                    html.Ol(id='my-list', children=[html.Li(site) for site in []]),
                                ]),
                                ),
                        dbc.Col(html.Div(), width=1)
                        ])
                    ])

@app.callback(
    [Output('my-list','children'),
    Output('label','children')],
    Input('button','n_clicks'),
    State('dropdown', 'value'),
    State('budget', 'value'),
    State('accuracy','value'),
    State('label','children'),
    prevent_initial_call=True
)
def run_algo(_,websiteList,budget,accuracy,output):
    if(budget==None):
        budget=10000
    if(accuracy==None):
        accuracy = 0.95
    result = backend.run_experiment(websiteList,budget,accuracy)
    if len(result)==1:
        return html.Li(f"{parseName(result[0].name)}"),"Found best website"
    return [html.Li(f"{parseName(site.name)}") for site in result],"Not enough budget, best sites so far."

def parseName(siteName: str):
    return f"Header {siteName[0]} text {siteName[1]} picture {siteName[2]}"

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
