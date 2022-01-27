import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import numpy as np
import plotly.graph_objects as go

from backend import backend
from frontend.options import options

emptyGraph = go.Figure()

draft_template = go.layout.Template()
draft_template.layout.annotations = [
    dict(
        name="draft watermark",
        text="RUN ALGORITHM",
        textangle=0,
        opacity=0.1,
        font=dict(color="black", size=50),
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
    )
]

emptyGraph.update_layout(
    template=draft_template,
    yaxis_range=[0,10],
    xaxis_range=[0,10]
    )



multi_dropdown = dcc.Dropdown(options=options,
                    multi=True,
                    id='dropdown',
                    className='m-1',
                    )

accuracyInput = dcc.Slider(
                        id='accuracy',
                        min=0.5,
                        max=0.99,
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
websiteAlert = dbc.Alert("Enter at least 2 websites to compare", 
                            color="danger", 
                            id='websiteAlert', 
                            is_open=False,
                            duration=4000
                        )

graph = dcc.Graph(figure=emptyGraph, id='graph')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
                    dbc.Row(
                        [html.H1("A/B Testing", className="display-3 text-center"),
                        html.H3("Using Succesive elimination for best arm identification",className="mb-3 text-center")]
                    ),
                    dbc.Row([
                        dbc.Col(html.Div(), width=1),
                        dbc.Col(html.Div([
                                dbc.Row([
                                    dbc.Col(html.Div([
                                            html.H2("Websites",className="mb-3"),
                                            websiteAlert,
                                            multi_dropdown
                                        ],className="shadow p-3 mb-5 bg-white rounded",style={'height': '80vh'})
                                    ),
                                    dbc.Col(html.Div([
                                        html.H2("Parameters",className="mb-3"),
                                        html.H4('Budget'),
                                        budgetInput,
                                        html.Br(),
                                        html.Br(),
                                        html.H4('Accuracy'),
                                        accuracyInput,
                                        html.Br(),
                                        html.Br(),
                                        html.Button('Run algoritms', id='button', className="btn btn-primary text-center")
                                    ],className="shadow p-3 mb-5 bg-white rounded",style={'height': '80vh'}))
                                ])
                            ]
                            )),
                        dbc.Col(html.Div(
                                    [
                                    html.H2('Recommendation',className="mb-3"),
                                    html.Br(),
                                    html.P('Press the run button', id='label'),
                                    html.Ol(id='my-list', children=[html.Li(site) for site in []]),
                                    graph
                                ],className="shadow p-3 mb-5 bg-white rounded",style={'height': '80vh'}),
                                ),
                        dbc.Col(html.Div(), width=1)
                        ])
                    ])

@app.callback(
    [Output('my-list','children'),
    Output('label','children'),
    Output('websiteAlert','is_open'),
    Output('graph', 'figure')],
    Input('button','n_clicks'),
    State('dropdown', 'value'),
    State('budget', 'value'),
    State('accuracy','value'),
    prevent_initial_call=True
)
def run_algo(_,websiteList,budget,accuracy):

    if((websiteList==None) or (len(websiteList)<2)):
        return [],'No enough websites',True,emptyGraph

    if(budget==None):
        budget=10000
    if(accuracy==None):
        accuracy = 0.95
    bestWebsites, allWebsites = backend.run_experiment(websiteList,budget,accuracy)

    if len(bestWebsites)==1:
        meanGraph = getMeanGraph(allWebsites)
        return html.Li(f"{parseName(bestWebsites[0].name)}, Average click rate: {round(bestWebsites[0].average*100,2)}%"),"Found best website", False, meanGraph
    bestWebsites.sort(key=lambda x: x.average, reverse=True)
    meanGraph = getMeanGraph(allWebsites)
    return [html.Li(f"{parseName(site.name)}, Average click rate:{round(site.average*100,2)}%") for site in bestWebsites],"Not enough budget, best sites so far.", False, meanGraph

def parseName(siteName: str):
    return f"Header {siteName[0]} text {siteName[1]} picture {siteName[2]}"


def getMeanGraph(websites):
    fig = go.Figure()
    fig.update_layout(
    title="Number of clicks for all website",
    xaxis_title="Number of visits",
    yaxis_title="Number of clicks",)
    for site in websites.values():
        actualRealisations = site.realisations[0:site.num-1]
        cumulativeRealisations = np.cumsum(actualRealisations)
        trace = {
            "x": np.arange(1,site.num),
            "y": cumulativeRealisations,
            "line": {"shape": 'hv'},
            "mode": 'lines',
            "name": parseName(site.name),
            "type": 'scatter',
            }
        fig.add_trace(trace)
    return fig

    

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
