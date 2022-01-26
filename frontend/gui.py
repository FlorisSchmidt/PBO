import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import dash_core_components as dcc
import plotly.graph_objs as go

from dash import Dash, dcc, html, Input, Output, State
from backend import backend

options = [{'label': 'Header 1 text 1 image 1 ', 'value': '111'},
    {'label': 'Header 1 text 1 image 2 ', 'value': '112'},
    {'label': 'Header 1 text 1 image 3 ', 'value': '113'},
    {'label': 'Header 1 text 2 image 1 ', 'value': '121'},
    {'label': 'Header 1 text 2 image 2 ', 'value': '122'},
    {'label': 'Header 1 text 2 image 3 ', 'value': '123'},
    {'label': 'Header 1 text 3 image 1 ', 'value': '131'},
    {'label': 'Header 1 text 3 image 2 ', 'value': '132'},
    {'label': 'Header 1 text 3 image 3 ', 'value': '133'},
    {'label': 'Header 2 text 1 image 1 ', 'value': '211'},
    {'label': 'Header 2 text 1 image 2 ', 'value': '212'},
    {'label': 'Header 2 text 1 image 3 ', 'value': '213'},
    {'label': 'Header 2 text 2 image 1 ', 'value': '221'},
    {'label': 'Header 2 text 2 image 2 ', 'value': '222'},
    {'label': 'Header 2 text 2 image 3 ', 'value': '223'},
    {'label': 'Header 2 text 3 image 1 ', 'value': '231'},
    {'label': 'Header 2 text 3 image 2 ', 'value': '232'},
    {'label': 'Header 2 text 3 image 3 ', 'value': '233'},
    {'label': 'Header 3 text 1 image 1 ', 'value': '311'},
    {'label': 'Header 3 text 1 image 2 ', 'value': '312'},
    {'label': 'Header 3 text 1 image 3 ', 'value': '313'},
    {'label': 'Header 3 text 2 image 1 ', 'value': '321'},
    {'label': 'Header 3 text 2 image 2 ', 'value': '322'},
    {'label': 'Header 3 text 2 image 3 ', 'value': '323'},
    {'label': 'Header 3 text 3 image 1 ', 'value': '331'},
    {'label': 'Header 3 text 3 image 2 ', 'value': '332'},
    {'label': 'Header 3 text 3 image 3 ', 'value': '333'}]

multi_dropdown = dcc.Dropdown(options=options,
                    multi=True,
                    id='dropdown',
                    style={'width': '250px'},
                    className='m-1'
                    )

fig = go.Figure(data=[go.Scatter(x=[1, 2, 3,4,5,6,7,8,9,10], y=[1,3,4.5,5.4,7.5,8.6,9,9.4], )])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
recommendedWebsites = [1,2,3]
fig = go.Figure(data=[go.Scatter(x=[1,2,3,4,5,6,7,8,9,10], y=[1,3,4.5,5.4,7.5,8.6,9,9.4], )])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
                    dbc.Row([html.H1("Dashboard OBP", className="display-3 text-center"),],),
                    dbc.Row(
                        [
                        dbc.Col(html.Div(), width=1),
                        dbc.Col(
                            html.Div([
                                dbc.Row([
                                    dbc.Label("Configuration",className="h-50"),
                                    dbc.Col(
                                        html.Div([
                                            multi_dropdown
                                        ])
                                    ),
                                    dbc.Col(html.Div([
                                        html.Div(id='dd-output-container'),
                                        html.Br(),
                                        html.H3('Budget'),
                                        dcc.Input(
                                            id="budget",
                                            type="number",
                                            value=1000,
                                            min=1,
                                            debounce=True, 
                                            placeholder="Budget"
                                        ),
                                        html.Br(),
                                        html.H3('Accuracy'),
                                        dcc.Slider(
                                            id='accuracy',
                                            min=0.5,
                                            max=1,
                                            step=0.01,
                                            value=0.95,
                                            tooltip={"placement": "bottom", "always_visible": True}
                                        ),
                                        html.Br(),html.Br(),
                                        html.Button('Run algoritms', id='button')
                                    ]))
                                ])
                            ]
                            )),
                        dbc.Col(
                            html.Div(['Results',
                                dbc.Label('Recommendation'),
                                html.Ul(id='my-list', children=[html.Li(site) for site in []]),
                                dcc.Graph(figure=fig)],
                                ),
                            ),
                        dbc.Col(html.Div(), width=1)
                        ]
                    )
            ])
@app.callback(
    Output('my-list','children'),
    Input('button','n_clicks'), #don't care about the value
    State('dropdown', 'value'),
    State('budget', 'value'),
    State('accuracy','value'),
    prevent_initial_call=True
)
def run_algo(_,websiteList,budget,accuracy):
    if(budget==None):
        budget=10000
    if(accuracy==None):
        accuracy = 0.95
    result = backend.run_experiment(websiteList,budget,accuracy)

    if len(result)==1:
        return [html.Li(f"Found best website {result[0].name}")]
    return [html.Li(f"Website config:{site.name}") for site in result]

    
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
