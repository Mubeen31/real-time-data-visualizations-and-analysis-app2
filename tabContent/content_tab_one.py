import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
from datetime import datetime
from app import app
import plotly.graph_objs as go

layout_tab_one = html.Div([

    dcc.Interval(id='update_value1',
                 interval=1 * 16000,
                 n_intervals=0),

    html.Div([
        html.Div([
            dcc.Graph(id='line_chart1',
                      config={'displayModeBar': False})
        ], className='tab_page eight columns')

    ], className='tab_content_row row')

])


@app.callback(Output('line_chart1', 'figure'),
              [Input('update_value1', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/2.csv?results=50'
    df = pd.read_csv(url)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')

    return {
        'data': [go.Scatter(
            x=df['created_at'],
            y=df['field2'],
            mode='markers+lines',
            line=dict(width=3, color='#1EEC11'),
            marker=dict(size=7, symbol='circle', color='#1EEC11',
                        line=dict(width=2, color='#1EEC11')),
            hoverinfo='text',
            hovertext=
            '<b>Date Time</b>: ' + df['created_at'].astype(str) + '<br>' +
            '<b>Temperature (°C)</b>: ' + [f'{x:.2f} °C' for x in df['field2']] + '<br>'

        )],
        'layout': go.Layout(
            margin=dict(t=50, l=50, r=40),
            hovermode='closest',
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            title={'text': '<b>Temperature (°C)',
                   'y': 0.95,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'size': 17,
                       'color': '#1EEC11'},
            xaxis=dict(
                showline=True,
                showgrid=False,
                linecolor='#666666',
                linewidth=1,
                ticks='outside',
                tickfont=dict(family='Arial',
                              size=12,
                              color='#666666')
            ),
            yaxis=dict(range=[min(df['field2']) - 0.05, max(df['field2']) + 0.05],
                       showline=False,
                       showgrid=True,
                       gridcolor='#e6e6e6',
                       tickfont=dict(family='Arial',
                                     size=12,
                                     color='#666666')
                       )
        )
    }
