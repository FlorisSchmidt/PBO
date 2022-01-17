import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(
    options=[
        {'label': 'Header 1 text 1 image 1 ', 'value': '111'},
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
        {'label': 'Header 3 text 3 image 3 ', 'value': '333'}
    ],
    multi=True,
    id='dropdown',
    style={'float': 'left','width': '250px'}
    ),
    html.Div(id='dd-output-container'),
    html.Button('Run algoritms', id='button2')
])


@app.callback(
    Output('dd-output-container', 'children'),
    Input('dropdown', 'value')
)
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
