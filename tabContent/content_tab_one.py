import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
from datetime import datetime
from app import app
import plotly.graph_objs as go
import dash_daq as daq

layout_tab_one = html.Div([

    dcc.Interval(id='update_value1',
                 interval=1 * 16000,
                 n_intervals=0),

    html.Div([
        html.Div([
            dcc.Graph(id='line_chart1',
                      config={'displayModeBar': False}),
            html.Div([
                daq.BooleanSwitch(id='line_color',
                                  on=True,
                                  color="#9B51E0",
                                  label='Line color',
                                  labelPosition='top'
                                  ),
                daq.BooleanSwitch(id='last_values',
                                  on=True,
                                  color="#9B51E0",
                                  label='Select last values',
                                  labelPosition='top'
                                  )
            ], className='button_row')
        ], className='tab_page eight columns')

    ], className='tab_content_row row')

])


@app.callback(Output('line_chart1', 'figure'),
              [Input('update_value1', 'n_intervals')],
              [Input('line_color', 'on')],
              [Input('last_values', 'on')])
def update_value(n_intervals, line_color, last_values):
    url = 'https://api.thingspeak.com/channels/2007583/fields/2.csv?results=50'
    df = pd.read_csv(url)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')

    url1 = 'https://api.thingspeak.com/channels/2007583/fields/2.csv?results=15'
    df1 = pd.read_csv(url1)
    df1['created_at'] = pd.to_datetime(df1['created_at'])
    df1['created_at'] = pd.to_datetime(df1['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')

    if line_color == True and last_values == True:
        return {
            'data': [go.Scatter(
                x=df['created_at'],
                y=df['field2'],
                mode='markers+lines',
                line=dict(width=3, color='rgb(214, 32, 32)'),
                marker=dict(size=7, symbol='circle', color='rgb(214, 32, 32)',
                            line=dict(width=2, color='rgb(214, 32, 32)')),
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
                           'color': 'rgb(214, 32, 32)'},
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

    if line_color == True and last_values == False:
        return {
            'data': [go.Scatter(
                x=df1['created_at'],
                y=df1['field2'],
                mode='markers+lines',
                line=dict(width=3, color='rgb(214, 32, 32)'),
                marker=dict(size=7, symbol='circle', color='rgb(214, 32, 32)',
                            line=dict(width=2, color='rgb(214, 32, 32)')),
                hoverinfo='text',
                hovertext=
                '<b>Date Time</b>: ' + df1['created_at'].astype(str) + '<br>' +
                '<b>Temperature (°C)</b>: ' + [f'{x:.2f} °C' for x in df1['field2']] + '<br>'

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
                           'color': 'rgb(214, 32, 32)'},
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
                yaxis=dict(range=[min(df1['field2']) - 0.05, max(df1['field2']) + 0.05],
                           showline=False,
                           showgrid=True,
                           gridcolor='#e6e6e6',
                           tickfont=dict(family='Arial',
                                         size=12,
                                         color='#666666')
                           )
            )
        }

    elif line_color == False and last_values == True:
        return {
            'data': [go.Scatter(
                x=df['created_at'],
                y=df['field2'],
                mode='markers+lines',
                line=dict(width=3, color='#0000FF'),
                marker=dict(size=7, symbol='circle', color='#0000FF',
                            line=dict(width=2, color='#0000FF')),
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
                           'color': '#0000FF'},
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

    elif line_color == False and last_values == False:
        return {
            'data': [go.Scatter(
                x=df1['created_at'],
                y=df1['field2'],
                mode='markers+lines',
                line=dict(width=3, color='#0000FF'),
                marker=dict(size=7, symbol='circle', color='#0000FF',
                            line=dict(width=2, color='#0000FF')),
                hoverinfo='text',
                hovertext=
                '<b>Date Time</b>: ' + df1['created_at'].astype(str) + '<br>' +
                '<b>Temperature (°C)</b>: ' + [f'{x:.2f} °C' for x in df1['field2']] + '<br>'

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
                           'color': '#0000FF'},
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
                yaxis=dict(range=[min(df1['field2']) - 0.05, max(df1['field2']) + 0.05],
                           showline=False,
                           showgrid=True,
                           gridcolor='#e6e6e6',
                           tickfont=dict(family='Arial',
                                         size=12,
                                         color='#666666')
                           )
            )
        }
