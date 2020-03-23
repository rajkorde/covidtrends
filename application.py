# -*- coding: utf-8 -*-
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# import plotly.express as px

from utils import read_data, get_data, get_regions
from charts import get_confirmed_trend, get_recovered_trend, get_death_trend
from update import update_data
from constants import DATA_SOURCE, CODE_SOURCE


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

covidtrends_flask = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=covidtrends_flask,
    external_stylesheets=external_stylesheets)

# Data processing
update_data()
confirmed_df, recovered_df, death_df = read_data()
regions = get_regions(confirmed_df)

# data_text = f'Data Source: <a href="{DATA_SOURCE}">Johns Hopkins CSEE</a>'
# code_text = f'Code Source: <a href="{CODE_SOURCE}">Github</a>'

footer_text_md = dcc.Markdown(f"""
    Data Source: [Johns Hopkins CSEE]({DATA_SOURCE})
    Code Source: [Github]({CODE_SOURCE})
    """)

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
    html.H1(children='Covid-19 Trends', style={'textAlign': 'center'}),
    html.Br(),

    dropdown_layout,

    html.H3(id='display-selected-values', style={'textAlign': 'center'}),
    dcc.Graph(id='confirmed-trend'),
    dcc.Graph(id='recovered-trend'),
    dcc.Graph(id='death-trend'),

    html.Hr(),
    html.Footer(footer_text_md)
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


@app.callback(
    Output('display-selected-values', 'children'),
    [Input('countries-dd', 'value'),
     Input('states-dd', 'value')])
def set_display_children(selected_country, selected_state):
    if selected_state == 'All':
        text = selected_country
    else:
        text = f'{selected_state}, {selected_country}'

    return text


@app.callback(
    Output('confirmed-trend', 'figure'),
    [Input('countries-dd', 'value'),
     Input('states-dd', 'value')])
def update_confirmed_visual(selected_country, selected_state):
    df = get_data(
        state=selected_state,
        country=selected_country,
        data=confirmed_df,
        include_feb=False)

    #fig = px.line(df, x='Date', y='Value', )

    return get_confirmed_trend(df)


@app.callback(
    Output('recovered-trend', 'figure'),
    [Input('countries-dd', 'value'),
     Input('states-dd', 'value')])
def update_recovered_visual(selected_country, selected_state):
    df = get_data(
        state=selected_state,
        country=selected_country,
        data=recovered_df,
        include_feb=False)

    #fig = px.line(df, x='Date', y='Value', )

    return get_recovered_trend(df)


@app.callback(
    Output('death-trend', 'figure'),
    [Input('countries-dd', 'value'),
     Input('states-dd', 'value')])
def update_death_visual(selected_country, selected_state):
    df = get_data(
        state=selected_state,
        country=selected_country,
        data=death_df,
        include_feb=False)

    #fig = px.line(df, x='Date', y='Value', )

    return get_death_trend(df)


if __name__ == '__main__':
    app.run_server(debug=True)