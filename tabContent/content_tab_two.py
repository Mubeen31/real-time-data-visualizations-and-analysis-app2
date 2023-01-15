import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
from datetime import datetime
from app import app
import plotly.graph_objs as go

layout_tab_two = html.Div([

    dcc.Interval(id='update_value2',
                 interval=1 * 16000,
                 n_intervals=0),

    html.Div([
        html.Div([
            dcc.Graph(id='line_chart2',
                      config={'displayModeBar': False})
        ], className='tab_page eight columns')

    ], className='tab_content_row row')

])


@app.callback(Output('line_chart2', 'figure'),
              [Input('update_value2', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/1.csv?results=50'
    df = pd.read_csv(url)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')

    return {
        'data': [go.Scatter(
            x=df['created_at'],
            y=df['field1'],
            mode='markers+lines',
            line=dict(width=3, color='#FFBF00'),
            marker=dict(size=7, symbol='circle', color='#FFBF00',
                        line=dict(width=2, color='#FFBF00')),
            hoverinfo='text',
            hovertext=
            '<b>Date Time</b>: ' + df['created_at'].astype(str) + '<br>' +
            '<b>Humidity (%)</b>: ' + [f'{x:.2f} %' for x in df['field1']] + '<br>'

        )],
        'layout': go.Layout(
            margin=dict(t=50, l=50, r=40),
            hovermode='closest',
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            title={'text': '<b>Humidity (%)',
                   'y': 0.95,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'size': 17,
                       'color': '#FFBF00'},
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
            yaxis=dict(range=[min(df['field1']) - 0.05, max(df['field1']) + 0.05],
                       showline=False,
                       showgrid=True,
                       gridcolor='#e6e6e6',
                       tickfont=dict(family='Arial',
                                     size=12,
                                     color='#666666')
                       )
        )
    }
