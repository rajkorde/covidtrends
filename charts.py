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
