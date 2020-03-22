# -*- coding: utf-8 -*-
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from utils import read_data, get_data, get_regions
from charts import get_confirmed_trend


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

covidtrends_flask = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=covidtrends_flask,
    external_stylesheets=external_stylesheets)

raw = read_data()
regions = get_regions(raw)

#state='Washington'
#country='US'
#fig = px.line(df, x='Date', y='Value')

# all_options = {
#     'America': ['New York City', 'San Francisco', 'Cincinnati'],
#     'Canada': [u'Montréal', 'Toronto', 'Ottawa']
# }

dropdown_layout = html.Div([

    html.Div([
        html.B('Country'),
        dcc.Dropdown(
            id='countries-dd',
            options=[{'label': k, 'value': k} for k in regions.keys()],
            value='US'
        )
    ],
    style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        html.B('State/County'),
        dcc.Dropdown(id='states-dd'),
    ],
    style={'width': '49%', 'display': 'inline-block'})

    # html.Div(id='display-selected-values')
    ])

app.layout = html.Div(children=[
    html.H1(children='Covid-19 Trends'),

    dropdown_layout,

    dcc.Graph(id='confirmed-trend')
])

@app.callback(
    Output('states-dd', 'options'),
    [Input('countries-dd', 'value')])
def set_state_options(selected_country):
    return [{'label': i, 'value': i} for i in regions[selected_country]]

@app.callback(
    Output('states-dd', 'value'),
    [Input('states-dd', 'options')])
def set_state_value(available_options):
    return available_options[0]['value']

# @app.callback(
#     Output('display-selected-values', 'children'),
#     [Input('countries-dd', 'value'),
#      Input('states-dd', 'value')])
# def set_display_children(selected_country, selected_state):
#     return u'{} is a state/county in {}'.format(
#         selected_state, selected_country,
#     )

@app.callback(
    Output('confirmed-trend', 'figure'),
    [Input('countries-dd', 'value'),
     Input('states-dd', 'value')])
def update_confirmed_visual(selected_country, selected_state):
    df = get_data(
        state=selected_state,
        country=selected_country,
        data=raw,
        include_feb=False)

    #fig = px.line(df, x='Date', y='Value', )

    return get_confirmed_trend(df)


if __name__ == '__main__':
    app.run_server(debug=True)