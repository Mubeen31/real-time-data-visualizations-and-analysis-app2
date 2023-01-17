import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
from datetime import datetime
from app import app
import plotly.graph_objs as go
import numpy as np

layout_tab_three = html.Div([
    dcc.Interval(id='update_value3',
                 interval=1 * 16000,
                 n_intervals=0),

    html.Div([
        html.Div([
            dcc.Graph(id='line_chart3',
                      config={'displayModeBar': False})
        ], className='tab_page eight columns')

    ], className='tab_content_row row')
])


@app.callback(Output('line_chart3', 'figure'),
              [Input('update_value3', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/2.csv?days=2'
    df = pd.read_csv(url)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df['Date'] = pd.to_datetime(df['created_at']).dt.date
    df['Hour'] = pd.to_datetime(df['created_at']).dt.hour
    unique = df['Date'].unique()
    filter_yesterday_date = df[df['Date'] == unique[-2]][['Date', 'Hour', 'field2']]
    yesterday_hourly_values = filter_yesterday_date.groupby(['Date', 'Hour'])['field2'].mean().reset_index()

    url1 = 'https://api.thingspeak.com/channels/2007583/fields/2.csv?days=1'
    df1 = pd.read_csv(url1)
    df1['created_at'] = pd.to_datetime(df1['created_at'])
    df1['created_at'] = pd.to_datetime(df1['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df1['Date'] = pd.to_datetime(df1['created_at']).dt.date
    df1['Hour'] = pd.to_datetime(df1['created_at']).dt.hour
    unique = df1['Date'].unique()
    filter_today_date = df1[df1['Date'] == unique[-1]][['Date', 'Hour', 'field2']]
    today_hourly_values = filter_today_date.groupby(['Date', 'Hour'])['field2'].mean().reset_index()

    return {
        'data': [go.Bar(
            x=today_hourly_values['Hour'],
            y=today_hourly_values['field2'],
            name='Today Average Temperature (°C)',
            marker=dict(color='#FFBF00'),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + today_hourly_values['Date'].astype(str) + '<br>' +
            '<b>Hour</b>: ' + today_hourly_values['Hour'].astype(str) + '<br>' +
            '<b>Temperature (°C)</b>: ' + [f'{x:.2f} °C' for x in today_hourly_values['field2']] + '<br>'

        ),
            go.Scatter(
            x=yesterday_hourly_values['Hour'],
            y=yesterday_hourly_values['field2'],
            name='Yesterday Average Temperature (°C)',
            mode='markers+lines',
            line=dict(width=3, color='rgb(214, 32, 32)'),
            marker=dict(size=7, symbol='circle', color='rgb(214, 32, 32)',
                        line=dict(width=2, color='rgb(214, 32, 32)')),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + yesterday_hourly_values['Date'].astype(str) + '<br>' +
            '<b>Hour</b>: ' + yesterday_hourly_values['Hour'].astype(str) + '<br>' +
            '<b>Temperature (°C)</b>: ' + [f'{x:.2f} °' for x in yesterday_hourly_values['field2']] + '<br>'

        )],
        'layout': go.Layout(
            margin=dict(t=50, l=50, r=40),
            hovermode='closest',
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            title={'text': '<b>Comparison two days Temperature (°C)',
                   'y': 0.95,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'size': 17,
                       'color': 'rgb(214, 32, 32)'},
            xaxis=dict(
                tick0=0,
                dtick=1,
                zeroline=False,
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
                       zeroline=False,
                       showline=False,
                       showgrid=True,
                       gridcolor='#e6e6e6',
                       tickfont=dict(family='Arial',
                                     size=12,
                                     color='#666666')
                       ),
            legend={
                'orientation': 'h',
                'bgcolor': 'rgba(255, 255, 255, 0)',
                'x': 0.5,
                'y': -0.3,
                'xanchor': 'center',
                'yanchor': 'bottom'},
            font=dict(
                family="sans-serif",
                size=12,
                color='#666666')
        )
    }
