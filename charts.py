import plotly.graph_objects as go


def get_confirmed_trend(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
                    x=df.Date,
                    y=df.Value,
                    line_color='deepskyblue',
                    opacity=0.8))
    fig.update_layout(title={
                        'text': 'Confirmed cases',
                        'y': 0.85,
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                   xaxis_title='',
                   yaxis_title='')
    return fig


def get_recovered_trend(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
                    x=df.Date,
                    y=df.Value,
                    line_color='darkgreen',
                    opacity=0.8))
    fig.update_layout(title={
                        'text': 'Recovered cases',
                        'y': 0.85,
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                   xaxis_title='',
                   yaxis_title='')
    return fig


def get_death_trend(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
                    x=df.Date,
                    y=df.Value,
                    line_color='crimson',
                    opacity=0.8))
    fig.update_layout(title={
                        'text': 'Death cases',
                        'y': 0.85,
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                   xaxis_title='',
                   yaxis_title='')
    return fig
